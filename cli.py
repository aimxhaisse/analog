#!/usr/bin/env python3

"""Analog processing tools.
"""

import click
import os
import re
import subprocess
import uuid
import pathlib

from wand.image import Image


@click.group()
def main():
    pass


def compress_if_needed(fp):
    """Losslessly compress TIFF images if not yet done.
    """
    try:
        with Image(filename=fp) as image:
            click.echo(f'inspecting image {fp} format={image.format} compression={image.compression}')

            if image.format == 'TIFF' and image.compression == 'no':
                click.echo(f'compressing {fp}...')
                command = ['magick', 'mogrify', '-compress', 'zip', fp]
                subprocess.run(command)
            else:
                click.echo(f'skipped {fp} as it is already processed')

    except Exception as e:
        click.echo(f'unable to process image {fp}: {e}, skipped')


def rename_if_needed(fp):
    """Rename images to fit the uuid format if not yet done.
    """
    p = pathlib.Path(fp)
    suffix = p.suffix
    if suffix == '.tif':
        name = p.stem
        is_uuid = '^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$'
        if not re.match(is_uuid, name):
            dst = f'{p.parent}/{uuid.uuid4()}.tif'
            click.echo(f'renaming {fp} to {dst}...')
            os.rename(fp, dst)


@main.command()
@click.argument('path')
def filmify(path: str):
    """Processes all images from a directory.
    """
    images = []
    for entry in os.listdir(path):
        fp = f'{path}/{entry}'
        compress_if_needed(fp)
        rename_if_needed(fp)
        


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

"""Analog processing tools.
"""

import click
import os
import re
import subprocess
import uuid

from wand.image import Image


@click.group()
def main():
    pass


@main.command()
@click.argument('path')
def filmify(path: str):
    """Processes all images from a directory.
    """
    images = []
    for entry in os.listdir(path):
        fp = f'{path}/{entry}'
        if os.path.isdir(fp):
            click.echo(f'processing subdirectory {fp}...')
            filmify(fp)
            continue

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
            click.warning(f'unable to process image {fp}: {e}, skipped')
        


if __name__ == '__main__':
    main()

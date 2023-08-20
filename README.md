# ANALOG

Tools for film processing.

## FILMIFY

`filmify` looks for a folder with TIFF scans of a film (can be 35mm or
120mm), then converts each file to a compressed TIFF file (lossless),
and renames it using UUIDs.  This is convenient to massively import
them in LightRoom Classic afterwards.

```
$ poetry shell
$ analog filmify ~/photos/
```

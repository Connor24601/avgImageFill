# avgImageFill
avgImageFill is an image manipulation script. The designed use case is to provide the script with an image and a black-and-white mask. The script will then color each 'cell' of the mask its average color.

This script will eventually have tie-ins with Blender.

usage: Image Filler [-h] [--version] [-v] [--verbose] [--dry-run] [-o O] [--output OUTPUT]
                    [--rough ROUGH] [--debug] [-m M] [--mask MASK]
                    imageFile

Takes an image and a mask, and fills the spaces defined by the mask by the average color

positional arguments:
  imageFile        image to process

options:
  -h, --help       show this help message and exit
  --version        show program's version number and exit
  -v               sets log level-- more 'v's means lower level
  --verbose        automatically sets log level to DEBUG
  --dry-run        does a dry run with no image saving
  -o O             output file
  --output OUTPUT  output file
  --rough ROUGH    takes an int, speeds up computation at cost of accuracy
  --debug          sets log level and enforces special pauses and input
  -m M             mask image to use
  --mask MASK      mask image to use

avgImageFiller is available on GitHub under the MIT license.
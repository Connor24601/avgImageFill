import PIL
import sys
import argparse
import logging
import src.imageLoader

#	major.minor.patch
VERSION = "0.0.0"
logging.basicConfig()
logger = logging.getLogger()


def main(parser):
	args = parser.parse_args()
	logLevel = args.v
	level = 40 - (10 * int(logLevel))
	if (args.verbose or args.debug):
		level = min(10, level)
	logger.setLevel(level)
	logging.info("Logging level set to %s", logging.getLevelName(logger.getEffectiveLevel()))
	logging.debug(sys.argv)
	if (args.debug):
		choice = input("DEBUG: Show all arguments? [y/N]: ").lower()
		if (choice in {"y","yes"}):
			print(args)
		print("DEBUG: continuing...")
	





if __name__ == "__main__":

	parser = argparse.ArgumentParser(prog='Image Filler',\
        description='Takes an image and a mask, and fills the spaces defined by the mask by the average color',\
        epilog='avgImageFiller is available on GitHub under the MIT license')
	parser.add_argument('--version', action='version', version='%(prog)s ' + VERSION)
	parser.add_argument('-v', action='count', default=0, help="sets log level-- more 'v's means lower level")
	parser.add_argument('--verbose', action='store_true',default=False, help="automatically sets log level to DEBUG")
	parser.add_argument('--dry-run', action='store_true', default=False, help="does a dry run with no image saving")
	parser.add_argument('--rough',action='store', default=0, help="takes an int, speeds up computation at cost of accuracy")
	parser.add_argument('--debug', action='store_true', default=False, help="sets log level and enforces special pauses and input")

	main(parser)
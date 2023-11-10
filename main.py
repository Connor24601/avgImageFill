#!/usr/bin/env python3

import sys
import argparse
import logging
import src.FileManager as FileManager
from utilities.util import CONSTANTS
import src.ImageManipulator as ImageManipulator

def main(args):
	
	
	logger = setupLogger("main")
	if (args.debug):
		choice = input("Show all arguments? [y/N]: ").lower()
		if (choice in {"y","yes"}):
			logger.debug(args)
		logger.debug("continuing...")
	
	try:
		mask = args.m if args.m != '' else args.mask
		output = args.o if args.o != './output.png' else args.output
		fileManager = FileManager.FileManager(args.imageFile,mask, output)
		imageManipulator = ImageManipulator.ImageManipulator(fileManager, args.rough, args.dry_run)

	except Exception as e:
		logger.critical(e)
	else:
		return -1
	finally:
		return 0
	
	



def setupLogger(name, **kwargs):
	logger = logging.getLogger(name)
	logLevel = kwargs.get("level", CONSTANTS.LOG_LEVEL)
	logger.setLevel(logLevel)
	try:
		import coloredlogs
		coloredlogs.install(level=logLevel, logger=logger,\
		 fmt='%(asctime)s %(name)s %(levelname)s: %(message)s',\
		 datefmt='%H:%M:%S',\
		 field_styles = {'asctime': {'color': 8}, 'name': {'color':103},'levelname': {'bold': True, 'color':'white'} })
		logger.debug("successfully set up colored logs")
	except Exception as e:
		logger.warning("%s: could not get optional dependency: coloredLogs", name)
	finally:
		logger.info("%s: logging level set to %s", name, logging.getLevelName(logger.getEffectiveLevel()))
		return logger
	




if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog='Image Filler',\
        description='Takes an image and a mask, and fills the spaces defined by the mask by the average color',\
        epilog='avgImageFiller is available on GitHub under the MIT license')
	parser.add_argument('--version', action='version', version='%(prog)s ' + CONSTANTS.VERSION)
	parser.add_argument('-v', action='count', default=0, help="sets log level-- more 'v's means lower level")
	parser.add_argument('--verbose', action='store_true',default=False, help="automatically sets log level to DEBUG")
	parser.add_argument('--dry-run', action='store_true', default=False, help="does a dry run with no image saving")
	parser.add_argument('-o', action='store', default='./output.png', help="output file")
	parser.add_argument('--output', action='store', default='./output.png', help="output file")
	parser.add_argument('--rough',action='store', default=0, help="takes an int, speeds up computation at cost of accuracy")
	parser.add_argument('--debug', action='store_true', default=False, help="sets log level and enforces special pauses and input")
	parser.add_argument('imageFile', action='store', default="", help="image to process")
	parser.add_argument('-m', action='store', default="", help="mask image to use")
	parser.add_argument('--mask', action='store', default="", help="mask image to use")
	#parser.add_argument('--resX', action='store', default=1920, help="resolution")
	#parser.add_argument('--resY', action='store', default=1080)

	args = parser.parse_args()
	CONSTANTS.LOG_LEVEL = max(40 - (10 * int(args.v)), 10)
	if (args.verbose or args.debug):
		CONSTANTS.LOG_LEVEL = min(10, CONSTANTS.LOG_LEVEL)

	main(args)



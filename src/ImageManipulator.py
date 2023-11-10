import sys
import logging

main = None
for i in range(2):
	try:
		import main
		break
	except ModuleNotFoundError as e:
		sys.path.append('../avgImageFill')
	except Exception as e:
		logging.getLogger("ImageManipulator").critical(e)
	
if (main == None):
	logging.getLogger("ImageManipulator").critical("Critical: Could not find main from ImageManipulator")
	exit(-1)


import src.FileManager as FileManager

class ImageManipulator:
	def __init__(self, FileManager, skipNum, dryRun):
		self.FileManager = FileManager
		self.logger = main.setupLogger("ImageManipulator")
		self.logger.debug("initializing ImageManipulator")
		import PIL
		import PIL.Image
		self.PIL = PIL







if __name__ == "__main__":
	logger = main.setupLogger("ImageManipulator", level=0)
	logger.warning("This file should only be run manually if testing")

import sys
import logging
import main
import src.FileManager as FileManager

class ImageManipulator:
	def __init__(self, FileManager, skipNum, ):
		self.FileManager = FileManager
		self.logger = main.setupLogger("ImageManipulator")
		logger.debug("initializing ImageManipulator")
		import PIL
		import PIL.Image
		self.PIL = PIL
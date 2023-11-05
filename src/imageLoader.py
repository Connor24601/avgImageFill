import sys
import logging
import main


class ImageLoader:
	def __init__(self, pathImage, pathMask):
		self.pathMask = pathMask
		self.pathImage = pathImage
		self.logger = main.setupLogger("imageLoader")
		if (self.pathImage == ""):
			self.logger.error("No image file provided-- running demo")
			self.pathImage = ""
		if (self.pathMask == ""):
			self.logger.warning("No mask image file provided-- using default")
			self.pathMask = ""
		try:
			import PIL
			self.logger.info("Pillow successfully found")
		except Exception as e:
			self.logger.critical("Could not find critical dependency Pillow")
			self.logger.warning("Please install Pillow. Exiting...")
			exit()
		finally:
			return




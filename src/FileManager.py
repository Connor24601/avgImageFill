import sys
import logging
import main


class FileManager:
	def __init__(self, pathImage, pathMask, output):
		self.pathMask = pathMask
		self.pathImage = pathImage
		self.output = output
		self.logger = main.setupLogger("FileManager")
		try:
			import PIL
			import PIL.Image
			self.PIL = PIL
			self.logger.info("Pillow successfully found")
		except Exception as e:
			self.logger.critical("Could not find critical dependency Pillow")
			self.logger.warning("Please install Pillow. Exiting...")
			exit()

		if (self.pathImage == ""):
			self.logger.error("No image file provided-- running demo")
			self.pathImage = "./Utilities/demo.png"
		if (self.pathMask == ""):
			self.logger.warning("No mask image file provided-- using default")
			self.pathMask = "./Utilities/defaultMask.png"

		try:
			self.input = None
			self.mask = None
			self.input = self.PIL.Image.open(self.pathImage)
			self.mask = self.PIL.Image.open(self.pathMask)
		except FileNotFoundError as e:
			badPath = self.pathImage if self.input == None else self.pathMask
			self.logger.error("Could not find image: %s", badPath)
		except Exception as e:
			self.logger.error(e)
		else:
			return
		return

	def createNewImage(**kwargs):
		#kwargs.path
		newImage = self.PIL.Image.new('HSV',(1080,1080))
		return newImage



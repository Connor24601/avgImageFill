import sys
import logging
from random import random
from random import randint
main = None
for i in range(2):
	try:
		import main
		from src.img.Pixel import Pixel as Pixel
		from src.img.Pixel import Region as Region
		logging.getLogger("main").debug("Successfully found things")
		assert(Region != None)
		break
	except ModuleNotFoundError as e:
		logging.getLogger("main").info(e)
		logging.getLogger("main").debug("current path: %s", sys.path[0])
		sys.path.append('../avgImageFill')
		#retry
	except AssertionError as e:
		throw(e)
	except Exception as e:
		throw(e)
	
if (main == None):
	logging.getLogger("main").critical("Critical: Could not find main from ImageManipulator")
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
		self.skip = skipNum + 1
		self.dryRun = dryRun
		self.output = None
		self.maskRegion = None
		self.regions = None

	def validationTest(self, image):
		self.logger.debug("testing random cell...")
		testY = randint(0, image.height)
		testX = randint(0, image.width)
		self.logger.debug("image %s has width of %s, height %s",image, image.width,image.height)
		self.logger.debug("value at (%s,%s): %s",testX,testY, image[testY][testX])

	def segFill(self,image, mask):
		try:
			self.floodRegionGeneration(image,mask)
		except Exception as e:
			self.logger.critical("Failure during region generation: %s", e)
		else:
			pass
		finally:
			return
		

	'''
	inefficient but no missing cases
	'''
	def floodRegionGeneration(self,image, mask):
		self.logger.debug("performing flood region generation")
		self.regions = {}
		self.maskRegion = Region("MASK")
		self.output = [[None]* image.width]*image.height
		for y in range(0, image.height, self.skip):
			for x in range(0, image.width, self.skip):
				if (self.output[y][x] != None):
					if mask[x][y].Color >= self.threshold:
						continue
					region = Region((x,y))
					startX = x
					lastX = image.width
					regionDone = True
					for subY in range(y, image.height, self.skip):
						if regionDone:
							break
						regionDone = True
						for subX in range(startX, image.width, self.skip):
							if True:#if mask[subX][subY].Color >= self.threshold and !(regionDone or lastX<subX):
								pixel = Pixel(subX,subY,image[subX][subY].color) #TODO: get value from image
								self.maskRegion.add(pixel)
								continue
							if True:#if mask[subX][subY].Color <= self.threshold:
								lastX = subX
								pixel = Pixel(subX,subY,image[subX][subY].color) #TODO: get value from image
								self.maskRegion.add(pixel)
								break
							if regionDone:
								startX = subX
							regionDone = False
							if self.output[subX][subY] != None:
								self.logger.info("Found pre-existing region at %s", (subX, subY))
								pixel = self.output[subX][SubY]
								if (pixel.region != region):
									region += pixel.region
									#self.regions.remove(pixel.region) #TODO: remove empty region from regions list
							pixel = Pixel(subX,subY,image[subX][subY].color) #TODO: get value from image
							region.add(pixel)
							self.output[subX][subY] = pixel
					self.regions.append(region)
		self.logger.debug("flood region generation completed with %s regions", len(self.regions))
		return self.regions, self.output


		

	def fastFill(image,mask):
		for y in range(0, image.height, self.skip):
			region = 0
			for x in range(0, image.width, self.skip):
				if mask[x][y].Color >= self.threshold:
					if (region == 0):
						regions += 1 # unsure how to deal with looped regions
						#acute polyhedral vs squiggly?

			









if __name__ == "__main__":
	logger = main.setupLogger("ImageManipulator", level=0)
	logger.warning("This file should only be run manually if testing")

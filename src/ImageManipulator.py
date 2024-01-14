import sys
import logging
from random import random
from random import randint
main = None
for i in range(2):
	try:
		import main
		from src.img.Pixel import Pixel
		from src.img.Pixel import Color
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
		self.threshold = Color((128,128,128))

	def imagePixelTest(self, image):
		self.logger.debug("testing random cell...")
		testY = randint(0, image.height)
		testX = randint(0, image.width)
		self.logger.debug("image %s has width of %s, height %s",image, image.width,image.height)
		self.logger.debug("value at (%s,%s): %s",testX,testY, image.getpixel((testX,testY)))
		self.logger.debug("value at (%s,%s): %s",0,0, image.getpixel((0,0)))

	def segFill(self,image, mask):
		try:
			self.floodRegionGeneration(image,mask)
			self.logger.info("proceeding to color regions")
			self.colorRegions()
		except Exception as e:
			self.logger.critical("Failure during region generation - %s : %s", type(e), e)
			self.logger.exception(e)
			raise
		else:
			pass
		finally:
			return
		
	def validationTest(self, image):
		total = 0
		assert(len(self.output) == image.height)
		for y in range(0,len(self.output)):
			assert(len(self.output[y]) == image.width)
			for x in range(0,len(self.output[y])):
				pixel = self.output[y][x]
				assert(pixel != None)
				assert(type(pixel) == Pixel)
				if (pixel.y != y):
					self.logger.warning("values differ: %s, %s", pixel, (x,y))
					self.logger.warning("values at %s : %s",(x,y),self.output[y][x])
				assert(pixel.x == x)
				#assert(pixel.y == y)
				if (pixel.region != "MASK"):
					assert(pixel.region in self.regions.keys())
				total += 1
		assert(total == image.height*image.width)
		self.logger.debug("Output validation passed on %s pixels", total)
		self.logger.debug("Proceeding with %s regions", len(self.regions))
		for hashVal in self.regions.keys():
			self.logger.debug("region %s with %s pixels", hashVal, len(self.regions[hashVal]))
		self.logger.debug("region %s with %s pixels", "MASK", len(self.maskRegion))
		self.logger.debug("All validation passed")
		return 1
	'''
	inefficient but no missing cases
	'''
	def floodFill(self,x,y,image,mask):
		pointSet = set()
		unverified = set()
		verified = set()
		unverified.add((x,y))
		while len(unverified) > 0:
			x,y = unverified.pop()
			verified.add((x,y))
			if x<0 or y<0 or x>=image.width or y>=image.height:
				continue
			maskColor = Color(mask.getpixel((x,y)))
			if not maskColor < self.threshold:
				pointSet.add((x,y))
				if ((x-self.skip,y) not in verified):
					unverified.add((x-self.skip,y))
				if ((x+self.skip,y) not in verified):
					unverified.add((x+self.skip,y))
				if ((x,y-self.skip) not in verified):
					unverified.add((x, y-self.skip))
				if ((x,y+self.skip) not in verified):
					unverified.add((x, y+self.skip))
		return pointSet

	def colorRegions(self):
		for region in self.regions.values():
			region.averageColor()

	def floodRegionGeneration(self,image, mask):
		self.logger.info("performing flood region generation")
		self.regions = {}
		self.maskRegion = Region("MASK")
		self.output = []
		for y in range(0, image.height):
			self.output.append([None]*image.width)
		self.logger.debug("output size %s by %s", len(self.output), len(self.output[0]))
		for y in range(0, image.height, self.skip):
			for x in range(0, image.width, self.skip):
				if (self.output[y][x] == None):
					maskColor = Color(mask.getpixel((x,y)))
					if maskColor < self.threshold:
						pixel = Pixel(x,y,maskColor)
						self.maskRegion.add(pixel)
						self.output[y][x] = pixel
						assert(pixel.x == x and pixel.y == y)
						continue
					else:
						pixel = Pixel(x,y,Color(image.getpixel((x,y))))
						maskColor = Color(mask.getpixel((x,y)))
						assert(self.threshold < maskColor)
						self.logger.debug("performing flood at (%s,%s)",x,y)
						newRegion = Region(hash((x,y)))
						pointSet = self.floodFill(x,y,image,mask)
						self.logger.debug("filled %s pixels", len(pointSet))
						assert((x,y) in pointSet)
						for xy in pointSet:
							pixel = Pixel(xy[0],xy[1],Color(image.getpixel((xy[0],xy[1]))))
							if self.output[xy[1]][xy[0]] != None:
								self.logger.warning("filling region that already has filled pixel!")
								continue
							self.output[pixel.y][pixel.x] = pixel
							newRegion.add(pixel)
						self.logger.debug("added region %s", newRegion.hash)
						self.regions[newRegion.hash] = newRegion
				assert(self.output[y][x] != None)
				pixel = self.output[y][x]
				assert(pixel.x == x and pixel.y == y)
		self.logger.info("flood region generation completed with %s regions", len(self.regions))
		self.logger.info("mask region contains %s pixels", len(self.maskRegion))
		return self.regions, self.output


	def paintOut(self,outImg):
		for y in range(0,len(self.output)):
			for x in range(0,len(self.output[y])):
				pixel = self.output[y][x]
				outImg.putpixel((x,y),pixel.color.toRGBA())

	def fastFill(self,image,mask):
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

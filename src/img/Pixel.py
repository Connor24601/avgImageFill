class Pixel:
	def __init__(self,x,y,color):
		self.x = x
		self.y = y
		self.color = color
		self.region = None
	def __str__(self):
		return "(x: "+ str(self.x) + ",y: "+ str(self.y) +")" + " - " + str(self.color.toRGBA())
	def __repr__(self):
		return self.__str__()
	def isEqual(self,other):
		if type(other) != Pixel:
			return False
		return self.x == other.x and self.y == other.y and self.color == other.color
	def __eq__(self, other):
		if other == None:
			return False
		return self.x == other.x and self.y == other.y and self.color == other.color


class Color:
	def __init__(self,rgba):
		if len(rgba) < 4:
			self.r, self.g, self.b = rgba
			self.a = 255
		else:
			self.r,self.g,self.b,self.a = rgba
	def toRGBA(self):
		return (self.r, self.g, self.b, self.a)

	def toHex(self):
		#TODO(Connor24601): process rgb to hex code
		return NotImplemented

	def __eq__(self, other):
		return self.r == other.r and self.g == other.g and self.b == other.b and self.a == other.a
	def __lt__(self, other):
		return self.r < other.r and self.g < other.g and self.b < other.b
	def __gt__(self, other):
		return self.r > other.r and self.g > other.g and self.b > other.b

class Region:
	def __init__(self, hashNum):
		self.hash = hashNum
		self.pixels = []
	def __add__(self, other):
		assert(type(other) == Region)
		for pixel in other.pixels:
			pixel.region = self.hash
			self.pixels.append(pixel)
		other.pixels.clear()
		return self
	def add(self, pixel):
		pixel.region = self.hash
		self.pixels.append(pixel)
	def contains(self, compPixel):
		for pixel in self.pixels:
			if pixel.isEqual(compPixel):
				return True
		return False
	def averageColor(self):
		sumR, sumG, sumB, sumA = (0,0,0,0)
		for pixel in self.pixels:
			sumR += pixel.color.r
			sumG += pixel.color.g
			sumB += pixel.color.b
			sumA += pixel.color.a
		total = len(self)
		aveR = sumR // total
		aveG = sumG // total
		aveB = sumB // total
		aveA = sumA // total
		fillColor = Color((aveR,aveG,aveB,aveA))
		for pixel in self.pixels:
			pixel.color = fillColor
		return 1




	def __len__(self):
		return len(self.pixels)

class Pixel:
	def __init__(self,x,y,color):
		self.x = x
		self.y = y
		self.color = color
		self.region = None


class Color:
	def __init__(self,r,g,b,a):
		self.r, self.g, self.b = r, g, b
		if (a == None):
			self.a = 1
		else:
			self.a = a

	def toHex():
		#TODO(Connor24601): process rgb to hex code
		return NotImplemented

class Region:
	def __init__(self, hashNum):
		self.hash = hashNum
		self.pixels = []
	def __add__(self, other):
		assert(type(other) == Region)
		# TODO: map region values. i.e. 
		# other.pixels.map(pixel => pixel.region = this; return pixel)
		self.pixels.extend(other.pixels)
		other.pixels.clear()
		return self
	def add(self, pixel):
		pixel.region = self.hash
		self.pixels.add(pixel)

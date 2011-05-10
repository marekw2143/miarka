def callMediator(f):
	def z(self, value):
		f(self, value)
		self.mediator.distanceMeasured((self.xMM, self.yMM))
	return z

class DistanceConverter(object):
	u"""converts a distance given in pixels to the distance in milimeters"""

	def reset(self):

		

		# distance in milimeters
		self.xMM, self.yMM = 0.0, 0.0


	def __init__(self, mediator):
		self.reset()
		# how many ticks are there for mm in each axis
		self.xRatio, self.yRatio = 1.0, 1.0#0.0, 0.0

		self.mediator = mediator

	def setRatio(self, ratio): self.xRatio, self.yRatio = ratio
	def getRatio(self):return(self.xRatio, self.yRatio)


	@callMediator
	def convX(self, value): 
		self.xMM = float(value)/self.xRatio	

	@callMediator
	def convY(self, value): 
		self.yMM = float(value)/self.yRatio
		

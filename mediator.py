from cursor_manager import CursorManager
from distance_converter import DistanceConverter
from options import Options

from tick_counter import VirtualCoordCounter			
class Mediator(object):


	def __init__(self, cursor, client):
		u"""
			cursor - reference to the mouse cursor used
			client - reference to the client object, that implements method setDistance((x,y)) where x and y are the distances in mm made
				 by the cursor
		"""

		# configure cursorManager
		# cursorManger should implement the CursorManagerBase interface
		self.cursorManager = CursorManager(cursor, self)

	
		# configure VirtualCoordCounter
		self.coordCounter = VirtualCoordCounter(self)
		
		
		self.distanceConverter = DistanceConverter(self)

		self.client = client

		
	def tickX(self, dirrection):
		u"""fired by the cursorManager object when the x axis value changed, dirrection is a value in units how many this value changed"""

		# update global amount of ticks in x axis
		self.coordCounter.cX(dirrection)
		
	def tickY(self, dirrection):
		u"""fired by the cursorManager object when the y axis value changed, dirrection is a value in units how many this value changed"""

		# update global amount of ticks in y axis
		self.coordCounter.cY(dirrection)

	def tickDistanceXChanged(self, x):#, y):
		u"""called after global distance of ticks in x axis changed"""		
		
		# calculate global X distance in MM
		self.distanceConverter.convX(x)

	def tickDistanceYChanged(self, y):
		u""" called after global distance of ticks in Y axis changed"""
		
		# calculate new global Y distance in mm
		self.distanceConverter.convY(y)


	def distanceMeasured(self, distance):
		"""called after measuring the distance in mm, calls the client setDistance method"""

		self.client.setDistance(distance)

# client's interface
		
	def reset(self):
		u"""sets all objects values to their defaults"""
		self.cursorManager.reset()
		self.coordCounter.reset()
		self.distanceConverter.reset()

	def coordChanged(self):
		u"""fired by the client to indicate that the position of the mouse cursor changed"""
		self.cursorManager.positionChanged()

	def storeRatio(self, ratio):
		self.distanceConverter.setRatio(ratio)

		

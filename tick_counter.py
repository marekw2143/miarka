from tick_exception import TickException


def checkTickValue(f):
	u"""decorator that check the dirrection value before further processing
	in case the abs(dirrection)>1 then the TickException is raised"""
	def z(self, dif):
		if dif not in (-1,0,1):raise TickException()
		f(self, dif)
	return z

class VirtualCoordCounter(object):
	u"""this object is responsible to check if the tick noumber is modified by more than 1 unit"""
	def reset(self):
		u"""sets distance in ticks in each axis to 0"""
		self.ticksX, self.ticksY = 0, 0

	def __init__(self, mediator):
		self.reset()

		# save mediators reference
		self.mediator = mediator


	@checkTickValue
	def cX(self, dif):
		u"adds a given difference to the distance in x axis"		
		self.ticksX += dif
		self.mediator.tickDistanceXChanged(self.ticksX)

	@checkTickValue
	def cY(self, dif):
		u"adds a given difference to the distance in x axis"
		self.ticksY += dif
		self.mediator.tickDistanceYChanged(self.ticksY)

		







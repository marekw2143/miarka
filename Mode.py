class Mode(object):
	u"""represents mode of working of an application"""
	def __init__(self, client, modes):
		self.client = client
		self.dict = {}
		for number, value in enumerate(modes):
			self.dict[value] = number

	

	def setMode(self, mode):
		print "w set mode"
		# check if the given mode is proper
		if mode not in self.dict:raise Exception("Value % isn't enumerational" % mode)
		
		# if the mode changes - call the proper client's mode so that it will be able to take proper action (like Mediator pattern)
		try:
			print 'setMode.try:, mode: ',mode
			if mode != self._mode:
				client.modeChanged(mode)
		except:
			pass
		
		# change mode			
		self._mode = mode

	def getMode(self):
		try:
			return self._mode
		except:
			raise Exception("Mode not set yet")

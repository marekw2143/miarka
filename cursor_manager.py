class CursorManagerBase(object):
	u"""gives an interface to check how many pixels a mouse cursor changed. Doesn't take responsibility to check if position changes only a 1 unit 
	at a time"""

	def positionChanged(self):
		u"""controls the screens cursor position to allow it to roll around
		changes the cursor's position if needed
		eg. when the user moves the cursor to the maximum screen resolution Y position, then it won't be allowed to move it farer
		so the measurement in the given axis will be unavalible"""
		raise Exception("Method isn't implemented")

	def reset(self):	
		u"""set initial positions of the current CursorManager
		initalizes self's variables"""
		raise Exception("Method isn't implemented")

	
	def setCallbacks(self,tickX, tickY):
		u"""set functions called after each change of x or y of cursor's coordinates"""
		raise Exception("Method isn't implemented")




class CursorManager(CursorManagerBase):
	u"""gives an interface to check how many pixels a mouse cursor changed. Doesn't take responsibility to check if position changes only a 1 unit 
	at a time"""


	def reset(self):
		u"""set initial positions of the current CursorManager
		initalizes self's variables"""

		# reset old  coordinates values
		self.oldX, self.oldY = 0, 0
		
		# reset self virtual coordinates values
		self.virtualX, self.virtualY = 0, 0

		# global (in context of whole screen) positions of staring coordinates of virtual window
		# measured in pixels
		self.globalMinX, self.globalMinY = 10, 100

		# define size of virtual window
		self.height, self.width = 40, 40
		
		# set cursors position to initial values (the starting values of virtual window)
		self.cursor.setPos(self.globalMinX,self.globalMinY)

	def __init__(self, cursor, mediator, *args, **kwargs):
	
		# dictionary of functions called in every change of x or y
		self.changed = {'X':None, 'Y':None}
		
		# reference to mouse cursor
		self.cursor = cursor

		# reference to mediator object
		self.mediator = mediator

		# define and set initial values
		self.reset()		


	
	def positionChanged(self):
		u"""controls the screens cursor position to allow it to roll around
		changes the cursor's position if needed
		eg. when the user moves the cursor to the maximum screen resolution Y position, then it won't be allowed to move it farer
		so the measurement in the given axis will be unavalible"""

		cursor = self.cursor

				


		# count virtual Y
		self.virtualY = cursor.pos().y() - self.globalMinY
		
		# here we check the dirrection of axis coordinates
		dirrectionY = self.virtualY - self.oldY
		


		print 'positionChanged.dirrectionY: ',dirrectionY

		# changing virtualY and cursor positions so that it won't run over the allowed area
		if self.virtualY == self.height:
			# set virtual position of Y to 0, needed while computing total distance
			self.virtualY = 0
	
			# set cursors position properly
			cursor.setPos(cursor.pos().x(), self.globalMinY)

		# if cursor went to high (Y coord is too low)
		elif self.virtualY == -1:
	
			# set virtual position of Y to height-1, needed while computing total distance
			self.virtualY = self.height -1
	
			# set cursors position properly
			cursor.setPos(cursor.pos().x(), self.globalMinY+self.height-1)

		# in the next coordinates changing the oldY will be "current" virtualY
		self.oldY = self.virtualY





		# count virtual X
		self.virtualX = cursor.pos().x() - self.globalMinX
		
		# here we check the dirrection of axis coordinates
		dirrectionX = self.virtualX - self.oldX
		
		print 'positionChanged.directionX: ',dirrectionX

		

		# changing virtualY and cursor positions so that it won't run over the allowed area
		if self.virtualX == self.width:

			# set virtual position of X to 0, needed while computing total distance
			self.virtualX = 0
	
			# set cursors position properly
			cursor.setPos(self.globalMinX, cursor.pos().y())

		# if cursor went to over the left border of virtula screen (X coord too low)
		elif self.virtualX == -1:
	
			# set virtual position of Y to width-1, needed while computing total distance
			self.virtualX = self.width -1
	
			# set cursors position properly
			cursor.setPos(self.globalMinX+self.width-1, cursor.pos().y())
		# in the next coordinates changing the oldX will be "current" virtualX
		self.oldX = self.virtualX


		# if dirrection changed, call proper function
		if dirrectionY != 0: self.mediator.tickY(dirrectionY)
		if dirrectionX != 0: self.mediator.tickX(dirrectionX)

		return



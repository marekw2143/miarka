from PyQt4 import QtGui, QtCore

class MenuInterface(object):
	u"""interface of the menu"""
	def __init__(self, parent, dct, callNumber = None):
		u"""
			parent - needed by PyQt4
			dct    - list containing menu options. Each option is a tulpe consisting of two things - the text of the menu position
				 and the function called after the menu item is choosen
				 the menu items will appear in the menu in the order tthey were given in the list
			callNumber - if True, then after calling executeMethod the number of the menu option will be passed as a first and only argument
				     of the function. If False, then no argument will be passed """

		raise Exception("Method isn't implemented yet")
	
	def keyUp(self):
		u""" makes choosen the menu item above curent choosen item. If current choosen item is the first, then the last (the most on top) menu
		item will be choosen. If the next menu item to choose is inactive, then unless all menu items are inactive, the keyUp method is called 
		recursively"""
		raise Exception("Method isn't implemented yet")
	def keyDown(self):
		u""" makes choosen the menu item below the current choosen item. If current choosen item is the last, then the first (the first from above)
		menu item will be choosen. If the next menu item to choose is inactive, then unless all menu items are inactive, the keyDown method is 
		called recursively"""
		raise Exception("Method isn't implemented yet")

	def executeMethod(self):
		u""" causes the method correlated with the current choosen menu item will be fired"""
		raise Exception("Method isn't implemented yet")

	def activate(self, number):
		u"""makest the menu item with the number "number" available to choose"""
		raise Exception("Method isn't implemented yet")

	def deactivate(self, number):
		u"""makes the menu item with the number "number" unavailable to choose
		    if there is beeing deactivated an option wchich is currently choosen, then unless there is no other active menu option, the 
		    keyDown method is called"""
		raise Exception("Method isn't implemented yet")




class Menu(QtGui.QWidget):
	def __init__(self, parent, dct, callNumber = None):
		QtGui.QWidget.__init__(self, parent)
		
		self.v_box = QtGui.QVBoxLayout()
	
		self.selectedItem = 0

		self.dct = dict(dct)
		self.func = {}
		self.hidden = []

		self.callNumber = callNumber
		

		for i in range(len(dct)):
			number, key, function = i, dct[i][0], dct[i][1]
			self.func[number] = function			

			name = "label%s"%number
			

			# create new label		
			setattr(self, name, QtGui.QLabel(key, self))	

			# name of new horizontal layout
			h_name = "hbox%s"%name	
				
			# generate new horizontal layout
			setattr(self, h_name , QtGui.QHBoxLayout())
					
			# take reference to the new generated horizontal layout
			hbox = getattr(self, h_name)


			# name of the arrow showing which option is choosen
			arrow_name = "arrow%s"%name
		
			# create new label showing arrow
			setattr(self, arrow_name, QtGui.QLabel("  ", self))
#			getattr(self, arrow_name).hide()

			# add proper widets

			hbox.addWidget(getattr(self, arrow_name))

			hbox.addWidget(getattr(self, name))
			hbox.addStretch(1)
			# add the horizontal layout to the global vertical layout
			self.v_box.addLayout(hbox)

		#self.v_box.setGeometry(QtCore.QRect(0, 0, 100, 100))

		self.setLayout(self.v_box)
#		self.resize(600, 600)
		
		self.selectedItem = len(self.dct) - 1
		self.keyDown()

	def getCurrentArrowName(self):return "arrowlabel%s"%self.selectedItem

	def hideOption(self):
		getattr(self, self.getCurrentArrowName()).setText("  ")
		pass

	def showOption(self):
		getattr(self, self.getCurrentArrowName()).setText("->")
		pass
	def keyUp(self):
		u"""changing the selected menu item one unit up"""

		self.hideOption()

		self.selectedItem -= 1
		if self.selectedItem == -1: self.selectedItem = len(self.func) - 1

		if self.selectedItem in self.hidden:
			if len(self.hidden)==len(self.dct):return
			self.keyUp()
 
		self.showOption()

	def keyDown(self):
		self.hideOption()

		self.selectedItem += 1
		if self.selectedItem == len(self.func): self.selectedItem = 0

 		if  self.selectedItem in self.hidden: 
			if len(self.hidden)==len(self.dct):return
			self.keyDown()

		self.showOption()

	def executeMethod(self):
		args = self.callNumber and [self.selectedItem] or []
		self.func[self.selectedItem](*args)

	def deactivate(self, number):
		self.hidden.append(number)
		if number == self.selectedItem: self.keyDown()
	
	def activate(self, number):
		self.hidden = [x for x in self.hidden if x!=number]		

	#for tests
	def keyPressEvent(self, event):
		events={'A':self.keyUp, 'B':self.keyDown, 'E':self.executeMethod}
		if type(event) == QtGui.QKeyEvent:
			if chr(event.key()) in events: events[chr(event.key())]()


def piszA():
	myapp.deactivate(0)
	print 'A'
def piszB():print 'B'
def piszC():print 'C'
if __name__ == "__main__":

	import sys
	app = QtGui.QApplication(sys.argv)
	myapp = Menu(None, [("a",piszA), ("b",piszB), ("c",piszC)])
	myapp.show()
	sys.exit(app.exec_())

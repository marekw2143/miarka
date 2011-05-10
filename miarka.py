#! /usr/bin/python

# 
# author: Marek Wawrzyczek
# e-mail: mwawrzyczek@gmial.com
# project page: http://miarka.sourceforge.net
# author's blog: www.marekw2143.wordpress.com
#


from options import _, Options
from mediator import Mediator
from tick_exception import TickException

from Mode import Mode

from menu import Menu

from PyQt4 import QtCore, QtGui

from main_window import Ui_Form



programName = "Miarka 1.0 alpha"


class MyForm(QtGui.QMainWindow):	


	def modeChanged(self, mode):
		self.showInfoMessage(mode)
		pass


	
	def setMeasuringMode(self):
		self.mode.setMode("MEASURING")
		for i in (4,5,6,7): self.ui.menu.deactivate(i)
		self.calibration=None
		self.reset()

	def showInfoMessage(self, mes):
		u"""shows info message"""
		QtGui.QMessageBox.information(self, programName, mes, QtGui.QMessageBox.Ok)

	def setDistance(self, distance):
		u"""called by the mediator when the distance changes
		updates fields distX and distY
		calls updateUi"""
		self.distX, self.distY = distance[0], distance[1]
		self.updateUi()


	def updateUi(self):		
		u"""updates UI based on distX and distY values"""
		
		# global distance ran over detector in both axis
		formatedDistanceX, formatedDistanceY = "%.3F" % self.distX, "%.3F" % self.distY
		
		# natively show the distance ran over the detector
		textX, textY = formatedDistanceX, formatedDistanceY


		# update info about
		if self.mode.getMode() == "MEASURING":
			pass	


		# the calibrated axis doesn't show the global way ran
		elif self.mode.getMode() == "CAL_X": textX = _("calibration")
		elif self.mode.getMode() == "CAL_Y": textY = _("calibration")

		self.textX = "<font color=red size=4><b>" + textX + "</b></font>"


		# fill the data into labels

		from PyQt4 import Qt
		# showing total distance ran over cursor
		self.ui.lbWayX.setText(textX)
		self.ui.lbWayY.setText(textY)
		

		# calculate the remaining distance and show it
		remainingX = self.wantedX - self.distX
		remainingY = self.wantedY - self.distY
		self.ui.lbRemainingX.setText("%3.3F"%remainingX)
		self.ui.lbRemainingY.setText("%3.3F"%remainingY)

		# show the distance user wants to measure
		self.ui.lbWantedX.setText("%3.3F"%self.wantedX)
		self.ui.lbWantedY.setText("%3.3F"%self.wantedY)

		# show info about current working mode
		self.ui.lbMode.setText(str(self.mode.getMode()))



	def __init__(self, parent=None):

		# 
		QtGui.QWidget.__init__(self, parent)


		
#		from PyQt4 import QString
		self.ui = Ui_Form()
		self.ui.setupUi(self, [  (_('Reset'), self.reset),
					 (_('Measuring mode'), self.setMeasuringMode),
					 (_('Distance to measure in X axis'), self.askWantedX),
					 (_('Distance to measure in Y axis'), self.askWantedY),
					 (_('Calibrate Y axis'), self.calY),
					 (_('Calibrate X axis'), self.calX),
					 (_('Finish calibration'), self.finishCal),
					 (_('Save calibration'), self.saveRatio),
					 (_('Allow calibration'), self.allowCalibrate),
					])


		
		print 'main widget: ',self.centralWidget()
		self.centralWidget().setMouseTracking(True)
		# mode of working
		self.mode = Mode(self, ("MEASURING", "CAL_X", "CAL_Y"))

		# storing programs options
		self.options = Options()

		# object that manages all other objects :)
		self.mediator = Mediator(self.cursor(), self)




		# distance the user wants the device to travel
		self.wantedX, self.wantedY = 0.0, 0.0

		self.setMeasuringMode()
		# set default values
		self.reset()

		



	def reset(self):
		u"""resets ui and mediator, loads ratio from file (if was calibrated at runtime and not saved, then calibration data will
		be lost, sets distance to 0"""

		# distance travelled by the input device in the measurements units (defalutly milimeters)
		self.distX, self.distY = 0.0, 0.0
		
		self.mediator.reset()
		self.mediator.storeRatio(self.options.getRatio())

		self.updateUi()
	
	def askWanted(self, axis):
		text, ok = QtGui.QInputDialog.getText(self, programName, _('Distance to measure in %s axis:')%axis)
		name = {'X':'wantedX', 'Y':'wantedY'}
		try:
			# force converting to float
			text="%s.0" % text
			distance = float(eval(text))
			setattr(self, name[axis], distance)
		except:
			self.showInfoMessage(_("You entered inproper number. You can use arithmetic operators (+, -, * /)"))
		self.updateUi()

	def askWantedX(self):self.askWanted('X')
	def askWantedY(self):self.askWanted('Y')
			
	def allowCalibrate(self):
		text, ok = QtGui.QInputDialog.getText(self, programName, _("""Enter below "SUWMIARKA". 
It is protection against accidentally changing of the calibration configuration.
Entering word other than "SUWMIARKA" or pressing Cancel key simply returns to the mail menu and doesn't allow calibration.
If you choose to allow calibrating, and then with any cause you would like to turn off allowing calibration, choose option """)
+_('Measuring mode'))
		if ok:
			if text == "SUWMIARKA":
				for i in (4,5):	self.ui.menu.activate(i)

	def saveRatio(self):
		u"""saves ratio to a file"""
		try:
			self.options.saveRatio()
		# if some problems occurred, show the info message
		except:
			self.showInfoMessage(_("Error during saving calibration data to file."))
		# else show message that everything was ok
		else:
			self.showInfoMessage(_("Calibration data saved correctly"))
			


	def finishCal(self):
		u"""calculates the ratio of the calibrated axis, saves it to the options object (not to a file!!)"""
		if self.calibration == None:
			self.showInfoMessage("Blad programu")
		elif self.calibration in ('X','Y'):


			#TODO: tu jest odwolanie do mediatora, koniecznie ustaw odpowiednie metody !!
			if self.calibration =='X': przesuniecie = self.mediator.coordCounter.ticksX
			else: przesuniecie = self.mediator.coordCounter.ticksY

			self.showInfoMessage(_("General distance in axis %s: %s"%(self.calibration, przesuniecie)))

			text, ok = QtGui.QInputDialog.getText(self, programName, _('Enter distance the input device has moved: '))
			if ok:
				calc = przesuniecie / float(text)
				if self.calibration == 'X':  self.options.xRatio = calc
				elif self.calibration =='Y': self.options.yRatio = calc
			self.showInfoMessage(_("Ticks on milimeter in axis ")+self.calibration+_(" is: %s")%calc)

		self.calibration = None
		self.setMeasuringMode()
		self.ui.menu.activate(7)

	def cal(self, axis):
		u"""starts calibrating an axis"""
		self.ui.menu.activate(6)
		reply = QtGui.QMessageBox.information(self, programName, _("Starting calibration of axis: %s")%axis, QtGui.QMessageBox.Ok)
		if reply == QtGui.QMessageBox.Ok:
			self.reset()
			self.calibration = axis
	
	def calX(self):
		self.mode.setMode("CAL_X")
		self.cal('X')

	def calY(self):
		self.mode.setMode("CAL_Y")
		self.cal('Y')

	def keyPressEvent(self, event):
		proc = {'A':self.ui.menu.keyUp,'Z':self.ui.menu.keyDown,'K':self.ui.menu.executeMethod}
		if type(event) == QtGui.QKeyEvent:
			char = chr(event.key())
			print 'char: ',char
			if char in proc: proc[char]()


	def mouseMoveEvent(self, event):
		try:
			self.mediator.coordChanged()
		except TickException, e:
			QtGui.QMessageBox.information(self, "", _("Inproper reading from input device."), QtGui.QMessageBox.Ok)
			self.reset()






if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	myapp = MyForm()
	myapp.setMouseTracking(True)
	myapp.show()
	sys.exit(app.exec_())

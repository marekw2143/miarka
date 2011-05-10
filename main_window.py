# -*- coding: utf-8 -*-


from PyQt4 import QtCore, QtGui
from menu import Menu

from options import _

	
class Ui_Form(object):

    def modifyLabels(self):
	u"""sets the font size of the labels"""
        font = QtGui.QFont()
        font.setPointSize(50)
	for label in (self.lbWayX, self.lbWayY, self.lbDescWayX, self.lbDescWayY, self.lbRemainingX, self.lbRemainingY, self.lbDescRX, self.lbDescRY): 
		label.setFont(font)
		label.setMouseTracking(True)
	font.setPointSize(20)
	for label in (self.lbDescWayX, self.lbDescWayY, self.lbDescRX, self.lbDescRY): 
		label.setFont(font)
		label.setMouseTracking(True)


    def addWidgets(self,widget, widgetsToAdd):
	for w in widgetsToAdd: widget.addWidget(w)
	
    def setupUi(self, Form, dct):

	self.menu = Menu(Form, dct)
	
	# labels showing info about current working mode
	self.lbModeDescription = QtGui.QLabel(_("Working mode"), Form)
	self.lbMode = QtGui.QLabel(Form)

	# v_box representing info about current working mode
	self.v_box_mode_widget = QtGui.QWidget(Form)
	self.v_box_mode = QtGui.QVBoxLayout(self.v_box_mode_widget)
	self.v_box_mode.addStretch(1)
	self.v_box_mode.addWidget(self.lbModeDescription)
	self.v_box_mode.addWidget(self.lbMode)
	self.v_box_mode_widget.resize(200,200)
	



	# lalbels showing the total way in mm in proper axises
        self.lbWayX = QtGui.QLabel(Form)
        self.lbWayY = QtGui.QLabel(Form)


	# labels showing how much distance the user should ran so that he ran all he wants TODO: przetlumacz to na poprawny angielski
	self.lbRemainingX = QtGui.QLabel(Form)
	self.lbRemainingY = QtGui.QLabel(Form)

	# how many of way a device should travel overall
	self.lbDescWantedX = QtGui.QLabel(_("Distance to measure: "), Form)
	self.lbDescWantedY = QtGui.QLabel(_("Distance to measure: "), Form)
	self.lbWantedX = QtGui.QLabel(Form)
	self.lbWantedY = QtGui.QLabel(Form)


	# labels descriptioning labels showing the total distance ran by the detector (mouse)
	self.lbDescWayX = QtGui.QLabel("X:", Form)
	self.lbDescWayY = QtGui.QLabel("Y:", Form)

	self.lbDescRX = QtGui.QLabel(_("distance left:"), Form)
	self.lbDescRY = QtGui.QLabel(_("distance left:"), Form)

	#
	# grouped information: axis name and how many millimeters the detector (mouse) has moved:
	#
	self.h_box_x_widget = QtGui.QWidget(Form)
	self.h_box_x = QtGui.QHBoxLayout(self.h_box_x_widget)
	self.h_box_x.addWidget(self.lbDescWantedX)
	self.h_box_x.addWidget(self.lbWantedX)


	self.h_box_y_widget = QtGui.QWidget(Form)
	self.h_box_y = QtGui.QHBoxLayout(self.h_box_y_widget)
	self.h_box_y.addWidget(self.lbDescWantedY)
	self.h_box_y.addWidget(self.lbWantedY)


	# information of all axis
	self.v_box_dist_widget = QtGui.QWidget(Form)
	self.v_box_dist = QtGui.QVBoxLayout(self.v_box_dist_widget)

	self.v_box_dist.addWidget(self.h_box_x_widget)
	self.v_box_dist.addWidget(self.h_box_y_widget)


	
	self.info_box_widget = QtGui.QWidget()
	self.info_box = QtGui.QVBoxLayout(self.info_box_widget)

	
	for w in(self.v_box_mode_widget, self.menu, self.v_box_dist_widget, QtGui.QLabel("\t\t\t",Form)): self.info_box.addWidget(w)

	self.distanceWidget = QtGui.QWidget()
	self.distance = QtGui.QVBoxLayout(self.distanceWidget)

	self.distanceXWidget = QtGui.QWidget()
	self.distanceX = QtGui.QHBoxLayout(self.distanceXWidget)
	for w in (self.lbDescWayX, self.lbWayX):self.distanceX.addWidget(w)

	self.distanceYWidget = QtGui.QWidget()
	self.distanceY = QtGui.QHBoxLayout(self.distanceYWidget)
	for w in (self.lbDescWayY, self.lbWayY):self.distanceY.addWidget(w)

	
	for w in (self.distanceXWidget, self.distanceYWidget):self.distance.addWidget(w)


	self.distanceRemainingWidget = QtGui.QWidget()
	self.distanceRemaining = QtGui.QVBoxLayout(self.distanceRemainingWidget)

	self.distanceRXW = QtGui.QWidget()
	self.distanceRX = QtGui.QHBoxLayout(self.distanceRXW)
	for w in (self.lbDescRX, self.lbRemainingX): self.distanceRX.addWidget(w)

	self.distanceRYW = QtGui.QWidget()
	self.distanceRY = QtGui.QHBoxLayout(self.distanceRYW)
	for w in(self.lbDescRY, self.lbRemainingY): self.distanceRY.addWidget(w)

	self.distanceRemaining.addWidget(self.distanceRXW)
	self.distanceRemaining.addWidget(self.distanceRYW)

	self.distanceWidget.setMouseTracking(True)
	self.lbWayX.setMouseTracking(True)
	self.distanceXWidget.setMouseTracking(True)

	self.main_widget = QtGui.QWidget()
	self.main = QtGui.QHBoxLayout()
	for widget in (self.distanceWidget, self.distanceRemainingWidget, self.info_box_widget):self.main.addWidget(widget)
	

	self.main.setGeometry(QtCore.QRect(100,100,600,600))
        Form.setObjectName("Form")
#	Form.setLayout(self.main)
        Form.resize(800, 800)

	self.main_widget.setLayout(self.main)
	Form.setCentralWidget(self.main_widget)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
	self.menu.show()

	self.modifyLabels()
	self.lbWayX.resize(200, 200)



    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))


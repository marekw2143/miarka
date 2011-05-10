import gettext
import os


languageFileName = 'language'
def getLanguage():
	f=open(languageFileName)
	return f.readline().split()[0]

lang_code = getLanguage()
#lang_code = 'en'
localedir = os.path.join(os.getcwd(), 'locales')
t = gettext.translation('messages', localedir, languages=[lang_code])
_ = lambda s: t.gettext(s).decode('utf-8')


class Options(object):
	u""" managing configuration options"""
	def __init__(self):
		self.xRatio, self.yRatio = 0.0, 0.0
		self.readRatio()

	ratioFilename = 'options'

	def readRatio(self):
		u""" reads options from config file"""
		f=open(Options.ratioFilename)
		self.xRatio = float(f.readline())
		self.yRatio = float(f.readline())
		f.close()


	def saveRatio(self):
		u"""saves ratio in the given format:
			xRatio
			yRatio"""
		f=open(Options.ratioFilename,'w')
		f=open('options','w')
		f.write("%s\n" % self.xRatio)
		f.write("%s\n" % self.yRatio)
		f.close()

	def getRatio(self):
		return(self.xRatio, self.yRatio)


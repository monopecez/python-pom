# Import Page class as base of page model
from PageObject.Page import Page
from Utils.CustomUtils import CustomUtils
import logging

class TNC_PP_Page(Page):
	def __init__(self, driver, stringDict = {}, conf = None):
		super().__init__(driver, stringDict, conf)
		
		#Set up CustomUtils for dumping GFX and RAM usage (optional)
		self.utils = CustomUtils(self.driver, self.stringDict, conf)
	
	def setUp(self):
		#Define all elements that will be used in current page/screen/activity
		
		#Define activity of current page/screen/activity
		self.activity_name = '.Settings'
	
		#Define elements that will be used in test process e.g. string check from a textview, click button, check radio button, fill EditText, etc

	
	def start(self):
		self.matchText()
	
    @Page.Test(tcId = "TL-123")
	def matchText(self):
		'''Assert/match text in the page with text in wireframe/dictionary'''
        # do text matching
        # in case of all text are match, result is true
        result = True
		return result #will assign result to test case number TL-123

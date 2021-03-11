# Import Page class as base of page model
from PageObject.Page import WebPage
from Utils.CustomUtils import CustomUtils
import logging
import requests
import subprocess
import json

class Login_Page(WebPage):
	def __init__(self, driver, stringDict = {}, conf = None):
		super().__init__(driver, stringDict, conf)

	def start(self):
		self.openPage()

	@WebPage.Test(tcId = "TL-124")
	def openPage(self):
		#Additional step. add logging. Where we are, what happened, any error, etc
		logging.info("opening %s" % self.conf.BASE_CMS_URL)
		self.driver.get(self.conf.BASE_CMS_URL)
		return True
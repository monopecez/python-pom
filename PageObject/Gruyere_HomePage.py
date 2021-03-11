# Import Page class as base of page model
from PageObject.Page import WebPage
from Utils.CustomUtils import CustomUtils
import logging
import requests
import subprocess
import json

class Gruyere_HomePage(WebPage):
	def __init__(self, driver, stringDict = {}, conf = None):
		super().__init__(driver, stringDict, conf)
		self.menu_left = 'menu-left' 						#id
		self.menu_right = 'menu-right'						#id
		self.h2 = '//h2'									#xpath
		self.content = 'content'							#class name
		self.most_recent_snippets = '//table/tbody/tr/td'	#xpath

	def start(self):
		self.openPage()
		self.checkTitleA()
		self.checkTitleB()
		self.checkPageElements()
		self.checkPageStrings()

	@WebPage.Test(tcId = "TL-124")
	def openPage(self):
		#Additional step. add logging. Where we are, what happened, any error, etc
		logging.info("opening %s" % self.conf.BASE_CMS_URL + self.conf.GRUYERE_ID)
		self.driver.get(self.conf.BASE_CMS_URL + self.conf.GRUYERE_ID)
		return True
		
	@WebPage.Test(tcId = 'TL-125')		
	def checkTitleA(self):
		return self.driver.title == self.stringDict['home-title']
	
	def checkTitleB(self):
		self.assertEqual(self.driver.title, self.stringDict['home-title'], tcid = 'TL-125')
		
	@WebPage.Test(tcId = 'TL-126')
	def checkPageElements(self):
		res = list()
		res.append(self.isElementExist('id', self.menu_left))
		res.append(self.isElementExist('id', self.menu_right))
		res.append(self.isElementExist('xpath', self.h2))
		res.append(self.isElementExist('class name', self.content))
		return all(res)
		
	@WebPage.Test(tcId = 'TL-127')
	def checkPageStrings(self):
		res = list()
		res.append(self.assertEqual(self.stringDict['home'], self.getText('id', self.menu_left)))
		res.append(self.assertEqual(self.stringDict['menu-right'], self.getText('id', self.menu_right)))
		res.append(self.assertEqual(self.stringDict['home-title'], self.getText('xpath', self.h2)))
		res.append(self.assertEqual(self.stringDict['most-recent-snippets'], self.getText('xpath', self.most_recent_snippets)))
		return all(res)
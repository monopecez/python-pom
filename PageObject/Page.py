import logging
import time
import subprocess
import ConfigFile
from Utils.TLConnect import TestLink
import functools

LOGFORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level = logging.INFO, format = LOGFORMAT, handlers=[logging.FileHandler("automation.log"), logging.StreamHandler()])


class Page():
	'''Page class that all page models can inherit from. Abstracted some common elements and basic funtions
	Attributes
	----------
	PACKAGE_NAME: str
		Package name of application under test
	DEVICE_NAME: str
		Device name of device under test
	driver: driver
		Driver that is being used between device under test and appium server
	StringDict: dict
		Collection of translatable string, used to assert text.
	midX: int
		Horizontal center point of device under test screen
	midY: int
		Vertical center point of device under test screen
	n_test_cases: int
		Number of test cases that ran (pass + fail)
	n_test_pass: int
		Number of test cases that ran and pass
	n_test_fail: int
		Number of test cases that ran but fail
	l_test_fail: list
		A list of failed test cases
	tls: TestLink
		TestLink connection, used for result assignment
	conf: configuration object
        Configuration object from config file
    
	Android Common Components/Elements:
	_content: str
		Element name of text content on android dialog box
	_alertTitle: str
		Element name of title on android dialog box
	_mesage: str
		Element name of text content on android dialog box
	_button1:
		Element name of right button on dialog box
	_button2:
		Element name of left button on dialog box
	'''
 
	def __init__(self, driver, stringDict = {}, conf = None):
		"CONFIG"
		if conf == None:
			logging.info("%s Config file is None" % driver.capabilities['deviceName'])
			conf = ConfigFile.Config()

		self._assertionDebug = conf.ASSERTION_DEBUG
		self.PACKAGE_NAME = conf.PACKAGE_NAME
		self.DEVICE_NAME = driver.capabilities['deviceName']
		self.driver = driver
		self.stringDict = stringDict
		self.midX = driver.get_window_size()['width'] // 2
		self.midY = driver.get_window_size()['height'] // 2
		self._content = 'android:id/content'
		self._alertTitle = 'android:id/alertTitle'
		self._message = 'android:id/message'
		self._button1 = 'android:id/button1'
		self._button2 = 'android:id/button2'
		self.webkit_class = 'android.webkit.WebView'
		self.n_test_cases = 0
		self.n_test_pass = 0
		self.n_test_fail = 0
		self.l_test_fail = list()
		self.tls = TestLink(conf.DEVKEY, conf.TESTLINK_URL, str(conf.TESTPLANID), str(conf.BUILDID), str(conf.PLATFORMID), conf.RESULTASSIGNMENT, self.DEVICE_NAME)
		self.conf = conf
		
	def goBack(self, sleep = 0):
		'''		Simulate back button via softkey or hardware button.
		Execute next command immediately if sleep value is not declared.
		Sleep unit is in second.
		'''
		self.driver.back()
		self.wait('time', sleep)
	
	def getText(self, by, name, idx = 0):
		'''Get text by 'by' and name 'name'
		Parameters:
		-----------
		by: str
			Mechanism used to locate elements within a screen/document.
			'id', 'class name', 'name', tag name', 'xpath', 'partial link text'
		name: str
			Name of element to be found
		idx: int (optional, default = 0)
			Return idx-th text if there are multiple elements with same name. Set idx to -1 to return a list of text.

		Example:
		-----------
		getText('id', 'com.samsung.android.rajaampat:id/title')
			get first text from element with id = com.samsung.android.rajaampat:id/title, return in string
		getText('class name', 'android.widget.TextView')
			get first text from element with class name = android.widget.TextView, return in string
		getText('class name', 'android.widget.TextView', -1)
			get all texts that have android.widget.TextView as their class name, return in array
		return empty array [] if not found
		'''
		#IF IDX = -1  then return as array
		if idx == -1:
			return [individualElement.get_attribute('text') for individualElement in self.driver.find_elements(by, name)]
		else:
		#IF IDX != -1, then return single item
		#By default, first item will be returned
			return self.driver.find_elements(by, name)[idx].get_attribute('text')
	
	def getPoint(self, findthis):
		'''- requires tesseract OCR https://opensource.google/projects/tesseract
		- requires tesseract to be runnable from anywhere (add to PATH environment)
		Get (x,y) coordinate of a text. Might get intervered if GPU rendering is on, pointer location is shown, or layout debuggin is on.
		return "Not Found" if not found'''
		screenshot = 'screenshot.png'
		result = 'result'
		self.driver.save_screenshot(screenshot)
		toutput = subprocess.getoutput('tesseract ' + screenshot +' ' + result + ' hocr')
		logging.info("%s getting '%s' using %s" % (self.DEVICE_NAME, findthis, toutput))
		f = open(result + '.html', 'rb')
		f = f.read()
		thetail = f.find(findthis.encode())
		thehead = f[:thetail].rfind('title'.encode())
		bbox = f[thehead+12:thetail-2].split()
		if thetail == -1 or thehead == -1:
			logging.error("%s '%s' is not found" % (self.DEVICE_NAME, findthis))
			return False
		else:
			logging.info("%s '%s' is found" % (self.DEVICE_NAME, findthis))
			midX, midY = int(bbox[0]) + (int(bbox[2]) - int(bbox[0]))//2, int(bbox[1]) + (int(bbox[3]) - int(bbox[1]))//2
			return midX, midY
	
	def wait_for_loading(self):
		'''	Performs wait until spinner, loading, or progress bar is gone
		'''
		while self.driver.find_elements_by_class_name('android.widget.ProgressBar'):
			time.sleep(2)

	def wait(self, type, name):
		'''
		Performs wait, depends on type Supported type: activity, package, time, elemnet type as specified in appium.webdriver.common.mobileby.By
		
		Parameters:
		-----------
		type: str
			wait method: 'activity', 'package', 'time', By
		name: str/int
		
		Example:
		-----------
		wait('activity', activityName)
			wait until activity with activityName is shown
		wait('package', packageName)
			wait until package with packageName is shown
		wait('time', timeInSecond)
			wait for timeInSeconds
		wait(by, elementName)
			wait until element is shown (by id, by class name)
		'''
		if type == 'activity':
			while self.driver.current_activity not in name:
				time.sleep(1)
		elif type == 'package' :
			while self.driver.current_package != name:
				time.sleep(1)
		elif type == 'time':
			time.sleep(name)
		else: 
			while not self.driver.find_elements(type, name):
				time.sleep(1)
	
	def click(self, by, name, sleep=0, idx = None):
		'''Click an element
		
		Parameters:
		-----------
		by: str
			Mechanism used to locate elements within a screen/document.
		name: str
			Name of element to be found and to be clicked
		sleep: int
			Do sleep after element has been clicked. Default is 0, no sleep time
		idx: int
			Click idx-th element if there are multiple elements with same element name. Default is None where first element is going to be clicked
		'''
		try:
			if idx == None:
				self.driver.find_element(by, name).click()
			else:
				self.driver.find_elements(by, name)[idx].click()
			self.wait('time', sleep)
			return True
		except Exception as e:
			logging.error(e)
			return False
		
	def get_yBounds(self, by, name):
		'''Get vertical bound of an element. Return a tuple containing top bound and bottom bound.
		
		Parameters:
		-----------
		by: str
			Mechanism used to locate elements within a screen/document.
		name: str
			Name of element to be found
		'''
		bounds = self.driver.find_element(by, name).get_attribute('bounds')[:-1][1:].split('][')
		top = bounds[0].split(',')[1]
		bottom = bounds[1].split(',')[1]
		return int(top)+1, int(bottom)-1
	
	def get_xBounds(self, by, name):
		'''Get horizontal bound of an element. Return a tuple containing left bound and right bound
		
		Parameters:
		-----------
		by: str
			Mechanism used to locate elements within a screen/document.
		name: str
			Name of element to be found
		'''
		bounds = self.driver.find_element(by, name).get_attribute('bounds')[:-1][1:].split('][')
		left = bounds[0].split(',')[0]
		right = bounds[1].split(',')[0]
		return int(left)+1, int(right)-1
		
	def isElementExist(self, by, name):
		'''To check whether an element is exist. Return True if exist, return False if otherwise
				
		Parameters:
		-----------
		by: str
			Mechanism used to locate elements within a screen/document.
		name: str
			Name of element to be found
		'''
		if self.driver.find_elements(by, name): return True
		else: return False
		
	def swipeLeft(self, y, sleep =1):
		'''Perform a swipe left
		
		Parameters:
		-----------
		y: int
			Where swipe left will be performed
		sleep: int
			Peform wait after swipe has been performed. Default value is 1
		'''
		margin = int(self.midX * 0.2)
		self.driver.flick((self.midX*2)-margin, y, margin, y)
		self.wait('time', sleep)
		
	def swipeRight(self, y, sleep = 1):
		'''Perform a swipe right
		
		Parameters:
		-----------
		y: int
			Where swipe right will be performed
		sleep: int
			Peform wait after swipe has been performed. Default value is 1
		'''
		margin = int(self.midX * 0.2)
		self.driver.flick(margin,y,(self.midX*2)-margin,y)
		self.wait('time', sleep)
		
	def reopen(self, sleep = 0):
		'''Bring application to foreground
		
		Parameter:
		-----------
		sleep: int
			By default, there is no sleep time.
		'''
		self.driver.activate_app(self.PACKAGE_NAME)
		self.wait('time', sleep)

	def assertText(self, item1, item2, tcid='Not_Specified', debug = False):
		self.n_test_cases += 1 
		debug = debug or self._assertionDebug
		if item1 == item2:
			notes = "MATCH!\n\t" + str(item1) + "\n\t" + str(item2)
			result = 'p'
			ret = True
			if debug: logging.info(notes)
			self.n_test_pass += 1
		else:
			notes = "NOT MATCH!\n\t" + str(item1) + "\n\t" + str(item2)
			if debug: logging.info(notes)
			result = 'f'
			ret = False
			self.l_test_fail.append((tcid, str(item1), str(item2)))
			self.n_test_fail += 1
		if tcid != 'Not_Specified' and not debug:
			self.tls.setResult(tcid, result, notes)
		else:
			if debug:
				logging.info("%s result is %s" % (tcid, result))
		return ret
	
	assertEqual = assertText
	
	def assertNotEqual(self, item1, item2, tcid='Not_Specified', debug = False):
		self.n_test_cases += 1 
		debug = debug or self._assertionDebug
		if item1 != item2:
			notes = "NOT EQUAL!\n\t" + str(item1) + "\n\t" + str(item2)
			result = 'p'
			ret = True
			if debug: logging.info(notes)
			self.n_test_pass += 1
		else:
			notes = "EQUAL!\n\t " + str(item1) + "\n\t" + str(item2)
			if debug: logging.info(notes)
			result = 'f'
			ret = False
			self.l_test_fail.append((tcid, str(item1), str(item2)))
			self.n_test_fail += 1
		if tcid != 'Not_Specified' and not debug:
			self.tls.setResult(tcid, result, notes)
		else:
			if debug:
				logging.info("%s result is %s" % (tcid, result))
		return ret
					
	def assertBool(self, item1, tcid='Not_Specified', debug = False, notes = ""):
		self.n_test_cases += 1
		debug = debug or self._assertionDebug
		result = ''
		if debug: logging.info(item1)
		if item1:
			self.n_test_pass += 1
			result = 'p'
			ret = True
		else:
			self.l_test_fail.append((tcid, str(item1)))
			self.n_test_fail += 1
			result = 'f'
			ret = False
		if tcid != 'Not_Specified' and not debug:
			self.tls.setResult(tcid, result, str(item1) + " " + notes)
		else:
			if debug:
				logging.info("%s result is %s" % (tcid, result))
		return ret
			
	def printTC(self):
		logging.info("Total Test : " + str(self.n_test_cases))
		logging.info("Total Pass : " + str(self.n_test_pass))
		logging.info("Total Fail : " + str(self.n_test_fail))
		if self.n_test_fail > 0:
			logging.info("List of failed TC : ")
			for item in self.l_test_fail:
				logging.info(item)
				
	def Test(func=None, *, tcId = None):
		def decorator(func):
			@functools.wraps(func)
			def wrapper(self, *args, **kwargs):
				try:			
					result = func(self, *args, **kwargs)
					if tcId is not None:
						self.assertBool(result, tcId)
					return result
				except Exception as e:
					logging.error(str(e))
					self.assertBool(False, tcId, notes = "ExceptionError")
			return wrapper
		if func:
			return decorator(func)
		return decorator
				
				
				
class WebPage():
	def __init__(self, driver, stringDict = {}, conf = None):
		"CONFIG"
		if conf == None:
			conf = ConfigFile.Config()

		self._assertionDebug = conf.ASSERTION_DEBUG
		self.driver = driver
		self.stringDict = stringDict
		self.n_test_cases = 0
		self.n_test_pass = 0
		self.n_test_fail = 0
		self.l_test_fail = list()
		self.DEVICE_NAME = driver.name
		self.tls = TestLink(conf.DEVKEY, conf.TESTLINK_URL, str(conf.TESTPLANID), str(conf.BUILDID), str(conf.PLATFORMID), conf.RESULTASSIGNMENT, self.DEVICE_NAME)
		self.conf = conf
		
		
	def getText(self, by, name, idx = 0):
		'''Get text by 'by' and name 'name'
		Parameters:
		-----------
		by: str
			Mechanism used to locate elements within a screen/document.
			'id', 'class name', 'name', tag name', 'xpath', 'partial link text'
		name: str
			Name of element to be found
		idx: int (optional, default = 0)
			Return idx-th text if there are multiple elements with same name. Set idx to -1 to return a list of text.

		Example:
		-----------
		getText('id', 'com.samsung.android.rajaampat:id/title')
			get first text from element with id = com.samsung.android.rajaampat:id/title, return in string
		getText('class name', 'android.widget.TextView')
			get first text from element with class name = android.widget.TextView, return in string
		getText('class name', 'android.widget.TextView', -1)
			get all texts that have android.widget.TextView as their class name, return in array
		return empty array [] if not found
		'''
		#IF IDX = -1  then return as array
		if idx == -1:
			return [individualElement.text for individualElement in self.driver.find_elements(by, name)]
		else:
		#IF IDX != -1, then return single item
		#By default, first item will be returned
			return self.driver.find_elements(by, name)[idx].text
			
	def isElementExist(self, by, name):
		'''To check whether an element is exist. Return True if exist, return False if otherwise
				
		Parameters:
		-----------
		by: str
			Mechanism used to locate elements within a screen/document.
		name: str
			Name of element to be found
		'''
		if self.driver.find_elements(by, name): return True
		else: return False
	
	def clear(self, by, name):
		'''To clear a textfield
				
		Parameters:
		-----------
		by: str
			Mechanism used to locate elements within a screen/document.
		name: str
			Name of element to be found
		'''
		try:
			self.driver.find_element(by, name).clear()
		except Exception as e:
			logging.error("Failed to clear %s by %s. %s" % (name, by, e))
		
	def wait(self, type, name):
		'''
		Performs wait, depends on type Supported type: time, element type
		
		Parameters:
		-----------
		type: str
			wait method: 'time', By
		name: str/int
		
		Example:
		-----------
		wait('time', timeInSecond)
			wait for timeInSeconds
		wait(by, elementName)
			wait until element is shown (by id, by class name)
		'''
		if type == 'time':
			time.sleep(name)
		else: 
			while not self.driver.find_elements(type, name):
				time.sleep(1)	
		
	def assertText(self, item1, item2, tcid='Not_Specified', debug = False):
		self.n_test_cases += 1 
		debug = debug or self._assertionDebug
		if item1 == item2:
			notes = "MATCH!\n\t" + str(item1) + "\n\t" + str(item2)
			result = 'p'
			ret = True
			if debug: logging.info(notes)
			self.n_test_pass += 1
		else:
			notes = "NOT MATCH!\n\t" + str(item1) + "\n\t" + str(item2)
			if debug: logging.info(notes)
			result = 'f'
			ret = False
			self.l_test_fail.append((tcid, str(item1), str(item2)))
			self.n_test_fail += 1
		if tcid != 'Not_Specified' and not debug:
			self.tls.setResult(tcid, result, notes)
		else:
			if debug:
				logging.info("%s result is %s" % (tcid, result))
		return ret
			
	assertEqual = assertText
	
	def assertNotEqual(self, item1, item2, tcid='Not_Specified', debug = False):
		self.n_test_cases += 1 
		debug = debug or self._assertionDebug
		if item1 != item2:
			notes = "NOT EQUAL!\n\t" + str(item1) + "\n\t" + str(item2)
			result = 'p'
			ret = True
			if debug: logging.info(notes)
			self.n_test_pass += 1
		else:
			notes = "EQUAL!\n\t " + str(item1) + "\n\t" + str(item2)
			if debug: logging.info(notes)
			result = 'f'
			ret = False
			self.l_test_fail.append((tcid, str(item1), str(item2)))
			self.n_test_fail += 1
		if tcid != 'Not_Specified' and not debug:
			self.tls.setResult(tcid, result, notes)
		else:
			if debug:
				logging.info("%s result is %s" % (tcid, result))
		return ret
					
	def assertBool(self, item1, tcid='Not_Specified', debug = False, notes = ""):
		self.n_test_cases += 1
		debug = debug or self._assertionDebug
		result = ''
		if debug: logging.info(item1)
		if item1:
			self.n_test_pass += 1
			result = 'p'
			ret = True
		else:
			self.l_test_fail.append((tcid, str(item1)))
			self.n_test_fail += 1
			result = 'f'
			ret = False
		if tcid != 'Not_Specified' and not debug:
			self.tls.setResult(tcid, result, str(item1) + " " + notes)
		else:
			if debug:
				logging.info("%s result is %s" % (tcid, result))
		return ret
			
	def printTC(self):
		logging.info("Total Test : " + str(self.n_test_cases))
		logging.info("Total Pass : " + str(self.n_test_pass))
		logging.info("Total Fail : " + str(self.n_test_fail))
		if self.n_test_fail > 0:
			logging.info("List of failed TC : ")
			for item in self.l_test_fail:
				logging.info(item)
				
	def Test(func=None, *, tcId = None):
		def decorator(func):
			@functools.wraps(func)
			def wrapper(self, *args, **kwargs):
				try:			
					result = func(self, *args, **kwargs)
					if tcId is not None:
						self.assertBool(result, tcId)
					return result
				except Exception as e:
					logging.error(str(e))
					self.assertBool(False, tcId, notes = "ExceptionError")
			return wrapper
		if func:
			return decorator(func)
		return decorator
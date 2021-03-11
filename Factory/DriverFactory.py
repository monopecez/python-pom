from appium import webdriver
import ConfigFile
import time
import subprocess
import re
import logging

LOGFORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level = logging.INFO, format = LOGFORMAT, handlers=[logging.FileHandler("automation.log"), logging.StreamHandler()])
#adb.exe shell settings list system

class DriverFactory:
	'''A helper to produce driver'''

	_appPackage = None
	_appActivity = None
	_deviceName = None
	_appLocation = None
	_adbPrefix = ''
	
	def __init__(self):
		pass
		
	def getDriver(self, port = 4723, installAppium = True, resetApp = False, config = ConfigFile.Config()):
		'''Initialize driver and return an initialized driver.
		Parameters:
		port: int, default 4723
			Port number of appium server. Set up another server on another port to run a parallelized test.
			Default value is 4723. 
		installAppium: bool, default True
			Install appium settings on device under test. Set to False IF appium settings has been installed, speed up initialization process
			Default value is True
		resetApp: bool, default False
			Reset application under test, revert to newly installed condition. Same as clear data before launch or fresh install.
			Default value is False
		config: Configuration file
			May be left blank and it will use ConfigFile.Config() file if parameter was left blank'''
	
		try:
			logging.info("Checking for adb.exe executable ...")
			subprocess.getoutput('adb.exe version')
		except:
			logging.info("adb.exe executable is not found on PATH variable")
			logging.info("using supplied adb.exe files inside Utils folder")
			self._adbPrefix = '.\\Utils\\platform-tools\\'
		
		deviceName = config.DEVICE_NAME
		self._appPackage = config.PACKAGE_NAME
		self._appActivity = config.MAIN_ACTIVITY
		
		if not deviceName:
			deviceName = subprocess.getoutput(self._adbPrefix + 'adb.exe devices').splitlines()[1].split('\t')[0]
			_cmd = self._adbPrefix + 'adb.exe shell getprop ro.build.version.release'
		else:
			_cmd = self._adbPrefix + 'adb.exe -s ' + deviceName + ' shell getprop ro.build.version.release'
		
		if self._appPackage == None or self._appActivity == None:
			self._appPackage = 'com.android.settings'
			self._appActivity = '.Settings'
			logging.info("%s either appPackage or appActivity is empty, starting in Android Settings Activity" % deviceName)

		
		_platformVersion = subprocess.getoutput(_cmd)
		self._desired_caps = {
			'platformName': 'Android',
			'platformVersion': _platformVersion,
			'udid': deviceName,
			'deviceName': deviceName,
			'automationName': 'UiAutomator2',
			'skipServerInstallation': 'true',
			'dontStopAppOnReset': 'true',
			'newCommandTimeout': '1200'
			}
		
		if config.APK_LOCATION is not None:
			logging.info("Config.APK_LOCATION is not empty. Overriding any ACTIVITY_NAME or PACKAGE_NAME")
			logging.info("using and installing apk from %s" % config.APK_LOCATION)
			self._appLocation = config.APK_LOCATION
			self._desired_caps['app'] = self._appLocation
		else:
			self._appLocation = None
			self._desired_caps['appPackage'] = self._appPackage
			self._desired_caps['appActivity'] = self._appActivity


		self._desired_caps['autoWebView'] = 'true'
		self._port = port
		self._deviceName = deviceName
		if installAppium:
			self._desired_caps['skipServerInstallation'] = 'false'
		else:
			self._desired_caps['skipServerInstallation'] = 'true'
		logging.info('%s %s' % (deviceName, str(self._desired_caps)))
		logging.info('%s connecting to %s' % (deviceName, deviceName)) 
		self._driver = webdriver.Remote('http://127.0.0.1:' + str(port) + '/wd/hub', desired_capabilities = self._desired_caps, keep_alive =True)
		self._width = self._driver.get_window_size()['width']
		self._height = self._driver.get_window_size()['height']
		self.config = config
		logging.info('%s connected' % deviceName)
		if resetApp: self._driver.reset()
		return self._driver

	def getWebDriver(self, type="chrome"):
		'''Initialize webdriver and return 
		Parameter:
		type: str (optional)
			value: chrome or firefox
			retrun chrome wendriver if value is unspecified'''
			
		from selenium import webdriver
		from selenium.webdriver.common.keys import Keys
		if type == "firefox":
			return webdriver.Firefox()
		else:
			return webdriver.Chrome()

	def regetDriver(self):
		'''Reinitialize driver with previous configuration and return a new driver. Old driver that used in other class will become obsolete
		'''
		return self.getDriver(port = self._port, installAppium = False, config = self.config)
	
	def setAnimation(self, animate):
		'''Set device animation. It is advised to set animation to False when doing automated testing.
		Parameter:
		animate: bool
		'''
		logging.info('%s set animation: %s' % (self._deviceName, animate))
		print('---------------------------------')			
		if animate:
			scale = 1
			print('-------ENABLING	ANIMATION-------')
		else:
			scale = 0
			print('-------DISABLING ANIMATION-------')
		print('---------------------------------')	
		result = 1
		while result ==1 :
			print('--------WINDOW  ANIMATION--------')
			_cmd = self._adbPrefix + 'adb.exe -s ' + self._deviceName + ' shell settings put global window_animation_scale ' + str(scale)
			result = subprocess.run(_cmd.split()).returncode
		result = 1
		while result ==1 :
			print('------TRANSITION	 ANIMATION------')
			_cmd = self._adbPrefix + 'adb.exe -s ' + self._deviceName + ' shell settings put global transition_animation_scale ' + str(scale)
			result = subprocess.run(_cmd.split()).returncode
		result = 1
		while result ==1 :
			print('-------ANIMATOR	DURATION--------')
			_cmd = self._adbPrefix + 'adb.exe -s ' + self._deviceName + ' shell settings put global animator_duration_scale ' + str(scale)
			result = subprocess.run(_cmd.split()).returncode
		print('-------------DONE----------------')
		print('---------------------------------')
	
	def getDeviceLanguage(self):
		'''Get device language. Useful to automatically get stringDictionary'''
		return subprocess.getoutput(self._adbPrefix + 'adb.exe -s ' +  self._deviceName +  ' shell getprop persist.sys.locale').split('-')[0]

	def getDeviceXMLtoTXT(self):
		'''--EXPERIMENTAL UNDERCONSTRUCTION-- 
		Print all texts that found in current screen.'''
		_cmd = self._adbPrefix + 'adb.exe -s ' + self._deviceName + ' shell uiautomator dump'
		subprocess.run(_cmd)
		_cmd = self._adbPrefix + 'adb.exe -s ' + self._deviceName + ' pull /sdcard/window_dump.xml'
		subprocess.run(_cmd)
		_cmd = self._adbPrefix + 'adb.exe -s ' + self._deviceName + ' rm /sdcard/window_dump.xml'

		stringnya = str(open('window_dump.xml','rb').read())
		stringnya = stringnya.replace('\\xe2\\x80\\x99', "'")
		result = [m.start() for m in re.finditer('%s:id/' % self._appPackage, stringnya)]

		elmlist = list()

		for item in result:
			elmlist.append((stringnya[item:item+stringnya[item:].find('"')], stringnya[stringnya[:item].rfind('text="')+6:item-15]))
		
		for item in elmlist:
			text = item[0].split('/')
			print('self.' + text[1] + ' = ' + "'"+ item[0] +"'")
			
	def setLayoutDebugging(self, cond):
		'''Set android layout debugging. Might intervere OCR function.
		Parameter:
		cond: bool'''
		logging.info('%s set layout debugging: %s' % (self._deviceName, cond))
		if cond == True:
			_cmd = self._adbPrefix + 'adb.exe -s ' + self._deviceName + ' shell setprop debug.layout true'
		if cond == False:
			_cmd = self._adbPrefix + 'adb.exe -s ' + self._deviceName + ' shell setprop debug.layout false'
		subprocess.run(_cmd)
		_cmd = self._adbPrefix + 'adb.exe -s ' + self._deviceName + ' shell service call activity 1599295570'
		subprocess.run(_cmd)
		
	def setPointerLocation(self, cond):
		'''Set pointer location. Might intervere OCR function.
		Parameter:
		cond: bool'''
		logging.info('%s show pointer location: %s' % (self._deviceName, cond))
		if cond == True:
			_cmd = self._adbPrefix + 'adb.exe -s ' + self._deviceName + ' shell settings put system pointer_location 1'
		if cond == False:
			_cmd = self._adbPrefix + 'adb.exe -s ' + self._deviceName + ' shell settings put system pointer_location 0'
		subprocess.run(_cmd)
		
	def setProfileGPURendering(self, cond):
		'''Set on screen GPU rendering. Might intervere OCR function.
		Parameter:
		cond: bool'''
		logging.info('%s on screen GPU rendering: %s' % (self._deviceName, cond))
		if cond == True:
			_cmd = self._adbPrefix + 'adb.exe -s ' + self._deviceName + ' shell setprop debug.hwui.profile visual_bars'
		if cond == False:
			_cmd = self._adbPrefix + 'adb.exe -s ' + self._deviceName + ' shell setprop debug.hwui.profile false'
		subprocess.run(_cmd)
		_cmd = self._adbPrefix + 'adb.exe -s ' + self._deviceName + ' shell service call activity 1599295570'
		subprocess.run(_cmd)
		
	def getDeviceName(self):
		return self._deviceName
		
	def getLaunchableActivity(self, packageName):
		'''Get launchable activity name of a package
		Parameter:
		packageName: string
			packageName of the target'''
		output = subprocess.getoutput(self._adbPrefix + 'adb.exe shell "cmd package resolve-activity --brief %s | tail -n 1"' % packageName)
		if '/' in output:
			logging.info("%s Package name: %s" % (self._deviceName, output.split('/')[0]))
			logging.info("%s Launchable activity name: %s" % (self._deviceName, output.split('/')[1]))
		else:
			logging.error("%s Failed to get launchable activity from %s" % (self._deviceName, packageName))
			
	def guessPackage(self):
		'''Get package name, activity name, and launchable activity name from current screen/activity'''
		try:
			currentPackage = self._driver.current_package
			self.getLaunchableActivity(currentPackage)
			logging.info("%s Current activity name: %s" % (self._deviceName, self._driver.current_activity))
		except Exception as e:
			logging.error("%s failed: %s", (self._deviceName, e))
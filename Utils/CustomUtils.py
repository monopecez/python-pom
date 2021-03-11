from PageObject.Page import Page
import os, subprocess
import ConfigFile
import logging

LOGFORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level = logging.INFO, format = LOGFORMAT, handlers=[logging.FileHandler("automation.log"), logging.StreamHandler()])

class CustomUtils(Page):
	"A Class containing custom utility. Need driver to communicate with target device"
	
	def __init__(self, driver ,stringDict = {}, conf = None):
		if conf == None:
			conf = ConfigFile.Config()
		self.conf = conf
		self.PACKAGE_NAME = self.conf.PACKAGE_NAME
		self.DEVICE_NAME = driver.capabilities['deviceName']
	
		self._ramSSCounter = 0
		if 'RAMDUMP' not in os.listdir():
			os.mkdir('RAMDUMP')
			
		self._gfxSSCounter = 0
		if 'GFXDUMP' not in os.listdir():
			os.mkdir('GFXDUMP')
		self.driver = driver
		self.stringDict = stringDict

	def removeSamsungAccount(self):
		"Remove Samsung Account. Will try to remove Samsung Account with a defined password in ConfigFile.py. Tested ok in Android P"
		logging.info("%s starting to remove Samsung Account" % (self.DEVICE_NAME))
		try:
			logging.info("%s opening Samsung Account settings activity" % (self.DEVICE_NAME))
			self.driver.start_activity('com.samsung.android.mobileservice', 'com.samsung.android.samsungaccount.setting.ui.main.SettingMainPreference')

			logging.info("%s clicking overflow menu button" % (self.DEVICE_NAME))
			bds = self.driver.find_element_by_id('com.samsung.android.mobileservice:id/toolbar').get_attribute('bounds')
			bds = bds.split('][')[1].split(',')
			x = int(bds[0]) - 1
			y = int(bds[1][:-1]) - 1
			self.driver.tap([(x,y)])

			logging.info("%s finding remove account menu" % (self.DEVICE_NAME))
			for item in self.driver.find_elements_by_id('com.samsung.android.mobileservice:id/title'):
				if item.get_attribute('text') in ('Remove account', 'Hapus akun'):
					logging.info("%s clicking remove account menu" % (self.DEVICE_NAME))
					item.click()
					break
			self.wait("time", 2)
			logging.info("%s proceed to remove Samsung Account" % (self.DEVICE_NAME))
			self.driver.find_element_by_id('com.samsung.android.mobileservice:id/right_text').click()
			self.wait("time", 2)
			logging.info("%s entering account password: %s" % (self.DEVICE_NAME, self.conf.SAMSUNG_ACCOUNT_PASSWORD))
			self.driver.find_element_by_class_name('android.widget.EditText').set_text(self.conf.SAMSUNG_ACCOUNT_PASSWORD)
			logging.info("%s proceed to remove Samsung Account" % (self.DEVICE_NAME))			
			self.driver.find_element_by_id('com.samsung.android.mobileservice:id/right_text').click()
			self.wait_for_loading()
			self.wait_for_loading()
			self.wait("time", 5)
			return True
		except Exception as e:
			logging.error("%s failed to remove samsung account" % self.DEVICE_NAME)
			logging.error("%s %s" % (self.DEVICE_NAME, e))
			return False
			
	def dumpRAM(self, filename, deviceName = None, packageName = None):
		"""Dump RAM usage of application under test. Stored into a file with .RAM extension
		Parameters:
		-----------
		filename: str (mandatory)
			Output file of RAM dump with .RAM extension. File is stored under RAMDUMP folder
		deviceName: str (optional)
			Optional. Will get from ConfigFile if not defined
		packageName: str (optional)
			Optional. Will get from ConfigFile if not defined
		"""
		if deviceName == None: deviceName = self.DEVICE_NAME
		if packageName == None: packageName = self.PACKAGE_NAME
		logging.info("%s dumping RAM to %s" % (deviceName, filename))
		self._ramSSCounter += 1
		#cmd = 'adb -s ' + deviceName + ' shell dumpsys meminfo %s | grep -w "TOTAL" | grep -v ":"' % packageName
		cmd = 'adb -s ' + deviceName + ' shell dumpsys meminfo %s' % packageName
		with open('.\\RAMDUMP\\' + deviceName + '-' +str(self._ramSSCounter) + '-' + filename + '.ram', 'w') as outfile:
			subprocess.call(cmd, stdout=outfile)
	
	def dumpGFX(self, filename, deviceName = None, packageName = None):
		"""Dump GFX info of application under test. Stored into a file with .GFX extension
		Parameters:
		-----------
		filename: str (mandatory)
			Output file of GFX info dump with .GFX extension. File is stored under GFXDUMP folder
		deviceName: str (optional)
			Optional. Will get from ConfigFile if not defined
		packageName: str (optional)
			Optional. Will get from ConfigFile if not defined
		"""

		if deviceName == None: deviceName = self.DEVICE_NAME
		if packageName == None: packageName = self.PACKAGE_NAME
		logging.info("%s dumping GFX to %s" % (deviceName, filename))
		self._gfxSSCounter += 1
		cmd = 'adb -s ' + deviceName + ' shell dumpsys gfxinfo %s' % packageName
		with open('.\\GFXDUMP\\' + deviceName + '-' +str(self._gfxSSCounter) + '-' + filename + '.gfx', 'w') as outfile:
			subprocess.call(cmd, stdout=outfile)

	def dumpGFXRAM(self, filename, deviceName = None, packageName = None):
		"""Dump RAM usage and GFX info of application under test.
		Parameters:
		-----------
		filename: str (mandatory)
			Output file of RAM dump with .RAM extension and GFX info dump with .GFX extension. Stored in respective folder
		deviceName: str (optional)
			Optional. Will get from ConfigFile if not defined
		packageName: str (optional)
			Optional. Will get from ConfigFile if not defined
		"""

		if deviceName == None: deviceName = self.DEVICE_NAME
		if packageName == None: packageName = self.PACKAGE_NAME
		logging.info("%s saving screenshot to %s" % (deviceName, filename + '.png'))
		self.driver.save_screenshot('.\\GFXDUMP\\' + deviceName + '-' + str(self._gfxSSCounter) + '-' + filename + '.png')
		self.dumpRAM(filename, deviceName, packageName)
		self.dumpGFX(filename, deviceName, packageName)
		
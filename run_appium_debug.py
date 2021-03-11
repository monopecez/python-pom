# start appium server via command line
# appium -p 4723 --default-capabilities "{\"fullReset\":\"false\", \"noReset\":\"true\", \"newCommandTimeout\":1200}
# appium -p 4723 --default-capabilities "{\"newCommandTimeout\":1200}

# run this script with -i
# e.g. ipython -i run_appium_debug.py
from Factory.DriverFactory import DriverFactory
from ConfigFile import Config
from StringDict import StringDict
import Factory.PageFactory
import logging

driverObj = DriverFactory()
configObj = Config()
configObj.MAIN_ACTIVITY = None
configObj.PACKAGE_NAME = None
configObj.APK_LOCATION = None

driver = driverObj.getDriver(installAppium = True, resetApp = False, config = configObj)

driverObj.setAnimation(False)

stringDict = StringDict().getStringDict(driverObj.getDeviceLanguage())
testObj = Factory.PageFactory.getPageObject("Page", driver, stringDict, configObj)

# Run this command to get package name, launchable activity, of application under test
driverObj.guessPackage()

# Run this cp,,amd to get testlink IDs
testObj.tls.getIDS()
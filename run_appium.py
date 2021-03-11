# start appium server via command line
# appium -p 4723 --default-capabilities "{\"fullReset\":\"false\", \"noReset\":\"true\", \"newCommandTimeout\":1200}
# appium -p 4723 --default-capabilities "{\"newCommandTimeout\":1200}
from Factory.DriverFactory import DriverFactory
from ConfigFile import Config
from StringDict import StringDict
import Factory.PageFactory
import logging

driverObj = DriverFactory()
configObj = Config()

# set installAppium to True for first time or appium server has not been installed on device
# installAppium can be set to False if appium server has been installed (minimizing prepartion time)
driver = driverObj.getDriver(installAppium = True, resetApp = False, config = configObj)

#Set animation to False.
driverObj.setAnimation(False)

stringDict = StringDict().getStringDict(driverObj.getDeviceLanguage())

'''#OPTIONAL
driverObj.setLayoutDebugging(False)
driverObj.setPointerLocation(True)
driverObj.setProfileGPURendering(False)
'''

testObj = Factory.PageFactory.getPageObject("TNC_PP_Page", driver, stringDict, configObj)
testObj.setUp()
testObj.start()
testObj.printTC()
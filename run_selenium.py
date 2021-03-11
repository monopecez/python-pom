from Factory.DriverFactory import DriverFactory
from StringDict import StringDict
from ConfigFile import Config
import Factory.PageFactory
import logging

#Driver factory instantiation
driverObj = DriverFactory()

#Config object instantiation
configObj = Config()

#Getting webdriver of chromedriver. change to "firefox" for firefox driver
webdriver = driverObj.getWebDriver("chrome")

#Getting string dictionary for string test data
stringDict = StringDict().getStringDict()

#If you wish to hardcode your test data  (not recommended),
#stringDict = {}

#Getting test Object
testObj = Factory.PageFactory.getPageObject("Gruyere_HomePage", webdriver, stringDict, configObj)
#supplied different test data
#testObj.conf.CMS_USERNAME = "another_user"
#testObj.conf.CMS_PASSWORD = "an0Th3R_p4$$w0Rd"
#starting test
testObj.start()

# appium-python

## Project Description 

This repository contains a set of files as a base for creating appium automation or selenium automation with python programming language.

## Requirements and Prerequisites

* [Python version 3.x](https://www.python.org/downloads/)

* [Appium-Python-Client](https://pypi.org/project/Appium-Python-Client/) package for python

* [Selenium](https://pypi.org/project/selenium/) package for python

* [requests](https://pypi.org/project/requests/) package for python

 Use the package manager [pip](https://pip.pypa.io/en/stable/) to install both packages.

```bash
pip install Appium-Python-Client selenium requests
```

* [adb.exe](https://developer.android.com/studio/releases/platform-tools) that can be called from anywhere ([added to PATH environment variable](https://lifehacker.com/the-easiest-way-to-install-androids-adb-and-fastboot-to-1586992378))
  * Can be checked by opening command prompt and type adb

## Files Description

### ConfigFile.py
A Class used to store configuration and can be used to store user defined variable for a cleaner code. This class is used in DriverFactory.py, Page.py, CustomUtils.py, and TLConnect.py
* Factory/DriverFactory.py consumes DEVICE_NAME, PACKAGE_NAME, and MAIN_ACTIVITY
* Page.py consumes PACKAGE_NAME
* Utils/CustomUtils.py consumes SAMSUNG_ACCOUNT_EMAIIL and SAMSUNG_ACCOUNT_PASSWORD for Samsung Account Removal method
* Utils/TLConnect.py consumes DEVKEY, TESTLINK_URL, PROJECTID, TESTPLANID, BUILDID, PLATFORMID, and RESULTASSIGNMENT. 

### Factory/DriverFactory.py
A helper class to produce appium mobile driver and selenium webdriver. Also, it contains method to adjust target the device, e.g. setAnimation, setLayoutDebugging, setPointerLocation

### Factory/PageFactory.py
A factory that produces test objects for the test scrpt

### PageObject/Page.py
A base for creating test cases. There are two classes, Page class and WebPage class
  * Page class used as a base for appium test script with some basic functions
  * WebPage class used as a base for selenium test script.

### StringDict.py
This class is to be filled with strings on the application. Support multiple language: english and indonesian.

### Utils/CustomUtils.py
A Class containing custom utility to extend base functionality. Some of defined custom utility are dumpGFX, dumpRAM


### run_selenium.py or run_appium.py
The main test script

## Further reading

https://wonderproxy.com/blog/page-object-models-in-python/

https://blog.testproject.io/2019/07/16/develop-page-object-selenium-tests-using-python/

https://qxf2.com/blog/page-object-model-selenium-python/



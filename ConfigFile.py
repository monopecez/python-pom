class Config():
	"""A Class used to store configuration. This class is used in DriverFactory.py, Page.py, CustomUtils.py, and TLSRIN.py
	DriverFactory.py consumes DEVICE_NAME, PACKAGE_NAME, and MAIN_ACTIVITY
	Page.py consumes PACKAGE_NAME
	CustomUtils.py consumes SAMSUNG_ACCOUNT_EMAIIL and SAMSUNG_ACCOUNT_PASSWORD for Samsung Account Removal
	
	Attributes
	----------
	DEVICE_NAME: str or None
		Device that will be used as test device. Set to None to use any available connected device
	
	PACKAGE_NAME: str or None
		Package name that will be used as application under test. Set to None to start in Android Settings Activity
	
	MAIN_ACTIVITY: str or None
		Activity name as application entry point. Consult with dev or inspect manifest.xml. Set to None to start in Android Settings Activity
	
	APK_LOCATION: str or None
		Absolute path to an android application installation file (apk) e.g. "D:\some\folder\application.apk"
		If APK_LOCATION is filled, PACKAGE_NAME and MAIN_ACTIVITY will be overridden.
	
	SAMSUNG_ACCOUNT_EMAIL: str
	
	SAMSUNG_ACCOUNT_PASSWORD: str
	
	"""

	
	def __init__(self):
		self.DEVICE_NAME = None # fill with None to find device automatically via adb devices and uses any available devices 
		self.PACKAGE_NAME = 'com.google.settings' # fill with None to open Android Settings Activity/screen
		self.MAIN_ACTIVITY = '.Settings' # fill with None to open Android Settings Activity/screen
		self.APK_LOCATION = None # 'absoule path to apk file'
		self.SAMSUNG_ACCOUNT_EMAIL = 'some_email@ema.il'
		self.SAMSUNG_ACCOUNT_PASSWORD = 'pa$$w@rd12'
		
		"""Below items are custom config to be used in test"""
		self.BASE_CMS_URL = "https://google-gruyere.appspot.com/"
		self.GRUYERE_ID = "363795474723627721643350876590119895176"
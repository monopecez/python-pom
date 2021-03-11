import requests
import testlink
import re
import logging
from ConfigFile import Config
#######################################
#######################################

LOGFORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level = logging.INFO, format = LOGFORMAT, handlers=[logging.FileHandler("automation.log"), logging.StreamHandler()])

class TestLink():
	'''A helper for creating TestLink connection and result assignment
	
	Attributes:
	-----------
	
	devKey: str
		TestLink personal API key
	testplanid: int
		Test plan ID of test plan under test
	buildid: int
		Build ID of build under test
	platformid: int
		Platform ID of platform under test
	assign: bool
		Assign result to TestLink. Default is False. Set to True to enable result assignment
	deviceName: str
		Device name. For logging purpose
	'''
	
	
	
	def __init__(self,devKey, url = "", testplanid = None, buildid = None, platformid = None, assign = False, deviceName = None):
		'''Initializate TestLink class
		
		Parameters:
		-----------
		devKey: str
			TestLink personal API key
		testplanid: int
			Test plan ID of test plan under test
		buildid: int
			Build ID of build under test
		platformid: int
			Platform ID of platform under test
		assign: bool
			Assign result to TestLink. Default is False. Set to True to enable result assignment
		deviceName: str
			Device name. For logging purpose
		'''
		self.tlurl = url
		self.devKey = devKey
		self.testplanid = testplanid
		self.buildid = buildid
		self.platformid = platformid
		self.assign = assign
		self.initted = False
		self.deviceName = deviceName
		try:
			self.tls = testlink.TestlinkAPIGeneric(self.tlurl, self.devKey, verbose = False)
			self.tls.checkDevKey()
			self.initted = True
			logging.info("%s Testlink dev key is valid" % deviceName)
		except Exception as e:
			logging.error("%s Invalid testlink configuration: %s" % (deviceName, e))
			self.initted = False
			
	def _isInit(self):
		'''Private method. Check whether connection to TestLink server has been initialized'''
		try:
			self.tls.checkDevKey()
			self.initted = True
			return True
		except:
			self.initted = False
			return False
			
	def _keyisempty(self):
		'''Private method. Check whether devKey or IDs are empty'''
		return (self.devKey == None or self.testplanid == None or self.buildid == None or self.platformid == None or self.tls == None)
	
	def printParams(self):
		'''Print current TestLink connection parameters
		will print devKey, testplanid, buildid, platformid, connector status'''
		print("devKey    \t= " + str(self.devKey))
		print("testplanid\t= " + str(self.testplanid))
		#try:
		#	print('\t%s' % "to be filled with human-friendly testplan name")
		print("buildid   \t= " + str(self.buildid))
		#try:
		#	print('\t%s' % "to be filled with human-friendly build name")
		print("platformid\t= " + str(self.platformid))
		#try:
		#	print('\t%s' % "to be filled with human-friendly platform name")
		print("\tTestlink connector Status = ", end='')
		try:
			self.tls.checkDevKey()
			print("Initialized")
		except:
			print("Not Initialized")
	
	def populateTestSuite(self, testplan, detailed = True):
		'''Populate test suite in a test plan
		'''
		testSuiteDict = dict()
		temp = dict()
		print("POPULATING TEST SUITE... " + str(testplan))
		testSuite = self.tls.getTestSuitesForTestPlan(testplan)
		for item in testSuite:
			if (detailed):            
				try:
					temp[item['id']] = self.tls.getTestSuiteByID(item['parent_id'])['name'] + ' - ' + item['name']
				except:
					temp[item['id']] = item['name']
			else:
				temp[item['id']] = item['name']
		else:
			testSuiteDict.update(temp)
		return {k:v for k,v in sorted(testSuiteDict.items(), key =lambda item: item[1])}
	
	def getIDS(self, assignIDResult=False):
		'''Get IDs of a test plan, build, amn platform. These IDs are important and will be used for result assignment.
		
		Parameter:
		----------
		assignIDResult: bool
			Assign returned ID to its respective attributes
		'''
		if self._isInit():
			'''Get testplanid, buildid, and platformid
			Will assign id automatically if assignIDResult=True
			'''
			print("-"*20)
			print("FETCHING PROJECT IDs")
			print("-"*20)
			result = self.tls.getProjects()

			print("Here are the project IDs")
			print("ProjectID| ProjectName")
			for item in result:
				print(item["id"] + "\t : " + item["name"])

			print("Next step: Getting testplan ID")
			projectID = input("Please input your project ID: ") #180678

			print("\n\n")
			print("-"*20)
			print("FETCHING TESTPLAN IDs")
			print("-"*20)

			result = self.tls.getProjectTestPlans(projectID)
			list2 = list()
			for item in result:
				list2.append((item['id'], item['name']))

			list2 = sorted(list2)
			list2.reverse()
			print('testPlanID| testPlanName')
			for item in list2:
				print(item[0] + '\t\t : ' + item[1])
				
			testplanID = input("Please input testplanID: ")
			print("\n\n")
			print("-"*20)
			print("FETCHING Build IDs")
			print("-"*20)

			result = self.tls.getBuildsForTestPlan(testplanID)
			print('buildID\t | buildName')
			for item in result:
				print(item['id'] + '\t : ' + item['name'])

			buildID = input("Please input buildID: ")

			print("\n\n")
			print("-"*20)
			print("FETCHING platform IDs")
			print("-"*20)

			result = self.tls.getProjectPlatforms(projectID)
			print('platformID | platformName')
			for key in result.keys():
				print(result[key]['id'] + '\t : ' + result[key]['name'])

			platformID = input("Please input platform ID of API: ")

			print("-"*20)
			print("\n\nHERE ARE THE IDs")
			print("ProjectID\t: "+ projectID)
			print("TestplanID\t: "+ testplanID)
			print("BuildID\t\t: " + buildID)
			print("PlatformID\t: "+ platformID)
			
			if assignIDResult:
				self.testplanid = testplanID
				self.buildid = buildID
				self.platformid = platformID
		else:
			print("Incorrect devkey, please assign a correct devKey first.")
			
	def setResult(self, tcId, status, notes = ''):
		'''Set and report the result of test execution
		
		Parameters:
		-----------
		
		tcId: str
			Full external test case ID = Project + Test Case Number. Example: 'QA-Auto-2372'
		status: str
			'f' for fail, 'p' for passed, 'b' for blocked, 'x' for not available
		notes: str
			Optional. Additional execution notes.
		'''
		if self.assign:
			if self._keyisempty():
				if not self.initted: print("Incorrect devkey, please assign a correct devKey first.\n")
				print("ID(s) are not initialized")
				self.printParams()
				print("\nIf you want to get ID, you can call getIDS() method")
				print("or use getIDS(assignIDResult=True) to assign IDs")
			else:
				try:
					self.tls.reportTCResult(self.testplanid, status, testcaseexternalid=tcId, buildid=self.buildid, platformid=self.platformid, notes=notes)
					logging.info("%s Result assigned to %s with status %s" % (self.deviceName, tcId, status))
				except Exception as e:
					logging.error("%s Error while submitting result: %s" % (self.deviceName, str(e)))
		else:
			logging.info("%s %s : %s - Result is not assigned. Init class with assign = True to assign the result" % (self.deviceName, tcId, status))
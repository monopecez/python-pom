class StringDict:
	'''This class contains strings for application. Support multiple language: english and indonesian.
	'''
	
	def __init__(self):
		self.stri = dict()
		self.stre = dict()
		self._populate()
		
	def addString(self, kwd, string1, string2 = None):
		'''Add string to transalation dictionary. String can be added in this class (via source code under _populate() method) or can be added on the fly (on the test script)
		
		Parameters:
		-----------
		kwd: str
			Keyword of a string to be stored
		string1: str
			If application supports multiple language, string1 is a string in Bahasa Indonesia. If application only supports one language, string1 can be in any language.
		string2: str
			If application supports multiple language, string2 is a string in Bahasa Inggris.
			If application only supports one language, string2 can be omitted or fill with None.
		
		Example:
		-----------
		addString(keywords, string in indonesian, string in english)
		addString('continue','LANJUTKAN','CONTINUE')
		'''
		self.stri[kwd] = string1
		if string2 == None:
			self.stre[kwd] = string1
		else:
			self.stre[kwd] = string2
		
	def getStringDict(self, lang = 'en'):
		'''	Return dictionary of string.
		Parameter:
		----------
		lang: str
			Value 'id' or 'en'
		note: English will be used if not specified or value is incorrect
		'''
		if lang == 'id':
			self.addString('_language', lang, lang)
			return self.stri
		else:
			self.addString('_language', lang, lang)
			return self.stre
		
	def _populate(self):
		'''A collection of predefined string. String can be defined here in source code.'''
		#TNC_PP_Page
		self.addString('home', 'Home')
		self.addString('menu-right', 'Sign in | Sign up')
		self.addString('sign-in', 'Sign in')
		self.addString('sign-up', 'Sign up')
		self.addString('home-title', 'Gruyere: Home')
		self.addString('most-recent-snippets', 'Most recent snippets:')
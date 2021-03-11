def getPageObject(page_name, driver, stringDict, conf = None):
	"Return the appropriate page object based on page_name"
	test_obj = None
	if page_name == "TNC_PP_Page":
		from PageObject.TNC_PP_Page import TNC_PP_Page
		test_obj = TNC_PP_Page(driver, stringDict, conf)
	elif page_name == "Page":
		from PageObject.Page import Page
		test_obj = Page(driver, stringDict, conf)
	elif page_name == "Gruyere_HomePage":
		from PageObject.Gruyere_HomePage import Gruyere_HomePage
		test_obj = Gruyere_HomePage(driver, stringDict, conf)
	return test_obj
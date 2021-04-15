from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
	
	def test_cannot_add_empty_list_items(self):
		self.fail('Add!')




















































# No need to use that anymore as from now on will be using Django test runner for FTs.
# if __name__ == "__main__":
# 	unittest.main()

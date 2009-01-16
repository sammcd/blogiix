import unittest
from django.test.client import Client

#############################################################################################
# Commenting Test Cases
#############################################################################################
#
# What I want to test:
#
# - Comments with valid information (but possibly invalid through not having enough fields)
# 		- Name Email Address
#		- 000 - Invalid
#		- 001 - Invalid
#		- 010 - Invalid
#		- 011 - Invalid
#		- 100 - Invalid
#		- 101 - Invalid
#		- 110 - Valid
#		- 111 - Valid
#
# - Comment test that is spam
#		- Proper result page displayed
#		- Comment not seen on post page.
# 
# - For successful comments
# 		- Check that appropriate result page is displayed
#		- Check that comment is properly put on post page
# 
# - Comments should not be placed on any post except for the one that it is tied to
#
#############################################################################################


class ValidComment000(unittest.TestCase):
	def setUp(self):
		


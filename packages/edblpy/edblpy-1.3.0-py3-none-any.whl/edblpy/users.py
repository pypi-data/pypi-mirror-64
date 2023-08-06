# Importing required modules
from requests import get
endpoint = 'https://www.edbl.xyz/api/user/{}'

# Defining the IdNotGiven exception
class IdNotGiven(Exception):
	pass

# The user class
class User:
	def __init__(self,id:int=None):
		self.id = id
	def get_info(self):
		if self.id == None:
			raise IdNotGiven('User id must be given in the class params')
		return get(endpoint.format(self.id)).json()

# Example
"""
jake = User(480407581085532180)
print(jake.get_info())
"""
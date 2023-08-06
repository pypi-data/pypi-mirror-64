# Importing required modules
from requests import get
endpoint = 'https://www.edbl.xyz/api/{}'

# Defining the IdNotGiven exception
class IdNotGiven(Exception):
	pass

# The bot class
class Bot:
	def __init__(self, id:int=None , token:str=None):
		self.id = id
		self.token = token
	def get_info(self):
		if self.id == None:
			raise IdNotGiven('Bot id must be given in the class params')
		return get(endpoint.format(f"bots/{self.id}")).json()
# Example
"""
mika = Bot(631669116926820353)
print(mika.get_info())
"""

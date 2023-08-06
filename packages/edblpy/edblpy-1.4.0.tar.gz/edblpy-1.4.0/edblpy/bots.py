# Importing required modules
from requests import get , post
endpoint = 'https://www.edbl.xyz/api/{}'

# Defining the needed exceptions
class IdNotGiven(Exception):
	pass

class TokenNotGiven(Exception):
	pass

class InvalidParam(Exception):
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
	def post_status(self , user_count:int=None , server_count:int=None):
		if self.token == None:
			raise TokenNotGiven('User token must be given in the class params to use this method')
		if user_count==None or server_count==None:
			raise InvalidParam('User count or/and server count is required to post status')
		return post(url=endpoint.format("postStatus"),json={'token' : self.token , 'serversCount' : server_count , 'usersCount' : user_count}).json()
# Example
"""
mika = Bot(631669116926820353)
print(mika.get_info())
"""

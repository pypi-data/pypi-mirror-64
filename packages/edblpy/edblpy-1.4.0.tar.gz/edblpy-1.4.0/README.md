
# Edblpy
<div align="center">
<a href="https://travis-ci.org/will-rowe/banner"><img src="https://travis-ci.org/will-rowe/banner.svg?branch=master" alt="travis"></a>
<a href='http://hulk.readthedocs.io/en/latest/?badge=latest'><img src='https://readthedocs.org/projects/hulk/badge/?version=latest' alt='Documentation Status' /></a>
<a href="https://github.com/will-rowe/banner/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License"></a>
</div>
Edblpy is an unofficial python module utilizing the electro discord bot list [api](https://www.edbl.xyz/api) . Easy to use and well documented!

# Getting started

- You must have ython 3*
- A bot's / user's id
- Install the module using pip : `pip install edblpy`
- Import what you need : `from edblpy import Bot` or `from edblpy import User`
- View more about usage in the docs section

# Docs

## Class : Bot

### Params ( name , description , type , default )
**id** : **The bot's id (Required when retrieving info)** : **integer** : `None`
**token** : **Your token  (Required when posting the bot's status)** : **string** : `None`
### Methods ( name , description , params , returns)
**get_info** : **Gets the bot's info** : `None` : `Dict`
**post_status** : **Posts the server/user count to the DB , requires auth** : `user_count , server_count` : `Dict`
## Class : User

### Params ( name , description , type , default )
**id** : **The user's id (Required)** : **integer** : `None`
### Methods ( name , description , params , returns)
**get_info** : **Gets the user's info** : `None` : `Dict`


# Examples
Getting a user's info
```py
from edblpy import User
jake = User(480407581085532180)
print(jake.get_info())
```
Getting a bot's info
```py
from edblpy import Bot
mika = Bot(631669116926820353)
print(mika.get_info())
```
Posting a bot's status
```py
from edblpy import Bot
mika = Bot(631669116926820353 , 'YOUR_SUPER_SECRET_TOKEN')
print(mika.post_status(user_count=100 , server_count=100)) # you should probably make the counts dynamic
```


# Edblpy

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
**id** : **The bot's id (Required)** : **integer** : `None`
### Methods ( name , description , params , returns)
**get_info** : **Gets the bot's info** : `None` : `Dict`

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
from edblpy import User
mika = Bot(631669116926820353)
print(mika.get_info())
```

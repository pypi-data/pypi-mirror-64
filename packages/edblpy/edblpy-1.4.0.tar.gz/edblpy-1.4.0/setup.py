import setuptools
from distutils.core import setup
with open("README.md", "r") as rm:
  long_description = rm.read()
setup(
  name = 'edblpy',        
  packages = ['edblpy'],   
  version = '1.4.0',   
  license='MIT', 
  description = 'A simple and easy-to-use unofficial python wrapper around the Electro discord bot list api',   
  long_description= long_description,
  long_description_content_type='text/markdown',
  author = 'Jake', 
  author_email = 'jstyle07072004@gmail.com', 
  url = 'https://github.com/Jakeisbored/edblpy',  
  download_url = 'https://github.com/Jakeisbored/edblpy',
  keywords = ['edbl', 'discord', 'botlist'],   
  install_requires=[
          'requests'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',  
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',     
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
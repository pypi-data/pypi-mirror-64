from setuptools import setup

setup(name='pycov',
      version='1.0',
      description='A library getting how many people are now ill with coronavirus',
      packages=['pycov'],
      author_email='kewldanil1@gmail.com',
      zip_safe=False,
	  install_requires=[
	  "requsts",
	  "lxml",
	  "bs4"
	  ]
)
from setuptools import setup

setup(name='pycov',
      version='1.2',
      description='A library getting how many people are now ill with coronavirus',
      packages=['pycov'],
      author_email='kewldanil1@gmail.com',
	author="kewldan",
	url="https://pypi.org/project/pycov/",
      zip_safe=False,
	python_requires= ">=3.6.0",
	install_requires=[
	  "requsts",
	  "lxml",
	  "bs4"
	  ]
)
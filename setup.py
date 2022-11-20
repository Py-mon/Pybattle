from setuptools import *



setup(
	name='PyBattle',
	version='0.1',
	packages=find_packages(),
	description='Game packages installation.',
	install_requires=[
		'colorama',
		'numpy',
	]
	# scripts=[''] # Will need to add this for game running script
)
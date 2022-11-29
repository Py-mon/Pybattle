from setuptools import setup, find_packages


setup(
    name='Pybattle',
    version='0.1',
    packages=find_packages(),
    description='Game packages installation.',
    author='Jacob Ophoven',
    python_requires='>=3.11',
    install_requires=[
                'colorama',
                'numpy',
                'keyboard'
    ]
    # scripts=[''] # Will need to add this for game running script
)

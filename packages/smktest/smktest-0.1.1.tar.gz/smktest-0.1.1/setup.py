from setuptools import setup, find_packages
from distutils.core import setup

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()


setup(
  name = 'smktest',
  packages = ['smktest'], # this must be the same as the name above
  version = '0.1.1',
  description = 'This package offers a series of tests to create the correct Smoke Test of an application before uploading changes to production.',
  author = 'Cecilio Cannavacciuolo Diaz',
  author_email = 'cecilio.cannav@gmail.com',
  url = 'https://github.com/cecilio-cannav/smktest.git', # use the URL to the github repo
  license='MIT',
  keywords = ['smoketest', 'testing', 'python', 'smart',],
  python_requires='>=3',
)

#setup(name='smktest',
#      version='0.1',
#      description='Easy way to make markdown code for tables',
#      url='https://github.com/cecilio-cannav/smktest.git',
#      author='cecilio cannavacciuolo diaz',
#      author_email='cecilio.cannav@gmail.com',
#      license='MIT',
#      packages=['smktest'],
#      )


install_requires = [
    'subprocess',
    'requests',
    'pytest',
    'pyhttptest',
]


#!/usr/bin/env python

from setuptools import setup

setup(name='tap-platformpurple',
      version='0.0.1',
      description='Singer.io tap for extracting data from the LogMeIn Rescue API',
      author='Fishtown Analytics',
      url='http://fishtownanalytics.com',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['tap_platformpurple'],
      install_requires=[
          'tap-framework==0.0.4',
          'pytz',
      ],
      entry_points='''
          [console_scripts]
          tap-platformpurple=tap_platformpurple:main
      ''',
      packages=['tap_platformpurple'])

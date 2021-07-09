#!/usr/bin/python3
from setuptools import setup

setup(name='jeopardy_sync',
      version='1.1',
      description='Reddit scraper to find and download Jeopardy! episodes.',
      url='https://github.com/batteryshark/jeopardy_sync',
      author='BatteryShark',
      author_email='batteryshark@outlook.com',
      license='MIT',
      packages=['jeopardy_sync'],
      install_requires=[
          'requests','google-api-python-client','oauth2client'
      ],
      scripts=['bin/jsync_scrape'],
      zip_safe=False)
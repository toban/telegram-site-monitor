from telegram import Update
import logging
from telegram.ext import CommandHandler, Updater
import time
import sys
from config import Setup
import os

from bot import Bot
import selenium
from selenium import webdriver
import time
import requests
import os
from PIL import Image
import traceback
import io
import hashlib
# This is the path I use
#DRIVER_PATH = '/Users/anand/Desktop/chromedriver'
# Put the path for your ChromeDriver here
from selenium.webdriver.chrome.options import Options
from screenshot_diff_comparator import ScreenshotDiffComparator
#filename=Setup.config['logfile']
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

bot = Bot(Setup.config['manager_bot'])
logger = logging.getLogger('Main')
sleep_seconds = 60*60
wait_for_element_seconds = 1

while True:

	chrome_options = Options()
	chrome_options.add_argument("--headless")
	wd = webdriver.Remote('http://localhost:4444/wd/hub', webdriver.DesiredCapabilities.CHROME)
	wd.set_window_size(1280, 1024)
	diffComparator = ScreenshotDiffComparator(bot, wd)
	
	for sitename in Setup.config['sites']:
		site = Setup.config['sites'][sitename]
		logger.info("getting: " + sitename)
		try:
			wd.get(Setup.config['sites'][sitename]['url'])
			time.sleep(wait_for_element_seconds)
			site['step'](wd, bot)
		except:
			e = sys.exc_info()[0]
			logger.error(e)
			logger.error(traceback.format_exc())

		if site['takePicture']:
			diffComparator.takePicture
	
	wd.quit()

	logger.info("sleeping %s seconds" % sleep_seconds)
	time.sleep(sleep_seconds)



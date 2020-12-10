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
import io
import hashlib
# This is the path I use
#DRIVER_PATH = '/Users/anand/Desktop/chromedriver'
# Put the path for your ChromeDriver here
from selenium.webdriver.chrome.options import Options

logging.basicConfig(filename=Setup.config['logfile'], format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)



bot = Bot(Setup.config['manager_bot'])
logger = logging.getLogger('Main')
sleep_seconds = 60*60
wait_for_element_seconds = 10
sitename = 'kmplx'

while True:
	#if manager.prefix_message:
	#	manager.getPrefixMessages()
	#else:
	#try:
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	wd = webdriver.Remote('http://localhost:4444/wd/hub', webdriver.DesiredCapabilities.CHROME)
	wd.set_window_size(1280, 1024)
	
	for sitename in Setup.config['sites']:
		logger.info("getting: " + sitename)
		try:
			wd.get(Setup.config['sites'][sitename]['url'])
			time.sleep(wait_for_element_seconds)
			Setup.config['sites'][sitename]['step'](wd)
		except:
			e = sys.exc_info()[0]
			logger.error(e)
			logger.error(sys.exc_info()[2])
		prefix = "screenshot-%s" % sitename
		filename = prefix
		compare = False

		if os.path.isfile('/tmp/' + filename + '.png'):
			compare = True
			filename += "-1"

		fullPath = '/tmp/' + filename + '.png'

		wd.save_screenshot(fullPath)
		logger.info('writing: ' + fullPath)

		if compare is True:
			command = "diff /tmp/screenshot-{0}.png /tmp/screenshot-{0}-1.png".format(sitename)
			logger.info("running: " + command)
			code = os.system(command)
			logger.info("diff exited with: %s" % code)
			if code != 0:
				bot.dispatcher.bot.sendPhoto(Setup.config['chat_id'], photo=open(fullPath, 'rb'))
				os.system('rm /tmp/screensho-%s*.png' % sitename)
				bot.talk("diff exit: %s" %  code)
	
	wd.quit()

	logger.info("sleeping %s seconds" % sleep_seconds)
	time.sleep(sleep_seconds)



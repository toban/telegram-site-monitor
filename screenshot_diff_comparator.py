from telegram import Update
import logging
import telegram
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters, CallbackContext
import time
import sys
from config import Setup
import os

class ScreenshotDiffComparator:

	def __init__(self, bot, webdriver):

		self.bot = bot
		self.webdriver = webdriver
		self.logger = logging.getLogger('Camera')
		self.compare = False

	def takePicture():
		self.logger.info("Update")
		try:
			prefix = "screenshot-%s" % sitename
			filename = prefix

			if os.path.isfile('/tmp/' + filename + '.png'):
				self.compare = True
				filename += "-1"

			fullPath = '/tmp/' + filename + '.png'

			wd.save_screenshot(fullPath)
			logger.info('writing: ' + fullPath)

			if self.compare is True:
				command = "diff /tmp/screenshot-{0}.png /tmp/screenshot-{0}-1.png".format(sitename)
				logger.info("running: " + command)
				code = os.system(command)
				logger.info("diff exited with: %s" % code)
				if code != 0:
					bot.dispatcher.bot.sendPhoto(Setup.config['chat_id'], photo=open(fullPath, 'rb'))
					os.system('rm /tmp/screensho-%s*.png' % sitename)
					bot.talk("diff exit: %s" %  code)
		except: # catch all
			e = sys.exc_info()[0]
			self.logger.error(e)
			raise e

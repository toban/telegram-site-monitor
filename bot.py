from telegram import Update
import logging
import telegram
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters, CallbackContext
import time
import sys
from config import Setup
import os

## todo telegram.vendor.ptb_urllib3.urllib3.exceptions.ReadTimeoutError:
## todo telegram.error.BadRequest: Message must be non-empty

class Bot:

	def __init__(self, token ):

		self.updater = Updater(token=token, use_context=True)
		self.dispatcher = self.updater.dispatcher
		self.logger = logging.getLogger('Bot')
		self.logger.info("starting bot!")

	def talk(self, message, reply_message=None):
		self.logger.info(message)
		try:
			if reply_message is not None:
				self.dispatcher.bot.send_message(chat_id=Setup.config['chat_id'], text=message)#, reply_to_message_id=reply_message.message_id)
			else:
				self.dispatcher.bot.send_message(chat_id=Setup.config['chat_id'], text=message, disable_notification=True)
		except telegram.error.TimedOut:
			self.logger.error("timeout!")
			time.sleep(10)
		except: # catch all
			e = sys.exc_info()[0]
			self.logger.error(e)
			raise e

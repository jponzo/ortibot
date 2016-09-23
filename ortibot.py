#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Example Bot to show some of the functionality of the library
# This program is dedicated to the public domain under the CC0 license.
import json
import sys
import random
import yaml
import func as f

with open("ortibot.yaml", 'r') as stream:
    try:
        config = yaml.load(stream)
	print "[CONFIG]: %s" % config
    except yaml.YAMLError as exc:
        print("ERROR: " + exc)

TOKEN = config['token']

from telegram.ext import Updater
from telegram.ext.dispatcher import run_async
from telegram import ChatAction
from time import sleep
import logging
import os

# Enable Logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)
handler = logging.FileHandler("/var/log/opsbot.log")  
logger.addHandler(handler)

# We use this var to save the last chat id, so we can reply to it
last_chat_id = 0

def any_message(bot, update):
    # Save last chat_id to use in reply handler
    global last_chat_id
    last_chat_id = update.message.chat_id
    sender_name = f.normalize_string(update.message.from_user['first_name'])

    bot.sendChatAction(update.message.chat_id, action=ChatAction.TYPING)

    # If Audio Message
    try:
        file_id = update.message.voice['file_id']
        logger.info("New audio message\nFrom: %s\nchat_id: %d\nText: %s Audio: %s" %
                    (update.message.from_user,
                     update.message.chat_id,
                     update.message.text, file_id))
        # Download Audio Message 
        newFile = bot.getFile(file_id)
        newFile.download('message.ogg')
        # Convert Ogg to Wav
        os.system('/usr/bin/opusdec message.ogg message.wav')
        message = f.SpeechToText('message.wav')
        logger.info("Speech Recognition: %s" % message)

    # If Text Message 
    except:
        logger.info("New text message\nFrom: %s\nchat_id: %d\nText: %s" %
                    (update.message.from_user,
                     update.message.chat_id,
                     update.message.text))
        message = update.message.text

    logger.info("[%s]: %s" % (sender_name, message))
 
    resp_string = ""
    resp = ['cerra el orto %s' % sender_name,'que boludo sos %s' % sender_name,'mierrrda vas a comer','%s, no te quiere ni el halcon de Velazquez' % sender_name, "siempre el mismo lame escrotos vos eh...", "ahh buee, labura cualquiera en Meli...", 'cerra el orto %s' % sender_name]
    if "max" in message.lower():
    	resp_string = "God bless Max Tkach our savior"
    elif "sarg" in message.lower():
        resp_string = "El gordo vaca debe estar en Wendys"
    elif "pochi" in message.lower():
        resp_string = "Pochi, necesito unos mocasines talle 46 en color caqui"
    elif "cusa" in message.lower() or "juan" in sender_name.lower():
        resp_string = "Cerra el orto, Cusa. Sos de Platense" 
    #elif "trolli" in message.lower() or "agustin" in sender_name.lower():
    #    resp_string = "Che Agus, acabo de ver un bora igualito al tuyo abajo del 60. Donde lo estacionaste?"
    #    bot.sendPhoto(update.message.chat_id, photo="http://sintinta.com.ar/wp-content/uploads/2012/12/bora-chocado-en-av-cabrera1.jpg")
    elif "beto" in message.lower() or "betun" in sender_name.lower():
        resp_string = "ufff! todos con el culo contra la pared que llego Alberto"
    elif "pablo" in sender_name.lower():
        resp_string = "Gordo, no te hace caso ni el boludo de tu bot"
    else:
    	#resp_string = random.choice(resp)
	pass
    logger.info("[ortibot]: %s" % resp_string)

    bot.sendMessage(update.message.chat_id, text=resp_string)

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN, workers=10)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # This is how we add handlers for Telegram messages
    ## Regex handlers will receive all updates on which their regex matches
    dp.addTelegramRegexHandler('.*', any_message)

    # Start the Bot and store the update Queue, so we can insert updates
    update_queue = updater.start_polling(poll_interval=0.01, timeout=5)

if __name__ == '__main__':
    main()

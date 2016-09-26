#!/usr/bin/env python
# -*- coding: utf-8 -*-

## ORTIBOT v1.0. 

import json
import sys
import random
import yaml
import func as f
from telegram.ext import Updater
from telegram.ext.dispatcher import run_async
from telegram import ChatAction
from time import sleep
import logging
import os
from modules.tu_vieja import TuVieja

# Enable Logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)
handler = logging.FileHandler("/var/log/ortibot.log")
logger.addHandler(handler)

# Load config file
with open("ortibot.yaml", 'r') as stream:
    try:
        config = yaml.load(stream)
        logger.info("[CONFIG]: %s" % config)
        TOKEN = config['token']
        WEATHERID = config['weatherid']
    except yaml.YAMLError as exc:
        logger.error(exc)
        sys.exit()

# Load messages
with open("messages.yaml", 'r') as stream:
    try:
        messages = yaml.load(stream)
        logger.info("[MESSAGES]: %s" % messages)
        BORA = messages['bora']
    except yaml.YAMLError as exc:
        logger.error(exc)

# We use this var to save the last chat id, so we can reply to it
last_chat_id = 0

ortibot = TuVieja()

def any_message(bot, update):
    # Save last chat_id to use in reply handler
    global last_chat_id
    last_chat_id = update.message.chat_id
    sender_name = f.normalize_string(update.message.from_user['first_name'])
    logger.debug("New message: %s" % update.message)

    # Audio Message
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

    # Text Message 
    except:
        logger.debug("New text message\nFrom: %s\nchat_id: %d\nText: %s" %
                    (update.message.from_user,
                     update.message.chat_id,
                     update.message.text))
        message = update.message.text
        msg = message.lower()

    logger.info("[%s]: %s" % (sender_name, message))

    # Think
    if "trolli" in msg:
        resp_string = "Trolli este es tuyo??"
        image=random.choice(BORA)
        bot.sendPhoto(update.message.chat_id, photo=str(image))
    elif "clima" in msg:
        city = msg.split(" en ")[1].split("?")[0]
        resp_string = f.getWeather(WEATHERID, city)
    elif "quien es" in msg or "que es" in msg:
        querystring = msg.split(" es ")[1].split("?")[0]
        resp_string = f.wikipedear(querystring)
    elif "calmate" in msg:
        mood = ortibot.setMood("calmado")
        logger.info("Cambiando a modo %s" % mood)
        resp_string = ortibot.puteada(sender_name)
    elif "boludo" in msg:
        mood = ortibot.setMood("messages")
        logger.info("Cambiando a modo %s" % mood)
        resp_string = ortibot.puteada(sender_name)
    else:
        resp_string = ortibot.puteada(sender_name)

    # Reply
    lista=[1,'bashton']
    if random.choice(lista) == 'bashton' or "clima" in msg or "ortibot" in msg:
      bot.sendChatAction(update.message.chat_id, action=ChatAction.TYPING)
      bot.sendMessage(update.message.chat_id, text=resp_string)
      logger.info("[ortibot]: %s" % resp_string)
    else:
      logger.info("[ortibot]: A este gil ni le contesto")

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


#!/usr/bin/env python
# -*- coding: utf-8 -*-

## ORTIBOT v1.0. 

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
WEATHERID = config['weatherid']

from telegram.ext import Updater
from telegram.ext.dispatcher import run_async
from telegram import ChatAction
from time import sleep
import logging
import os


# My custom modules
from modules.tu_vieja import TuVieja

# Enable Logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)
handler = logging.FileHandler("/var/log/ortibot.log")  
logger.addHandler(handler)

# We use this var to save the last chat id, so we can reply to it
last_chat_id = 0

def any_message(bot, update):
    # Save last chat_id to use in reply handler
    global last_chat_id
    last_chat_id = update.message.chat_id
    sender_name = f.normalize_string(update.message.from_user['first_name'])
    logger.info("New message: %s" % update.message)

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

    # TODO: Remove all if statements and replace them with this class:
    #resp = TuVieja().puteada(sender_name)
 
    resp_string = ""
    resp = ['cerra el orto %s' % sender_name,'que boludo sos %s' % sender_name,'mierrrda vas a comer','%s, no te quiere ni el halcon de Velazquez' % sender_name, "siempre el mismo lame escrotos vos eh...", "ahh buee, labura cualquiera en Meli...", 'cerra el orto %s' % sender_name]
    if "max" in message.lower():
        resp_string = "God bless Max Tkach our savior"
    if "sarg" in message.lower():
        resp_string = "El gordo vaca debe estar en Wendys"
    if "pochi" in message.lower():
        resp_string = "Pochi, necesito unos mocasines talle 46 en color caqui"
    if "cusa" in message.lower() or "juan" in sender_name.lower():
        resp_string = "Cerra el orto, Cusa. Sos de Platense"
    if "trolli" in message.lower() or "agustin" in sender_name.lower():
        resp_string = "Trolli este es tuyo??"
        bora_images=['http://img.ar.autos.cozot.com/pics/ar/2015/08/22/Vw-bora-chocado-el-la-trompa-General-Roca-20150822215257.jpg', 'http://imganuncios.mitula.net/vendo_volkswagen_bora_1_8t_full_con_cuero_2011_5520130462999686988.jpg', 'http://i.ebayimg.com/00/s/NjAwWDgwMA==/z/9doAAOSw3mpXOJqo/$_20.jpg', 'http://www.diariohuarpe.com/wp-content/uploads/2014/05/Pol-AutoChocadoBoraHilux-27052014-640x375.jpg', 'http://www.noticiaspv.com/wp-content/uploads/2012/04/20120407_valle_2593.jpg']
        image=random.choice(bora_images)
        bot.sendPhoto(update.message.chat_id, photo=str(image))
    if "beto" in message.lower() or "betun" in sender_name.lower():
        resp_string = "ufff! todos con el culo contra la pared que llego Alberto"
    if "pablo" in sender_name.lower():
        resp_string = "Gordo, no te hace caso ni el boludo de tu bot"
    if "dario" in sender_name.lower():
        resp_string = "no le hagan caso a ese pibe, tiene mas rivo encima que el loco Ventus"
    if "jew" in message.lower():
        resp_string = "Solo los Jewvengers pueden salvarnos"
    if "clima" in message.lower():
        city = message.lower().split(" en ")[1].split("?")[0]
        resp_string = f.getWeather(WEATHERID, city)
    else:
        resp_string = (random.choice(resp))

    logger.info("[ortibot]: %s" % resp_string)

    lista=[1,2,'bashton']
    if random.choice(lista) == 'bashton' or "clima" in message.lower():
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


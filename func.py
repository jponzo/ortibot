#!/usr/bin/pypy
# -*- coding: utf-8 -*-
import unicodedata
import time
import os

def normalize_string(mystring):
        mystring.encode("utf-8")
        text = unicodedata.normalize("NFKD", mystring)
        clean_text = text.encode("ascii", "ignore")
        return clean_text

def SpeechToText(filename):
	#!/usr/bin/env python3
	import speech_recognition as sr
	from os import path

	WAV_FILE = path.join(path.dirname(path.realpath(__file__)), filename)
	r = sr.Recognizer()
	with sr.WavFile(WAV_FILE) as source:
	    audio = r.record(source) # read the entire WAV file
        

	# recognize speech using Google Speech Recognition
	try:
	    # for testing purposes, we're just using the default API key
	    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
	    # instead of `r.recognize_google(audio)`
	    recognized_word = normalize_string(r.recognize_google(audio, language = "es-US"))
	    print("Google Speech Recognition thinks you said: " + recognized_word)
	    return recognized_word
	except sr.UnknownValueError:
	    caca = "Google Speech Recognition could not understand audio"
            return caca
	except sr.RequestError as e:
	    caca = "Could not request results from Google Speech Recognition service; {0}".format(e)
            return caca

def Text2Speech(text):
	from gtts import gTTS
	tts = gTTS(text=text, lang="es-us")
	tts.save('mostro_response.mp3')

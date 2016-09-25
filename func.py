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

def wikipedear(target):
    result = "No tengo idea"
    try:
        wikipedia.set_lang("es")
        result = wikipedia.summary(target, sentences=1, auto_suggest=True, redirect=True)
        print "Wikipedia result is: %s" % result
    except Exception as e:
        print "Error trying to search in wikipedia: %s" % e
    return result

def getWeather(id, city):
        from urllib2 import urlopen
        import simplejson
        app_id = id
        request = simplejson.load(urlopen('http://api.openweathermap.org/data/2.5/weather?q=%s&units=metric&APPID=%s&lang=es' % (city, app_id)))
        opinion = ""
        description = request['weather'][0]['description']
        temperature = str(request['main']['temp']).split(".")[0]
        temp_max = str(request['main']['temp_max']).split(".")[0]
        humidity = str(request['main']['humidity'])
        if int(humidity) > 80:
                opinion = opinion + "Terrible la humedad que hay!"
        if int(temperature) < 15:
                opinion = opinion + "Abrigate que hace frio"
        response = "El estado del clima de hoy. %s. Ahora hace %s grados de temperatura y puede llegar a %s grados durante la tarde. La humedad es del %s porciento. %s" % (description, temperature, temp_max, humidity, opinion)
        return response

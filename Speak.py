import pyttsx3
from gtts import gTTS
import playsound as ps
import random
import os
from resources.interactions import *

class Speak:
    def __init__(self, reader = "google") -> None:
        self.reader = f"{reader}_speak"
        self.interactions = interactions
        
        ## pyttsx3 config
        if reader == "pyttsx3":
            self.engine = pyttsx3.init()
            self.voices = self.engine.getProperty('voices')
            self.engine.setProperty('voice', self.voices[0].id)
            self.engine.setProperty('rate', 158)
        
    def text_to_speech(self, text):
        self.__getattribute__(self.reader)(text)
    
    def interact(self, type):
            self.__getattribute__(self.reader)((random.choice(self.interactions[type])))
            
    ## read text with pyttsx3
    def pyttsx3_speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
        
    ## read text with google api
    def google_speak(self, text):
        tts = gTTS(text=text, lang='en',  tld='co.in')
        filename = 'temp/voice.mp3'
        tts.save(filename)
        ps.playsound(filename)
        os.remove(filename)
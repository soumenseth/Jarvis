from platform import platform
import speech_recognition as sr
import sounddevice as sd
import os
import wavio
from resources.interactions import *
from Speak import Speak
from utils import *
from sys import platform

class Jarvis:
    def __init__(self, fps=44100, duration=4) -> None:
        self.fps = fps
        self.duration = duration
        self.audio_filepath = "temp/output.wav"
        self.spoken_texts_filepath = "data/spoken_texts.json"
        self.spoken_texts = self.get_spoken_texts(self.spoken_texts_filepath)
        self.speak = Speak()
        self.platform = platform
        self.scripts_dir = "scripts"
        
    def run(self):
        self.speak.interact("greetings")
        self.record_audio()
        text = self.recognize_audio()
        while text == "":
            self.speak.text_to_speech("Buddy, you there?")
            self.record_audio()
            text = self.recognize_audio()
        self.store_spoken_text(text)
        if self.check_command(text):
            self.run_command(text)
        self.remove_audiofile()
        self.speak.interact("job_done")
        
    def check_command(self, text):
        '''
        check if the spoken text is a command or normal interaction line
        '''
        return True
    
    def run_command(self, text):
        print(text)
        if check_common(["terminal", "power shell", "powershell"], text.lower().split()):
            self.speak.text_to_speech("Opening the terminal. Please wait a second.")
            os.system(open_terminal(self.platform))
    
    def record_audio(self):
        self.speak.interact("seek_command")
        print("Recognizing.....")
        
        recording = sd.rec(self.duration*self.fps, samplerate=self.fps, channels=2)
        sd.wait()
        print("Done!")
        wavio.write(self.audio_filepath, recording, self.fps, sampwidth=2)
        
    def recognize_audio(self):
        rec = sr.Recognizer()
        with sr.AudioFile(self.audio_filepath) as source:
            audio = rec.record(source)
            print("file reading")
            
        try:
            text = rec.recognize_google(audio)
            self.speak.text_to_speech("So your want to:")
            self.speak.text_to_speech(text)
            return text
        except Exception as e:
            print(e)
            return ""
        
    def remove_audiofile(self):
        os.remove(self.audio_filepath)
    
    def give_voice(self, text, type):
        self.speak(text, type)
        
    def get_spoken_texts(self, spoken_texts_filepath):
        return read_json(spoken_texts_filepath) if os.path.exists(spoken_texts_filepath) else []
    
    def store_spoken_text(self, text):
        self.spoken_texts.append(text)
        write_json(self.spoken_texts_filepath, self.spoken_texts)
        
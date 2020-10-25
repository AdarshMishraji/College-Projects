import pyttsx3
import datetime
import speech_recognition


engine = pyttsx3.init()
voices = engine.getProperty('voices')

def speak(string):
    engine.say(string)
    engine.runAndWait()

def initialGreetings():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Hello,Good Morning")
        print("Hello,Good Morning")
    elif hour>=12 and hour<18:
        speak("Hello,Good Afternoon")
        print("Hello,Good Afternoon")
    else:
        speak("Hello,Good Evening")
        print("Hello,Good Evening")

def takeUserSpeech():

    userSpeech = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as audio_source:
        userSpeech.adjust_for_ambient_noise(audio_source)
        speak("I'am Listening")
        print("I'am Listening...")
        userSpeech.pause_threshold = 1
        audio = userSpeech.listen(audio_source, phrase_time_limit = 4)

        try:
            userSpeech = userSpeech.recognize_google(audio, language = 'en-in')
            print(userSpeech)
        except Exception:
            speak("Pardon me, please say that again")
            return
    return userSpeech

engine.setProperty('rate', 150)

import pyttsx3  # for text to speech
import speech_recognition # for speech recognition.


engine = pyttsx3.init()
voices = engine.getProperty('voices')

# convert string to voice. (Text-to-Speech)
def speak(string): 
    engine.say(string)
    engine.runAndWait()

# takes user speech and convert it to string (Speech-to-Text)
def takeUserSpeech(): 
    userSpeech = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as audio_source:
        userSpeech.adjust_for_ambient_noise(audio_source)
        speak("I'am Listening")
        print("I'am Listening...")
        userSpeech.pause_threshold = 2
        audio = userSpeech.listen(audio_source, phrase_time_limit = 4)

        try:
            userSpeech = userSpeech.recognize_google(audio, language = 'en-in')
            print(userSpeech)
        except Exception:
            speak("Pardon me, please say that again")
            return
    return userSpeech

engine.setProperty('rate', 125)

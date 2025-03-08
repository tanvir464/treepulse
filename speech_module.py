import speech_recognition as sr
from gtts import gTTS
import os
from playsound import playsound

def speech_to_text(language="en-US"):
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    # Use the microphone as source for input.
    with sr.Microphone() as source:
        print(f"Please speak in {language}...")
        audio = recognizer.listen(source)
    
    try:
        # Recognize speech using Google's online API.
        text = recognizer.recognize_google(audio, language=language)
        print(f"Recognized text ({language}): {text}")
    except sr.UnknownValueError:
        print("Could not understand the audio.")
    except sr.RequestError as e:
        print(f"Request error from Google Speech Recognition service: {e}")

def speak(text, lang='en'):
    # Create the TTS object (default voice is generally female)
    tts = gTTS(text=text, lang=lang, slow=False)
    
    # Save the audio to a temporary file
    filename = "temp.mp3"
    tts.save(filename)
    
    # Play the audio file
    playsound(filename)
    
    # Remove the temporary file
    os.remove(filename)

if __name__ == '__main__':
    # Test the speech-to-text function
    speech_to_text(language="bn-BD")
    
    # Test the text-to-speech function
    speak(" আমার নাম তানভীর আহমেদ", lang='bn')
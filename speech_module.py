import speech_recognition as sr
from gtts import gTTS
import os
import pygame

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
    """
    Convert text to speech and play it using pygame instead of playsound
    """
    try:
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Generate speech
        tts = gTTS(text=text, lang=lang)
        
        # Save to temporary file
        temp_file = "temp_audio.mp3"
        tts.save(temp_file)
        
        # Load and play the audio
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()
        
        # Wait for the audio to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        # Cleanup
        pygame.mixer.quit()
        
        # Remove temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)
            
    except Exception as e:
        print(f"Error in speech playback: {str(e)}")
        # Continue without audio if there's an error
        pass

if __name__ == '__main__':
    # Test the speech-to-text function
    speech_to_text(language="bn-BD")
    
    # Test the text-to-speech function
    speak(" আমার নাম তানভীর আহমেদ", lang='bn')
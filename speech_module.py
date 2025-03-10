import speech_recognition as sr
from gtts import gTTS
import os
import pygame
import time

def speech_to_text(language="en-US"):
    """Convert speech to text using Google's speech recognition API."""
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    # Use the microphone as source for input.
    with sr.Microphone() as source:
        print(f"Please speak in {language}...")
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        # Recognize speech using Google's online API.
        text = recognizer.recognize_google(audio, language=language)
        print(f"Recognized text ({language}): {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Request error from Google Speech Recognition service: {e}")
        return None

def listen_for_speech(timeout=5, language="en-US"):
    """Listen for speech with a timeout."""
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    # Use the microphone as source for input.
    with sr.Microphone() as source:
        print(f"Listening in {language}... (speak now)")
        
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)
        
        try:
            # Set timeout for listening
            audio = recognizer.listen(source, timeout=timeout)
            
            # Recognize speech using Google's online API
            text = recognizer.recognize_google(audio, language=language)
            print(f"Recognized: {text}")
            return text
        except sr.WaitTimeoutError:
            print("No speech detected within timeout period.")
            return None
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Request error from Google Speech Recognition service: {e}")
            return None
        except Exception as e:
            print(f"Error during speech recognition: {e}")
            return None

def speak(text, lang='en'):
    """
    Convert text to speech and play it using pygame.
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
            
        # Add a small pause after speech
        time.sleep(0.5)
            
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
    # Test the functions
    speak("Please say something in English or Bangla", lang='en')
    user_input = listen_for_speech()
    if user_input:
        speak(f"You said: {user_input}", lang='en')
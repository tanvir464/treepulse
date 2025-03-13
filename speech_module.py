import speech_recognition as sr
from gtts import gTTS
import os
import pygame
import time

def listen_for_speech(timeout=5, language="en-US"):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print(f"Listening in {language}... (speak now)")

        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=timeout)

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
    try:
        pygame.mixer.init()
        
        tts = gTTS(text=text, lang=lang)

        temp_file = "temp_audio.mp3"
        tts.save(temp_file)

        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        time.sleep(0.5)

        pygame.mixer.quit()

        if os.path.exists(temp_file):
            os.remove(temp_file)
            
    except Exception as e:
        print(f"Error in speech playback: {str(e)}")
        pass

if __name__ == '__main__':
    speak("Please say something in English or Bangla", lang='en')
    user_input = listen_for_speech()
    if user_input:
        speak(f"You said: {user_input}", lang='en')
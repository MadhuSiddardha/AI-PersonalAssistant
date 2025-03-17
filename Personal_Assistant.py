import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import sys
import requests
from bs4 import BeautifulSoup
import nltk

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)

def engine_talk(text):
    """Function to convert text to speech."""
    print(f"Assistant: {text}")  # Display the response
    engine.say(text)
    engine.runAndWait()

def user_commands():
    """Function to recognize user voice commands with improved accuracy."""
    recognizer = sr.Recognizer()
    command = ""
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Reduce background noise
            print("Listening...")
            voice = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(voice).lower()
            print(f"User: {command}")  # Display the recognized command
    except sr.WaitTimeoutError:
        engine_talk("I did not hear anything. Please try again.")
    except sr.UnknownValueError:
        engine_talk("Sorry, I could not understand the command.")
    except Exception as e:
        print(f"Error: {str(e)}")
        engine_talk("An error occurred while recognizing your speech.")
    return command

def fetch_information_online(query):
    """Fetches search results from Google."""
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    result_snippets = [g.get_text() for g in soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd') if g.get_text()]
    
    return result_snippets[0] if result_snippets else "Sorry, I couldn't find any relevant information."

def process_query(query):
    """Processes user query and fetches information online."""
    result = fetch_information_online(query)
    print(f"Online result: {result}")
    engine_talk(result)

def run_assistant():
    """Main function to run the voice assistant and respond to every input."""
    while True:
        command = user_commands()
        if not command:
            continue
        
        if 'play' in command:
            song = command.replace('play', '').strip()
            engine_talk(f'Playing {song}')
            pywhatkit.playonyt(song)
        elif 'time' in command:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            engine_talk(f'The current time is {current_time}')
        elif 'who is' in command:
            name = command.replace('who is', '').strip()
            info = wikipedia.summary(name, 1)
            print(info)
            engine_talk(info)
        elif 'joke' in command:
            joke = pyjokes.get_joke()
            print(joke)
            engine_talk(joke)
        elif 'search' in command or 'what is' in command or 'how to' in command:
            process_query(command)
        elif 'stop' in command or 'exit' in command:
            engine_talk("Goodbye!")
            sys.exit()
        else:
            engine_talk(f"You said: {command}")  # Ensure every input gets a response

if __name__ == "__main__":
    engine_talk("Hello! I am your Assistant. How can I assist you today?")
    run_assistant()

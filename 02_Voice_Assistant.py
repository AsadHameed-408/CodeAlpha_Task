import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import pyjokes
import datetime
import webbrowser
import os
import subprocess
import requests
from time import sleep


class VoiceAssistant:
    def __init__(self):
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()

        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()

        # Get available voices
        self.voices = self.engine.getProperty('voices')

        # Set voice (0 for male, 1 for female)
        self.engine.setProperty('voice', self.voices[1].id)

        # Set speech rate (words per minute)
        self.engine.setProperty('rate', 150)

        # Set wake word (what you say to activate the assistant)
        self.wake_word = "jarvis"

    def speak(self, text):
        """Convert text to speech"""
        self.engine.say(text)  # Queue the text to be spoken
        self.engine.runAndWait()  # Make it speak

    def take_command(self):
        """Listen for voice commands using microphone"""
        try:
            with sr.Microphone() as source:  # Use microphone as audio source
                print("Listening...")
                audio = self.recognizer.listen(source)  # Listen to microphone
                command = self.recognizer.recognize_google(audio)  # Convert speech to text
                command = command.lower()  # Convert to lowercase for easier processing

                # Check if wake word was said
                if self.wake_word in command:
                    command = command.replace(self.wake_word, '')  # Remove wake word
                    print("Command:", command)
                    return command
                else:
                    return None

        except sr.UnknownValueError:
            print("Sorry, I didn't get that.")
            return None
        except sr.RequestError:
            print("Sorry, my speech service is down.")
            return None
        except Exception as e:
            print("An error occurred:", e)
            return None

    def run(self):
        """Main loop for the voice assistant"""
        self.speak(f"Hello! I'm {self.wake_word.capitalize()}. How can I help you today?")

        while True:  # Infinite loop to keep listening
            command = self.take_command()
            

            if command:  # If we got a command
                # PLAY MUSIC
                if 'play' in command:
                    song = command.replace('play', '')  # Extract song name
                    self.speak(f"Playing {song}")
                    pywhatkit.playonyt(song)  # Play on YouTube

                # TELL TIME
                elif 'time' in command:
                    current_time = datetime.datetime.now().strftime('%I:%M %p')
                    self.speak(f"The current time is {current_time}")

                # WIKIPEDIA SEARCH
                elif 'search' in command or 'who is' in command or 'what is' in command:
                    query = command.replace('search', '').replace('who is', '').replace('what is', '')
                    info = wikipedia.summary(query, sentences=2)  # Get short summary
                    self.speak(info)

                # TELL A JOKE
                elif 'joke' in command:
                    joke = pyjokes.get_joke()
                    self.speak(joke)

                # OPEN APPLICATIONS
                elif 'open' in command:
                    app = command.replace('open', '').strip()
                    if 'chrome' in app:
                        self.speak("Opening Google Chrome")
                        os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
                    elif 'notepad' in app:
                        self.speak("Opening Notepad")
                        subprocess.Popen(['notepad.exe'])
                    else:
                        self.speak(f"Opening {app}")
                        webbrowser.open(f"https://www.{app}.com")

                # WEATHER REPORT
                elif 'weather' in command:
                    self.speak("Please tell me the city name")
                    city = self.take_command()
                    if city:
                        # You would need to get an API key from openweathermap.org
                        api_key = "YOUR_API_KEY"
                        base_url = "http://api.openweathermap.org/data/2.5/weather?"
                        complete_url = f"{base_url}appid={api_key}&q={city}"
                        response = requests.get(complete_url)
                        data = response.json()

                        if data["cod"] != "404":
                            main = data["main"]
                            temperature = main["temp"] - 273.15  # Convert Kelvin to Celsius
                            humidity = main["humidity"]
                            weather_desc = data["weather"][0]["description"]
                            self.speak(f"Weather in {city}: Temperature {temperature:.1f} degrees Celsius, "
                                       f"{weather_desc}, Humidity {humidity}%")
                        else:
                            self.speak("City not found")

                # EXIT THE ASSISTANT
                elif 'exit' in command or 'quit' in command or 'goodbye' in command:
                    self.speak("Goodbye! Have a great day.")
                    break

                # UNKNOWN COMMAND
                else:
                    self.speak("I didn't understand that command. Can you please repeat?")

            sleep(1)  # Small delay between commands


if __name__ == "__main__":
    assistant = VoiceAssistant()  # Create an instance
    assistant.run()  # Start the assistant
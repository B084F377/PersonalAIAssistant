import datetime
import webbrowser
import os
import random
import requests
import speech_recognition as sr
import pyttsx3
import time
import threading
import smtplib
from twilio.rest import Client as TwilioClient
from qhue import Bridge
from wolframalpha import Client as WolframAlphaClient
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from PyDictionary import PyDictionary
from forex_python.converter import CurrencyRates
import requests

# Insert your API Keys here
API_KEY_WEATHER = "your_openweathermap_api_key"
API_KEY_NEWS = "your_newsapi_api_key"
API_KEY_WOLFRAMALPHA = "your_wolframalpha_api_key"
TWILIO_SID = "your_twilio_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_PHONE_NUMBER = "your_twilio_phone_number"
TO_PHONE_NUMBER = "recipient_phone_number"
EMAIL_ADDRESS = "your_email_address"
EMAIL_PASSWORD = "your_email_password"
TO_EMAIL_ADDRESS = "recipient_email_address"
HUE_BRIDGE_IP = "your_hue_bridge_ip"
HUE_USERNAME = "your_hue_username"
TRELLO_API_KEY = 'your_trello_api_key'
TRELLO_TOKEN = 'your_trello_token'
TRELLO_BOARD_ID = 'your_trello_board_id'
TRELLO_LIST_ID = 'your_trello_list_id'
SCOPES = ['https://www.googleapis.com/auth/calendar']

#... existing functions ...

def dictionary_meaning(word):
    dictionary=PyDictionary()
    meanings = dictionary.meaning(word)
    if meanings:
        for key in meanings:
            speak(f"{key}: {meanings[key]}")

def dictionary_synonym(word):
    dictionary=PyDictionary()
    synonyms = dictionary.synonym(word)
    if synonyms:
        speak(f"Synonyms for {word} are:{', '.join(synonyms)}")

def dictionary_antonym(word):
    dictionary=PyDictionary()
    antonyms = dictionary.antonym(word)
    if antonyms:
        speak(f"Antonyms for {word} are: {', '.join(antonyms)}")

def convert_currency(amount, from_currency, to_currency):
    cr = CurrencyRates()
    result = cr.convert(from_currency, to_currency, amount)
    speak(f"{amount} {from_currency} is equal to {result} {to_currency}")

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    engine = pyttsx3.init()
    
    while True:
        try:
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                text = text.lower()

            if "hello" in text:
                speak("Hello! How can I assist you?")
            elif "time" in text:
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"The current time is {current_time}")
            elif "search" in text:
                search = text.split(" ", 1)[1]
                url = f"https://google.com/search?q={search}"
                webbrowser.get().open(url)
                speak(f'Here is what I found for {search} on google')
            elif "weather" in text:
                city = text.split(" ", 1)[1]
                weather = get_weather(city)
                speak(f"The weather in {city} is currently {weather[0]} with {weather[1]} and a temperature of {weather[2]} degrees Celsius.")
            elif "play music" in text:
                play_music("/path/to/your/music/directory")
            elif "write note" in text:
                note = text.split(" ", 2)[2]
                write_note(note, "note.txt")
                speak("I have written down your note.")
            elif "set reminder" in text:
                reminder_text = text.split(" ", 2)[2]
                delay_seconds = 60  # set your desired delay here
                set_reminder(reminder_text, delay_seconds)
                speak(f"I will remind you to {reminder_text} in {delay_seconds} seconds.")
            elif "read news" in text:
                headlines = get_news()
                for headline in headlines[:5]:  # read the top 5 headlines
                    speak(headline)
            elif "question" in text:
                question = text.split(" ", 1)[1]
                answer = answer_question(question)
                speak(answer)
            elif "send email" in text:
                subject = "Hello from your Assistant"  # modify as needed
                body = text.split(" ", 2)[2]
                send_email(subject, body)
                speak("Email sent.")
            elif "send text" in text:
                message = text.split(" ", 2)[2]
                send_text(message)
                speak("Text message sent.")
            elif "lights on" in text:
                control_lights("on")
                speak("Lights have been turned on.")
            elif "lights off" in text:
                control_lights("off")
                speak("Lights have been turned off.")
            elif "add event" in text:
                summary = "New Event"  # modify as needed
                start_time = "2023-07-01T09:00:00"  # modify as needed
                end_time = "2023-07-01T10:00:00"  # modify as needed
                add_calendar_event(summary, start_time, end_time)
                speak("Event added to yourcalendar.")
            elif "add task" in text:
                name = "New Task"  # modify as needed
                desc = text.split(" ", 2)[2]
                create_trello_card(name, desc)
                speak("Task added to your Trello board.")
            elif "meaning" in text:
                word = text.split(" ", 1)[1]
                dictionary_meaning(word)
            elif "synonym" in text:
                word = text.split(" ", 1)[1]
                dictionary_synonym(word)
            elif "antonym" in text:
                word = text.split(" ", 1)[1]
                dictionary_antonym(word)
            elif "convert" in text:
                _, amount, from_currency, _, to_currency = text.split(" ")
                convert_currency(float(amount), from_currency, to_currency)
            elif "exit" in text:
                speak("Goodbye!")
                break
        except sr.UnknownValueError:
            pass

if __name__ == "__main__":
    main()

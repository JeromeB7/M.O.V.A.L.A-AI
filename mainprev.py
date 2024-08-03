# Miraculously Operating Virtual Assistant Like Alexa
# --> Frequently Updated Virtual Assistant Like Siri and Alexa

import speech_recognition as sr
import os
import time
import webbrowser
# import webdriver
import datetime
import google.generativeai as genai
import random


chatStr = ""

def chat(query):
    global chatStr
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    # Create the model configuration
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    # Initialize the generative model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        # safety_settings = Adjust safety settings if needed
        # See https://ai.google.dev/gemini-api/docs/safety-settings
    )
    chatStr += f"Jerome: {query}\Movala:"
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [query],
            }
        ]
    )
    response = chat_session.send_message(query)
    espeak(response.text)
    chatStr += f"{response.text}\n"
    return response.text
    if not os.path.exists("Gemini"):
        os.makedirs("Gemini")

        #with open(f"Gemini/prompt- {random.randint(1, 2343434356)}", "w") as f:
    with open(f"Gemini/{''.join(query.split('ai')[1:]).strip()}.txt", "w") as f:
            f.write(text)

# Function to generate a response using Gemini
def ai(prompt):
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    # Create the model configuration
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    # Initialize the generative model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        # safety_settings = Adjust safety settings if needed
        # See https://ai.google.dev/gemini-api/docs/safety-settings
    )
    text = f"Gemini response for Prompt: {prompt} \n *************************************************** \n\n"
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [prompt],
            }
        ]
    )
    response = chat_session.send_message(prompt)
    # print(response.text)
    text += response.text
    if not os.path.exists("Gemini"):
        os.makedirs("Gemini")

        #with open(f"Gemini/prompt- {random.randint(1, 2343434356)}", "w") as f:
    with open(f"Gemini/{''.join(prompt.split('ai')[1:]).strip()}.txt", "w") as f:
            f.write(text)



def espeak(text):
    # To initialize espeak 
    # os.system(f"espeak -s 100 -v en+f3 -p 50 'Initializing' ")
    #time.sleep(0.2) 
    os.system(f"espeak -s 100 -v en+f3 -p 50 '{text}'")
# def takeCommand():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         r.pause_threshold = 1
#         audio = r.listen(source)
#         try:
#             query = r.recognize_google(audio, language="en-in")
#             print(f"User said: {query}")
#             return query
#         except Exception as e:
#             return "Some Error occured. Sorry from Movala"

if __name__ == '__main__':
    espeak("Hello I am MOVALA-A.I")
    while True:
        print("Listening...")
        # text = takeCommand()
        query = input()
        # espeak(query)
        sites = [["youtube", "https://www.youtube.com"], 
                 ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"],
                 ["chatgpt", "https://www.chatgpt.com"]]
        
        songs = [["God is in Charge", "/home/skywalker/Music/'God is in Charge.mp3'"],
                 ["My God is powerful", "/home/skywalker/Music/'My God is Powerful.mp3'"]]

        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                espeak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
        # For music in system
        for song in songs:        
            if f'play {song[0].lower()} song' in query.lower():
                #musicPath = "/home/skywalker/Music/'My God is Powerful.mp3'"
                espeak(f"Playing {song[0]} sir...")
                os.system(f"ffplay -v 0 -nodisp -autoexit {song[1]}")

        # For search in internet
        if 'search for' in query:
            any = query.lower().replace('search for', '').strip()
            espeak(f"Searching for {any} sir..")
            google_search_url = f"https://www.google.com/search?q={any}"
            webbrowser.open(google_search_url)

        elif 'the time' in query:
            strfTime = datetime.datetime.now().strftime("%H:%M")
            espeak(f"Sir the time is {strfTime}")

        elif 'open VS Code'.lower() in query.lower():
            espeak(f"Opening VS Code sir")
            os.system("/snap/bin/code")
        
        elif "Using AI".lower() in query.lower():
            ai(prompt=query)

        elif "Movala quit".lower() in query.lower():
            exit()
        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            chat(query)
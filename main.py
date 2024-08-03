import os
import time
import webbrowser
import datetime
import google.generativeai as genai
import random

# Initialize the chat history
chatStr = ""

# Function to interact with the AI model
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

    # Append user query to chat history
    chatStr += f"Jerome: {query}\nMovala: "
    
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
    
    # Append AI response to chat history
    chatStr += f"{response.text}\n"
    save_chat(query, chatStr)

def save_chat(prompt, chat_text):
    # Ensure the Gemini directory exists
    if not os.path.exists("Gemini"):
        os.makedirs("Gemini")

    # Generate a valid filename
    sanitized_prompt = ''.join(e for e in prompt if e.isalnum() or e.isspace()).strip().replace(" ", "_")
    if not sanitized_prompt:
        sanitized_prompt = f"prompt_{random.randint(1, 2343434356)}"
    filename = f"Gemini/{sanitized_prompt}.txt"
    
    with open(filename, "w") as f:
        f.write(chat_text)

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
    text += response.text
    save_chat(prompt, text)

def espeak(text):
    os.system(f"espeak -s 100 -v en+f3 -p 50 '{text}'")

if __name__ == '__main__':
    espeak("Hello, I am MOVALA-A.I")
    while True:
        print("Listening...")
        query = input()
        
        sites = [["youtube", "https://www.youtube.com"], 
                 ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"],
                 ["chatgpt", "https://www.chatgpt.com"]]
        
        songs = [["God is in Charge", "/home/skywalker/Music/'God is in Charge.mp3'"],
                 ["My God is powerful", "/home/skywalker/Music/'My God is Powerful.mp3'"]]

        for site in sites:
            if f"open {site[0]}".lower() in query.lower():
                espeak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

        for song in songs:        
            if f'play {song[0].lower()} song' in query.lower():
                espeak(f"Playing {song[0]} sir...")
                os.system(f"ffplay -v 0 -nodisp -autoexit {song[1]}")

        if 'search for' in query.lower():
            search_query = query.lower().replace('search for', '').strip()
            espeak(f"Searching for {search_query} sir..")
            google_search_url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(google_search_url)

        elif 'the time' in query.lower():
            strfTime = datetime.datetime.now().strftime("%H:%M")
            espeak(f"Sir, the time is {strfTime}")

        elif 'open vs code' in query.lower():
            espeak("Opening VS Code sir")
            os.system("/snap/bin/code")

        elif "using ai" in query.lower():
            ai(prompt=query)

        elif "movala quit" in query.lower():
            espeak("Goodbye sir")
            exit()

        elif "reset chat" in query.lower():
            chatStr = ""
            espeak("Chat history has been reset")

        else:
            chat(query)
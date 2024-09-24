import os
import webbrowser
import google.generativeai as genai
import pyttsx3
import datetime
import sounddevice as sd
import numpy as np
import vosk

# Configure the Gemini API key
genai.configure(api_key=os.getenv("API_KEY"))

# Initialize pyttsx3 engine for TTS
engine = pyttsx3.init()

chatStr = ""

def speak(text):
    """ Function to use text-to-speech with pyttsx3 """
    engine.say(text)
    engine.runAndWait()

def chat(query):
    global chatStr
    print(chatStr)
    chatStr += f"User: {query}\nJarvis: "

    # Use Gemini API for chat response
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(chatStr)
    reply = response.text

    speak(reply)
    chatStr += f"{reply}\n"
    return reply

def ai(prompt):
    text = f"Gemini response for Prompt: {prompt} \n *************************\n\n"

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    text += response.text
    if not os.path.exists("Gemini"):
        os.mkdir("Gemini")

    with open(f"Gemini/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)

def record_audio(duration=5, fs=44100):
    """ Function to record audio using sounddevice """
    print("Recording...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    return audio

def takeCommand():
    # Load Vosk model
    model = vosk.Model("model")  # Ensure you have the Vosk model downloaded in the 'model' folder
    recognizer = vosk.KaldiRecognizer(model, 44100)

    with sd.RawInputStream(samplerate=44100, blocksize=8000, dtype='int16', channels=1) as stream:
        print("Listening...")
        while True:
            data = stream.read(4000)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                query = result['text']
                print(f"User said: {query}")
                return query

            # Optionally handle partial results
            partial_result = recognizer.PartialResult()
            if partial_result:
                print(f"Partial result: {partial_result['partial']}")

if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    speak("Jarvis A.I is online.")

    while True:
        query = takeCommand()

        # List of sites to open
        sites = [["youtube", "https://www.youtube.com"],
                 ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"]]

        for site in sites:
            if f"open {site[0]}".lower() in query.lower():
                speak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

        if "open music" in query.lower():
            musicPath = "/path/to/your/music.mp3"
            os.system(f"open {musicPath}")

        elif "the time" in query.lower():
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            speak(f"Sir, the time is {hour} bajke {min} minutes")

        elif "open facetime" in query.lower():
            os.system(f"open /System/Applications/FaceTime.app")

        elif "open pass" in query.lower():
            os.system(f"open /Applications/Passky.app")

        elif "using artificial intelligence" in query.lower():
            ai(prompt=query)

        elif "jarvis quit" in query.lower():
            speak("Goodbye, sir.")
            exit()

        elif "reset chat" in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)

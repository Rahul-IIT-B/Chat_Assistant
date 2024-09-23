import speech_recognition as sr
import sounddevice as sd
import numpy as np
import os
import webbrowser
import google.generativeai as genai
import pyttsx3
import datetime

# Configure the Gemini API key
genai.configure(api_key=os.environ["API_KEY"])

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


def record_audio(duration=5, fs=44100, device=1):
    """ Function to record audio using sounddevice with explicit device selection """
    print("Recording...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64', device=device)
    sd.wait()  # Wait until the recording is finished
    return audio


def takeCommand():
    r = sr.Recognizer()
    mic_index = 1  # Change this to the index of the microphone you want to use
    with sr.Microphone(device_index=mic_index) as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
            return "Some Error Occurred. Sorry from Jarvis"
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return "Some Error Occurred. Sorry from Jarvis"


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

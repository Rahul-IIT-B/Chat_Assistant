import os
import webbrowser
import google.generativeai as genai
import pyttsx3
import datetime

# Configure the Gemini API key
genai.configure(api_key='AIzaSyAXAkuLUaDFcMqI3dxyKnzLtppBHmRsaA0')

# Initialize the TTS engine
engine = pyttsx3.init()

chatStr = ""

def speak(text):
    """ Function to use text-to-speech with pyttsx3 """
    engine.say(text)
    engine.runAndWait()

def chat(query):
    global chatStr
    chatStr += f"User: {query}\nJarvis: "

    # Use Gemini API for chat response
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(chatStr)
    reply = response.text

    speak(reply)
    chatStr += f"{reply}\n"
    return reply

def ai(prompt):
    text = f"Gemini response for Prompt: {prompt}\n*************************\n\n"
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    text += response.text

    if not os.path.exists("Gemini"):
        os.mkdir("Gemini")

    # Save response to a text file
    file_name = f"Gemini/{''.join(prompt.split('intelligence')[1:]).strip()}.txt"
    with open(file_name, "w") as f:
        f.write(text)

if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    speak("Jarvis A.I is online.")

    while True:
        query = input("Type your query: ")  # Get user input

        # List of sites to open
        sites = [
            ["youtube", "https://www.youtube.com"],
            ["wikipedia", "https://www.wikipedia.com"],
            ["google", "https://www.google.com"]
        ]

        # Check for site commands
        for site in sites:
            if f"open {site[0]}".lower() in query.lower():
                speak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
                break

        # Handle other commands
        if "open music" in query.lower():
            musicPath = "/path/to/your/music.mp3"  # Update with the correct path
            os.system(f"start {musicPath}")  # Use 'open' on macOS or 'start' on Windows

        elif "the time" in query.lower():
            current_time = datetime.datetime.now().strftime("%H:%M")
            speak(f"Sir, the time is {current_time}.")

        elif "open facetime" in query.lower():
            os.system("open /System/Applications/FaceTime.app")  # macOS command

        elif "open pass" in query.lower():
            os.system("open /Applications/Passky.app")  # macOS command

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

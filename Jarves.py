import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import urllib.parse
import subprocess
import os
import platform
import pywhatkit as kit
import pyautogui
import psutil


engine = pyttsx3.init()

def set_female_voice():
    voices = engine.getProperty('voices')
    selected = None

    for voice in voices:
        name = str(getattr(voice, "name", "")).lower()
        gender = str(getattr(voice, "gender", "")).lower() if hasattr(voice, "gender") else ""
        if "female" in name or "female" in gender or "zira" in name or "hazel" in name:
            selected = voice.id
            break

    if not selected and len(voices) > 1:
        selected = voices[1].id

    if selected:
        engine.setProperty('voice', selected)

    engine.setProperty('rate', 190)
    engine.setProperty('volume', 1.0)

set_female_voice()

def speak(text):
    print("Jarves:", text)
    engine.stop()
    engine.say(text)
    engine.runAndWait()

def wish_user():
    hour = datetime.datetime.now().hour

    if 0 <= hour < 12:
        greeting = "Good morning Sir"
    elif 12 <= hour < 18:
        greeting = "Good afternoon Sir"
    else:
        greeting = "Good evening Sir"

    speak(f"{greeting}, I am your personal assistant jarves. How can I help you?")

recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.6
recognizer.non_speaking_duration = 0.3
recognizer.dynamic_energy_threshold = True

contacts = {
    "Saksham": "917895447398",
    "Sagar"  : "917351203490",
    "Sissy"  : "917818066792",
    "Mummy"  : "919897152435",
    "Papa"   : "919548316083",
}

def listen():
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        try:
            audio = recognizer.listen(source, timeout=2, phrase_time_limit=3)
        except sr.WaitTimeoutError:
            return ""

    try:
        command = recognizer.recognize_google(audio)
        command = command.lower().strip()
        print("You said:", command)
        return command
    except:
        return ""

def open_whatsapp_app(phone=None, message=None):
    message = message or ""
    encoded_message = urllib.parse.quote(message)

    if phone:
        whatsapp_url = f"whatsapp://send?phone={phone}&text={encoded_message}"
    else:
        whatsapp_url = "whatsapp://"

    system_name = platform.system().lower()

    try:
        if "windows" in system_name:
            os.system(f'start "" "{whatsapp_url}"')
        elif "darwin" in system_name:
            subprocess.run(["open", whatsapp_url], check=False)
        else:
            subprocess.run(["xdg-open", whatsapp_url], check=False)

        speak("Opening WhatsApp")
    except:
        speak("Could not open WhatsApp app")

def send_whatsapp_message(contact_name, message):
    phone = contacts.get(contact_name)

    if not phone:
        speak("Contact not found")
        return

    if not message.strip():
        speak("Message is empty")
        return

    speak(f"Opening WhatsApp for {contact_name}")
    open_whatsapp_app(phone, message)

def guided_whatsapp_message():
    speak("Tell contact name")
    contact_name = listen()

    if not contact_name or contact_name not in contacts:
        speak("Contact not found")
        return

    speak("Tell message")
    message = listen()

    if not message:
        speak("No message detected")
        return

    send_whatsapp_message(contact_name, message)

def extract_message_command(command):
    patterns = [
        "send whatsapp message to ",
        "send message to ",
        "write for ",
        "message "
    ]

    for pattern in patterns:
        if command.startswith(pattern):
            remaining = command.replace(pattern, "").strip()
            words = remaining.split()

            if len(words) >= 2:
                contact_name = words[0]
                message = " ".join(words[1:])
                return contact_name, message

    return None, None



def play_song(song_name):
    if not song_name:
        speak("Please say song name")
        return

    speak(f"Playing {song_name}")
    kit.playonyt(song_name)

def handle_command(command):
    if not command:
        return

    if "hello Jarves" in command:
        speak("Hello Sir")

    elif "how's your day" in command:
          speak("how's your day sir")

    elif "good morning" in command:
        speak("Good morning to you too")

    elif "good afternoon" in command:
        speak("Good afternoon to you too")

    elif "good evening" in command:
        speak("Good evening to you too")

    elif "Shorya Parmar" in command:
        speak("Hello Sir, I am Jarves")

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")

    elif "date" in command:
        today = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"Today's date is {today}")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif command.startswith("play song "):
        song = command.replace("play song ", "").strip()
        play_song(song)

    elif command.startswith("play "):
        song = command.replace("play ", "").strip()
        play_song(song)

    elif "open github" in command:
        speak("Opening GitHub")
        webbrowser.open("https://github.com")

    elif "open GLA university" in command:
        speak("Opening GLA University")
        webbrowser.open("https://www.gla.ac.in")

    elif "open notepad" in command:
        speak("Opening Notepad")
        if platform.system().lower() == "windows":
            subprocess.Popen(["notepad.exe"])
        else:
            speak("Notepad is only supported on Windows")

    elif "open calculator" in command:
        speak("Opening Calculator")
        if platform.system().lower() == "windows":
            subprocess.Popen(["calc.exe"])
        else:
            speak("Calculator is only supported on Windows")

    elif " open command prompt" in command or "open cmd" in command:
        speak("Opening Command Prompt")
        if platform.system().lower() == "windows":
            subprocess.Popen(["cmd.exe"])
        else:
            speak("Command Prompt is only supported on Windows")

    elif "open linkedIn" in command:
        speak("Opening LinkedIn")
        if platform.system().lower() == "windows":
            subprocess.Popen(["linkedin"])
        else:
            speak("LinkedIn app is only supported on Windows")

            
    elif "open whatsapp" in command:
        open_whatsapp_app()

    elif (
        command.startswith("send whatsapp message to ") or
        command.startswith("send message to ") or
        command.startswith("write for ") or
        command.startswith("message ")
    ):
        contact_name, message = extract_message_command(command)
        if contact_name and message:
            send_whatsapp_message(contact_name, message)
        else:
            speak("Say name and message")

    elif "send whatsapp" in command:
        guided_whatsapp_message()

    elif "search for" in command:
        query = command.replace("search for", "").strip()
        if query:
            speak(f"Searching {query}")
            webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(query)}")

    elif "wish me" in command:
        wish_user()

    elif "exit" in command or "stop" in command or "close Jarves" in command:
        speak("Goodbye")
        exit()

    else:
        speak("Command not understood")

wish_user()

while True:
    command = listen()
    handle_command(command)
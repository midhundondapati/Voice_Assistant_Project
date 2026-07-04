import customtkinter as ctk
import pyttsx3
import speech_recognition as sr
import threading
import datetime
import wikipedia
import pyjokes
import webbrowser
import pywhatkit
import os

# ---------------- SETTINGS ----------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

engine = pyttsx3.init()

command_count = 0
history = []

# ---------------- SPEAK ----------------

def speak(text):
    output.insert("end", f"\n🤖 Jarvis: {text}\n")
    output.see("end")

    engine.say(text)
    engine.runAndWait()

# ---------------- LISTEN ----------------

def listen():

    status_label.configure(text="🎤 Listening...")

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:

            recognizer.adjust_for_ambient_noise(source)

            audio = recognizer.listen(source)

        command = recognizer.recognize_google(audio)

        output.insert("end", f"\n👤 You: {command}\n")

        process_command(command.lower())

    except Exception:
        output.insert("end", "\n⚠ Could not understand.\n")

    status_label.configure(text="✅ Ready")

# ---------------- COMMANDS ----------------

def process_command(command):

    global command_count

    command_count += 1

    history.append(command)

    counter_label.configure(
        text=f"Commands : {command_count}"
    )

    status_label.configure(
        text="⚙ Processing..."
    )

    # Greeting

    if "hello" in command:

        speak("Hello, nice to meet you.")

    # Time

    elif "time" in command:

        current_time = datetime.datetime.now().strftime("%I:%M %p")

        speak(f"The time is {current_time}")

    # Date

    elif "date" in command:

        today = datetime.datetime.now().strftime("%d %B %Y")

        speak(f"Today is {today}")

    # Open YouTube

    elif "open youtube" in command:

        webbrowser.open("https://youtube.com")

        speak("Opening YouTube")

    # Search YouTube

    elif "search youtube" in command:

        query = command.replace("search youtube", "")

        speak(f"Searching YouTube for {query}")

        pywhatkit.playonyt(query)

    # Open Google

    elif "open google" in command:

        webbrowser.open("https://google.com")

        speak("Opening Google")

    # Search Google

    elif "search google" in command:

        query = command.replace("search google", "")

        webbrowser.open(
            f"https://www.google.com/search?q={query}"
        )

        speak(f"Searching Google for {query}")

    # Wikipedia

    elif "wikipedia" in command:

        query = command.replace(
            "wikipedia",
            ""
        )

        try:

            result = wikipedia.summary(
                query,
                sentences=2
            )

            speak(result)

        except:

            speak("No information found.")

    # Joke

    elif "joke" in command:

        speak(pyjokes.get_joke())

    # Notepad

    elif "open notepad" in command:

        os.system("notepad")

        speak("Opening Notepad")

    # Calculator

    elif "open calculator" in command:

        os.system("calc")

        speak("Opening Calculator")

    # History

    elif "history" in command:

        speak("Showing recent commands")

        output.insert(
            "end",
            "\n".join(history[-10:]) + "\n"
        )

    # Exit

    elif "exit" in command:

        speak("Goodbye")

        app.destroy()

    else:

        speak("Command not recognized")

    status_label.configure(
        text="✅ Ready"
    )

# ---------------- THREAD ----------------

def start_listening():
    threading.Thread(
        target=listen,
        daemon=True
    ).start()

# ---------------- GUI ----------------

app = ctk.CTk()

app.title("JARVIS AI")

app.geometry("900x650")

# Title

title = ctk.CTkLabel(
    app,
    text="JARVIS AI ASSISTANT",
    font=("Arial", 30, "bold")
)

title.pack(pady=15)

# Status

status_label = ctk.CTkLabel(
    app,
    text="✅ Ready",
    font=("Arial", 16)
)

status_label.pack()

# Counter

counter_label = ctk.CTkLabel(
    app,
    text="Commands : 0",
    font=("Arial", 16)
)

counter_label.pack(pady=5)

# Mic Button

listen_btn = ctk.CTkButton(
    app,
    text="🎤",
    width=120,
    height=120,
    corner_radius=60,
    font=("Arial", 40),
    command=start_listening
)

listen_btn.pack(pady=20)

# Output Box

output = ctk.CTkTextbox(
    app,
    width=800,
    height=300,
    font=("Consolas", 15)
)

output.pack(pady=10)

# Buttons Frame

frame = ctk.CTkFrame(app)

frame.pack(pady=10)

# Clear Button

clear_btn = ctk.CTkButton(
    frame,
    text="Clear",
    command=lambda: output.delete(
        "1.0",
        "end"
    )
)

clear_btn.grid(
    row=0,
    column=0,
    padx=10
)

# Dark Mode

dark_btn = ctk.CTkButton(
    frame,
    text="Dark Mode",
    command=lambda:
    ctk.set_appearance_mode("dark")
)

dark_btn.grid(
    row=0,
    column=1,
    padx=10
)

# Light Mode

light_btn = ctk.CTkButton(
    frame,
    text="Light Mode",
    command=lambda:
    ctk.set_appearance_mode("light")
)

light_btn.grid(
    row=0,
    column=2,
    padx=10
)

# Welcome Message

speak(
    "Hello. I am Jarvis. Press the microphone button and speak a command."
)

app.mainloop()

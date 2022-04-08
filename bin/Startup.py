import os, win32gui,win32con

import speech_recognition as sr

win32gui.ShowWindow(win32gui.GetForegroundWindow() , win32con.SW_HIDE)

def commands():
    r = sr.Recognizer()
    query = ''
    with sr.Microphone() as source:
        r.pause_threshold = 0.5
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-us')
    except:
        return "IDK"
    return query

def main():
    query = ""
    while True:
        if "google" in query or "jarvis" in query: 
            break
        else:
            query = commands()
            query = query.lower()
            print(query)


while True:
    main()
    os.system("start Karen")
    
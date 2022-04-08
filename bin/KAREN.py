from datetime import datetime
from tkinter import *
from PIL import ImageTk, Image
import speech_recognition as sr
import win32gui, win32con, pyttsx3, datetime, sys, wikipedia, wolframalpha, os, random, webbrowser
import urllib.request, urllib.parse, re, json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

from modules import weather
#folder = r'C:\\Users\\rynda\\Music\\'

config = open(BASE_DIR/"config.json","r",encoding="utf-8")
conf_data = json.load(config)

client = wolframalpha.Client(conf_data["wolframalpha"])
engine = pyttsx3.init()
voices = engine.getProperty('voices')

def speak(audio):
    print('Karen:', audio)
    engine.setProperty('voice', voices[len(voices) - 1].id)
    engine.say(audio)
    engine.runAndWait()

def greetMe():
    currentH = int(datetime.datetime.now().hour)
    #win32gui.ShowWindow(win32gui.GetForegroundWindow() , win32con.SW_HIDE)
    if currentH >= 0 and currentH < 12:
        speak('Good Morning!')

    elif currentH >= 12 and currentH < 18:
        speak('Good Afternoon!')

    elif currentH >= 18 and currentH <0:
        speak('Good Evening!')
    else:
        speak('Good Night!')

def myCommand():
   
    r = sr.Recognizer()                                                                                   
    with sr.Microphone() as source:                                                                       
        print("Listening...")
        speak("Listening...")
        r.pause_threshold =  1
        audio = r.listen(source)
    
    try:
        query = r.recognize_google(audio, language='pl')
        print('User: ' + query + '\n')
    except sr.UnknownValueError:
        try:
            query = r.recognize_google(audio, language='en-us')
            print('User: ' + query + '\n')
        except sr.UnknownValueError:
            speak('Try again')
            pass

    return query

def search(program, query):
    speak('okay')

    # speak('What you need to search?: ')
    x = query.find(program) + len(program)
    y = query.find("search")
    z = query.find("wyszukaj")
    if y != -1:
        query = query[y + 6:]
    elif z != -1:
        query = query[z + 8:]
    if len(query[x:]) > 2:
        query = query[x:]
    else:
        speak('What you need to search?: ')
        query = myCommand()
    return query

class Widgets:
    def __init__(self):
        greetMe()
        root = Tk()
        root.title('KAREN')
        root.config(background='Red')
        root.geometry('350x600')
        root.resizable(1,1)
        root.iconbitmap(BASE_DIR/'img/spider.ico')
        #bottom label
        
        img = ImageTk.PhotoImage(Image.open(BASE_DIR/"img/karen.jpg"))
        panel = Label(root, image = img)
        panel.pack(side = "bottom", fill = "both", expand = "no")

        self.query = ""
        self.userText = StringVar()

        self.userText.set('Click \'Enter\' to Give commands')

        #User window
        userFrame = LabelFrame(root, text="Spiderman", font=('Black ops one', 10, 'bold'))
        userFrame.pack(fill="both", expand="yes")
         
        left2 = Label(userFrame, textvariable=self.userText, bg='dodgerBlue', fg='white',justify=LEFT)
        left2.config(font=("Comic Sans MS", 10, 'bold'))
        left2.pack(fill='both', expand='yes')

        #comp window
        compFrame = LabelFrame(root, text="KAREN", font=('Black ops one', 10, 'bold'))
        compFrame.pack(fill="both", expand="yes")

        scrollbar = Scrollbar(compFrame)
        scrollbar.pack( side = RIGHT, fill = Y )

        self.mylist = Listbox(compFrame, yscrollcommand = scrollbar.set, bg='Red', fg='white', justify=LEFT)
        self.mylist.config(font=("Comic Sans MS", 10, 'bold'))
        self.mylist.pack(fill = BOTH, expand='yes' )
        scrollbar.config( command = self.mylist.yview )
        self.mylist.insert(END,"What can I do for you?")
        
        #searchbar
        self.view = Entry(master=root, font = "Helvetica 15 bold", justify=CENTER, text=LEFT)
        self.view.pack(fill='x',expand='no')
        #btn = Button(root, text='Enter', font=('Black Ops One', 10, 'bold'), bg='deepSkyBlue', fg='white', command=self.clicked)
        #btn.pack(fill='x', expand='no')


        root.bind("<Return>", self.clicked) # handle the enter key event of your keyboard
        root.mainloop()
        
    def sets(self,compText):
        self.mylist.delete(0, END)
        temp = ''
        ile = 0
        for i in compText:
            temp+=i
            ile+=1
            if (i ==" " and ile>40) or i=="\n":
                self.mylist.insert(END,temp)
                ile=0
                temp=''
        self.mylist.insert(END,temp)

    def google(self):
        self.query = search('google', self.query)
        temp = self.query.split()
        wynik = ""
        for i in range(len(temp)):
            wynik += temp[i] + "+"
        webbrowser.open('www.google.com/search?q=%s' % wynik)
        self.sets("Openinig google search")

    def youtube(self):
        query = search('youtube', self.query)

        query_string = urllib.parse.urlencode({"search_query": query})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'watch\?v=(\S{11})', html_content.read().decode())
        webbrowser.open("http://www.youtube.com/watch?v=%s" % search_results[0])

    def wiki(self):
        self.query = search('wiki', self.query)
        try:
            results = wikipedia.summary(self.query, sentences=2)
            sentence = "Wikipedia says: \n" +results

            self.sets(sentence)
        except:
            webbrowser.open('https://pl.wikipedia.org/wiki/%s' % self.query)
    
    def weather(self):
        weather.write()
        if "dzisiaj" in self.query or "today" in self.query:
            content = weather.read(0)
        elif "jutro" in self.query or "tomorrow" in self.query:
            content = weather.read(1)
        else:
            content = "Here you go! That's your weater"
            print(weather.read())
        speak("Here you go! That's your weater")
        self.sets(content)

    def wifi(self):
        os.system(r'start "karen" .\other\speedtest.bat')
        f = open(r'.\other\wifi.txt')
        fi = f.read()
        self.sets(fi)
    
    def web(self):
        webbrowser.open(self.query[4:])
    
    def cmd(self):
        os.system(self.query[4:])

    def shutdown(self):
            if "stop" in self.query:
                os.system("shutdown -a")
            else:
                if len(self.query) > 9:
                    os.system("shutdown -s -t %s" % (self.query[9:]))
                else:
                    os.system("shutdown -s -t 600")

    def bye(self):
        self.sets('Bye Sir, have a good day.')
        speak('Bye Sir, have a good day.')
        sys.exit()

    def programs(self):
        file = open("responses.json","r",encoding="utf-8")
        data = json.load(file)

        for res_tab in data["res"]:
            for i in res_tab["query"]:

                if i in self.query:
                    res = random.choice(res_tab["response"])
                    speak(res)
                    self.sets(res)
                    return True

        for prog_tab in data["programs"]:
            for i in prog_tab["query"]:

                if i in self.query:
                    res = random.choice(prog_tab["response"])
                    for p in prog_tab["exec"]:
                        os.system(r'start "karen" %s' %p)
                    print(res)
                    speak(res)
                    self.sets(res)
                    return True
        return False
    
    def other(self):
        try:
            try:
                res = client.query(self.query)
                results = next(res.results).text
                results = "WolframAlpha says: \n"+results
                self.sets(results)
                speak("Reasult from WolframAlpha")

            except:
                results = wikipedia.summary(self.query, sentences=2)
                sentence = "Wikipedia says: \n"+results
                self.sets(sentence)
                speak("Reasult from Wikipedia")
                
        except:
            speak('I don\'t know Sir! Google is smarter than me!')
            self.sets('I don\'t know Sir! Google is smarter than me!')
            temp = self.query.split()
            result = ""
            for i in temp:
                result += i + "+"
            webbrowser.open('www.google.com/search?q=%s' % result)

    def clicked(self,*args):
        print(self.query)
        self.query = self.view.get()
        self.view.delete(0,END)
        if self.query == "":
            self.query = myCommand()
        
        self.userText.set(self.query)
        self.query = self.query.lower()
        flag = False
        #name of function asign to keyword
        keywords = {self.google:["google"], 
                    self.youtube:["youtube"], 
                    self.wiki:["wiki"], 
                    self.weather:["weather", "pogoda"], 
                    self.wifi:['scan wifi', 'speedtest', 'skan wifi'], 
                    self.web:["www"],
                    self.cmd:["cmd"],
                    self.shutdown:["shut down","shutdown"], 
                    self.bye:['zakończ', 'bye', 'stop']}

        for key, value in keywords.items():
            for j in value:
                if j in self.query:
                    key()
                    flag=True
                    break

        if not flag:
            flag = self.programs()
            
        if not flag: #search in wolframalpha and wikipedia
            self.other()
                
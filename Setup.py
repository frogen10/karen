import ctypes, sys,os
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    os.system("python -m pip install --upgrade pip")
    os.system("pip install keyboard wolframalpha wikipedia pywin32 pillow pyttsx3==2.71 speechrecognition")
    os.system("pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib")

    path = str(os.getcwd())+'\\bin'
    plik = open("./bin/Karen.bat", 'w', encoding="utf-8")
    plik.write("D:\ncd "+path+"\npython .\\main.py\nexit")
    plik.close()

    plik = open("./bin/Startup.bat", 'w', encoding="utf-8")
    plik.write("python "+path+"\\Startup.py")
    plik.close()
    x = ord(input("Set up on startup? (Y)/N"))
    if x!=ord('N') and x!=ord("n"):
        os.system(r'setx path "%path%;'+path)
        os.system(r'REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /V "Jarvis" /t REG_SZ /F /D "'+path+"\\Startup.bat\"")
        os.system("pause")
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


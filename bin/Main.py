import win32gui, keyboard

if __name__ == '__main__':
    hwnd = win32gui.FindWindow(None,"KAREN")
    print(hwnd)
    if int(hwnd) == 0:
        import KAREN 
        widget = KAREN.Widgets()
    else: #if window exist focus on opened window
        win32gui.ShowWindow(hwnd,5)
        win32gui.SetForegroundWindow(hwnd)
        keyboard.press('enter')
        keyboard.release('enter')
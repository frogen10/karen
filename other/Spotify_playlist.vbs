Set WshShell = WScript.CreateObject("WScript.Shell")
Comandline = "C:\Users\rynda\AppData\Roaming\Spotify\Spotify.exe"
WScript.sleep 500
CreateObject("WScript.Shell").Run("spotify:user:spotify:playlist:37i9dQZF1DX0jc7XXxzhOG")
WScript.sleep 3000
WshShell.SendKeys " "
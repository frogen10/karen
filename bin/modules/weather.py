import requests, json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

def conversion(date): # konwersja daty na polską
    x = date.find("T")
    daysOfWeek={"Monday":"Poniedziałek", "Tuesday":"Wtorek", "Wednesday":"Środa", "Thursday":"Czwartek","Friday":"Piątek", "Saturday":"Sobota", "Sunday":"Niedziela"}
    Day = datetime(int(date[:4]),int(date[5:7]),int(date[8:x]))
    weekDay = Day.strftime('%A')
    return Day.strftime('%d.%m.%Y')+" "+daysOfWeek[weekDay]

def write_to_file():
    config = open(BASE_DIR/"config.json",encoding="utf-8")
    conf_data = json.load(config)
    api_key = conf_data["accuweather"]
    CityId = conf_data["CityID"] 
    url = r"http://dataservice.accuweather.com/forecasts/v1/daily/5day/"+CityId+"?apikey="+api_key+"&language=pl&details=True&metric=True"
    response = requests.get(url)
    data = response.json()
    print(url)
    code = None
    content = ""
    try:
        code = data['Code']
    except Exception:
        pass
    if code!=None : # jeśli servis nie jest osiągalny
        content = data['Message'] # napisz wiadomość dlaczego

    else:
        
        dailyWeather=data["DailyForecasts"] # lista dni z pogodą
        for weather in dailyWeather:
            # temperatura minimalna i maksymalna
            temperature = str(weather["Temperature"]["Minimum"]["Value"]) +"°C i "+ str(weather["Temperature"]["Maximum"]["Value"])+"°C"

            day = weather["Day"] #skróty do dnia 
            night = weather["Night"] # i nocy

            SkyDay = day["IconPhrase"] # informacja o chmurach 
            SkyNight = night["IconPhrase"]

            windDay = str(day["Wind"]["Speed"]["Value"]) +"km/h" # informacja o wietrze 
            windNight=str(night["Wind"]["Speed"]["Value"])+"km/h"

            PrecipitationDay =str(day["PrecipitationProbability"]) + "%" # informacja o możliwości opadów 
            PrecipitationNight = str(night["PrecipitationProbability"])+"%"
            
            spaces = int(len(SkyDay))+6
            #wypisz na ekran
            
            content +=("\n Pogoda na dzień: "+conversion(weather["Date"])+
                    "\n Temperatura pomiędzy:   " + temperature + 
                    "\n Parametry                   Dzień"+(" "*(spaces-5))+"Noc"+
                    "\n ______________________________________________________________________"+
                    "\n Niebo:                      "+SkyDay+"      "+SkyNight+
                    "\n Prędkość wiatru :           "+windDay+(" "*(spaces-len(windDay)))+ windNight+
                    "\n Prawdopodobieństwo opadów:  "+ PrecipitationDay+(" "*(spaces-len(PrecipitationDay)))+PrecipitationNight)
            
            if day["HoursOfPrecipitation"]>0.5 or night["HoursOfPrecipitation"]>2:
                
                if day["HoursOfRain"]>0.5 or night["HoursOfRain"]:
                    content+=("\n Ilość godzin deszczu:       "+str(day["HoursOfRain"])+(" "*(spaces-len(str(day["HoursOfRain"]))))+str(night["HoursOfRain"])+
                    "\n Ilość opadów w mm:          "+str(day["Rain"]["Value"])+(" "*(spaces-len(str(day["Rain"]["Value"]))))+str(night["Rain"]["Value"]))
                
                if day["HoursOfSnow"]>0.5 or night["HoursOfSnow"]:
                    content+=("\n Ilość godzin opadów śniegu:       "+str(day["HoursOfSnow"])+(" "*(spaces-len(str(day["HoursOfSnow"]))))+str(night["HoursOfSnow"])+
                    "\n Ilość opadów w mm:          "+str(day["Snow"]["Value"])+(" "*(spaces-len(str(day["Snow"]["Value"])))))
            content+="\n"
    
    return content

def write():
    plik = open(BASE_DIR/"bin/modules/weather.txt","w",encoding="utf-8")
    plik.write(write_to_file())
    plik.close()

def read(date = None):
    plik = open(BASE_DIR/"bin/modules/weather.txt","r",encoding="utf-8")
    if date == None:
        return plik.read()
        
    elif date == 0:
        tmp = plik.readlines()
        i =tmp.index("\n",1)
        return ''.join(tmp[:10])
    elif date == 1:
        tmp = plik.readlines()
        i = tmp.index("\n",1)
        j = tmp.index("\n",i+1)
        return ''.join(tmp[i+1:j])
    plik.close()
# tester
# print(read(1))

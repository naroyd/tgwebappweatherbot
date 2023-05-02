# -*- coding: utf-8 -*-
import time
import random
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
from geopy.geocoders import Nominatim
from astral import moon
from astral.moon import moonrise, moonset
from astral.sun import sunrise, sunset
from astral import LocationInfo
from timezonefinder import TimezoneFinder
import pytz
import json
import datetime

class WEATHER:
    def __init__(self, owm_token,  city_name):
        self.city_name= city_name
        self.config_dict= get_default_config()
        self.config_dict['language']= 'en'
        self.owm = OWM(owm_token, self.config_dict)
        self.mgr = self.owm.weather_manager()

    def Search_City(self, str):
        geolocator = Nominatim(user_agent="inf_proj")
        location = geolocator.geocode(str,language='en')
        if location != None:
                location_s = location.address.replace(' ','').split(',')
                return [location_s[0], location_s[len(location_s)-1], location.latitude, location.longitude, TimezoneFinder().timezone_at(lng=location.longitude, lat=location.latitude)]
        return None
        
    def month_detach(self, num):
        arr = ["January", "Febuary", "Mart", "April","May", "June", "July", "August", "Septeber", "October", "November", "December"]
        return arr[num-1]

    def daytime(self, hour):
        if 0<=hour<6:
            return "night"
        elif 6<=hour<12:
            return "morning"
        elif 12<=hour<18:
            return "afternoon"
        else:
            return "evening"
        
    def wind_direction(self, deg):
        if 337.5<=deg or deg<=22.5:
            return "Northern"
        elif 22.5<deg<67.5:
            return "Northeastern"
        elif 67.5<=deg<=112.5:
            return "Eastern"
        elif 112.5<deg<157.5:
            return "Southeastern"
        elif 157.5<=deg<=202.5:
            return "Southern"
        elif 202.5<deg<247.5:
            return "Southwestern"
        elif 247.5<=deg<=292.5:
            return "Western"
        else:
            return "Northwestern"
    
    def gusts(self, wind):
        try:
            return wind['gust']
        except:
            return None
        
    def icon(self, weather):
        if weather=="Clear":
            rise = sunrise(self.loc.observer, self.dt,self.tmz)
            set = sunset(self.loc.observer, self.dt, self.tmz)
            if not (rise<=self.dt<=set):
                return fr"assets/icons/weather/main/moon/{self.moon[3]}"
        return fr"assets/icons/weather/main/{weather}"


    def forecasts(self):
        daily_forecaster = self.mgr.forecast_at_coords(self.lat, self.lon, '3h') 
        weaher = daily_forecaster.forecast
        i=0
        forecasts=[]
        for ws in weaher:
            if i==6: break
            elif i!=0:
                forecasts.append({'time':str(ws.reference_time('iso'))[11:16], 'weather':str(ws.status), 'temp':int(round(ws.temperature('celsius')['temp'])), 'feel':int(round(ws.temperature('celsius')['feels_like'])), "icon": self.icon(str(ws.status))})
            i+=1
        return forecasts
    
    def aqi(self):
        try:
            arr = ['Low', 'Moderate', 'High', 'Very high', 'Extreme']
            return arr[int(self.owm.airpollution_manager().air_quality_at_coords(self.lat, self.lon).aqi)-1]
        except:
            return None
    
    def uvi(self):
        try:
            return self.owm.uvindex_manager().uvindex_around_coords(self.lat,self.lon).get_exposure_risk().capitalize()
        except:
            return None
        
    def sun_info(self):
        rise = sunrise(self.loc.observer, self.dt,self.tmz)
        set = sunset(self.loc.observer, self.dt, self.tmz)
        if rise<=self.dt<=set:
            delta_dt=self.dt-rise
            delta_set=set-rise
            percent=(delta_dt.seconds)/(delta_set.seconds)
        else:
            percent = 0
        return [str(rise)[11:16], str(set)[11:16], percent]
        
    def moon_info(self):
        phase = moon.phase(self.dt)
        if phase == 0 or 27<phase<28:
            phase = 0
        elif 1 < phase < 6:
            phase = 1
        elif 6 < phase < 8:
            phase = 2
        elif 8 < phase < 13:
            phase = 3
        elif 13 < phase < 15:
            phase = 4
        elif 15 < phase < 20:
            phase = 5
        elif 20 < phase < 22:
            phase = 6
        else:
            phase = 7

        rise = moonrise(self.loc.observer, self.dt, self.tmz)
        try:
            set=moonset(self.loc.observer, self.dt, self.tmz)
            if rise>set:
                if self.dt>set:
                    set=moonset(self.loc.observer, self.dt+datetime.timedelta(days=1), self.tmz)
                else:
                    rise=moonrise(self.loc.observer, self.dt-datetime.timedelta(days=1), self.tmz)
        except:
            set=moonset(self.loc.observer, self.dt+datetime.timedelta(days=1), self.tmz)
        
        if rise<=self.dt<=set:
            delta_dt=self.dt-rise
            delta_set=set-rise
            percent=(delta_dt.seconds)/(delta_set.seconds)
        else:
            percent = 0

        return [str(rise)[11:16], str(set)[11:16], percent, phase]

    
    def GET_WEATHER(self):
        self.city, self.country, self.lat, self.lon, self.tmz = self.Search_City(self.city_name)
        self.observation = self.mgr.weather_at_coords(self.lat, self.lon)
        self.w = self.observation.weather
        self.loc = LocationInfo(self.city, self.country, self.tmz, self.lat, self.lon)
        self.dt = datetime.datetime.now(pytz.timezone(self.tmz))
        self.weather_now = self.w.status
        self.sun=self.sun_info()
        self.moon = self.moon_info()
        self.wind = self.w.wind()
        self.ico = self.icon(self.weather_now)

        dct = {
        "main":{
        "temp": int(round(self.w.temperature('celsius')['temp'])),
        "image": fr"{random.randint(1,144)}",
        "weather": self.weather_now,
        "icon": self.ico,
        "location": f"{self.city}, {self.country}",
        "day":self.dt.day,
        "month":self.month_detach(self.dt.month)
        },
        "forecast":self.forecasts(),
        "wind":{
        "deg": self.wind['deg'],
        "speed": self.wind['speed'],
        "gusts": self.gusts(self.wind),
        "dir":self.wind_direction(self.wind['deg'])
        },
        "air":{
        "wetness": self.w.humidity,
        "pressure": int(round(self.w.barometric_pressure()['press']*0.7501)),
        "aqi": self.aqi(),
        "uvi": self.uvi()
        },
        "rise_set":{
        "sunrise":self.sun[0],
        "sunset":self.sun[1],
        "sun_percent":self.sun[2],
        "moonrise":self.moon[0],
        "moonset":self.moon[1],
        "moon_percent": self.moon[2],
        "moonphase" : self.moon[3]}
        }
        return json.dumps(dct)
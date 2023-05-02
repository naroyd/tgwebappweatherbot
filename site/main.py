# -*- coding: utf-8 -*-
import weather
import config

W  = weather.WEATHER(config.OWM_TOKEN, input())

print(W.GET_WEATHER())
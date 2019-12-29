#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from flask import Flask, Response, request
from configparser import ConfigParser
import json
import urllib.request


app = Flask(__name__)
parser = ConfigParser()
parser.read('config/config.ini')

def read_configuration():

    parser = ConfigParser()
    parser.read('config/config.ini')

    print(parser.get('openweathermap', 'user_api_key'))
    print(parser.get('application', 'server_name'))



@app.route('/')
def get_app_info():
    return "Appen verkar!"


@app.route('/', methods=['POST'])
def get_weather():
    location = request.form.get('text')
    token = request.form.get('token')

    valid_token = parser.get('mattermost', 'authorization_token')
    require_authorization = parser.get('mattermost', 'require_authorization')
    user_api_key = parser.get('openweathermap', 'user_api_key')
    measurement_unit = parser.get('openweathermap', 'unit')

    if require_authorization == 'true':
        if token == valid_token:
            weather_api_url = openweathermap_url_builder(location, False, user_api_key, measurement_unit)
            #return weather_api_url
        else:
            return 'Nei.'
    else:
        return 'accept.'

    # If the /weather command contains no arguments, the default action is to display a weather overview.
    if location == 'None':
        location = 'Bergen'
    else:
        weather_api_url = openweathermap_url_builder(urllib.parse.quote(location), False, user_api_key, measurement_unit)

    weather_data = urllib.request.urlopen(weather_api_url)
    weather_data_text = weather_data.read().decode('utf-8')
    weather_data_json = json.loads(weather_data_text)

    return weather_data_json
    # json_data = 'test'
    # mattermost_text = build_response_text(json_data)
    # return mattermost_text

    return 'Data me fekk var: ' + str(location) + str(token)


def get_weather_icon_url(icon_code, description):
    icon_url = '![desc](http://openweathermap.org/img/w/{code}.png "{desc}")'.format(code=icon_code, desc=description)
    return icon_url


def build_forecast_response_text(data):
    return 'test'


def build_weather_response_text(data):
    return 'test'


def build_weather_overview_text(data):
    return 'test'


def openweathermap_url_builder(location, forecast, user_api_key, unit):
    forecast_api_url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q='
    weather_api_url = 'http://api.openweathermap.org/data/2.5/weather?q='

    if forecast:
        resulting_api_url = forecast_api_url + str(location) + '&mode=json&units=' + unit + '&APPID=' + user_api_key + '&cnt=7'
    else:
        resulting_api_url = weather_api_url + str(location) + '&mode=json&units=' + unit + '&APPID=' + user_api_key

    return resulting_api_url


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

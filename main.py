import requests
import configparser
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def weather_dashboard():
    return render_template('base.html')


@app.route('/results', methods=['POST'])
def results():
    zip_code = request.form['zipCode']
    country_coad = request.form['country_code']

    api_key = get_api_key()
    data_to_show = get_weather_res(zip_code, country_coad, api_key)
    temp = "{0:.2f}".format(data_to_show["main"]["temp"])
    feels_like = "{0:.2f}".format(data_to_show["main"]["feels_like"])
    temp_min = "{0:.2f}".format(data_to_show["main"]["temp_min"])
    temp_max = "{0:.2f}".format(data_to_show["main"]["temp_max"])
    weather = data_to_show["weather"][0]["main"]
    location = data_to_show["name"]

    return render_template('results.html', location=location, temp=temp,
                           feels_like=feels_like, weather=weather,
                           temp_max=temp_max, temp_min=temp_min)


def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']


def get_weather_res(zip_code, country_code, api_key):
    api_url = "http://api.openweathermap.org/data/2.5/weather?zip={}&country={}&units=metric&appid={}".format(zip_code,
                                                                                                              country_code, api_key)
    r = requests.get(api_url)
    return r.json()


if __name__ == '__main__':
    app.run()

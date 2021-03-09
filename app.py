from flask import Flask, request, render_template, redirect
import os
import requests


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('index.html')


@app.route('/city')
def city_search():
    API_KEY = os.environ.get('API_KEY')  # укажите переменные среды для ключа
    city = request.args.get('q')
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'

    response = requests.get(url).json()
    if response.get('cod') != 200:
        msg = response.get('message', '')
        return f'Ошибка получения температуры для города {city.title()}, сообщение: {msg}'

    current_weather = response.get('main', {}).get('temp')
    if current_weather:
        celsius = round(current_weather - 273.15, 2)
        return f'Temperature in {city.title()} now is {celsius}'
    else:
        return f'Error getting temperature for {city.title()}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

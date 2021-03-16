from flask import Flask, request, render_template, redirect, url_for
from forms import SearchForm
from config import Config
import os
import requests


app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    form = SearchForm()
    if form.validate_on_submit():
        city = request.form['city'].lower()
        return redirect(url_for('city_search', city=city))
    return render_template('index.html', form=form)


@app.route('/city?q=<city>')
def city_search(city):
    API_KEY = os.environ.get('API_KEY') or 'try-to-connect'  # укажите переменные среды для ключа
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

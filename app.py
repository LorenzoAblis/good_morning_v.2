from flask import Flask, render_template
from data_scraper import get_overview_data, get_current_weather_data, get_forecast_data, get_news_data
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/')
@cache.cached(timeout=3600)
def overview():
    overview_data = get_overview_data()

    return render_template('overview.html', overview_data=overview_data)

@app.route('/news')
@cache.cached(timeout=3600)
def news():
    news_data = get_news_data()

    return render_template('news.html', news_data=news_data)

@app.route('/weather')
@cache.cached(timeout=3600)
def weather():
    current_weather_data = get_current_weather_data()
    forecast_data = get_forecast_data()

    forecast_column_1 = forecast_data[::2]
    forecast_column_2 = forecast_data[1::2]

    return render_template('weather.html', current_weather_data=current_weather_data, forecast_column_1=forecast_column_1, forecast_column_2=forecast_column_2)

if __name__ == '__main__':
    app.run(debug=True)

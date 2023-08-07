import requests
import os
import dotenv
import datetime as dt


def get_overview_data():
    news_data = get_news_data()
    forecast_data = get_forecast_data()
    weather_data = get_current_weather_data()
    news_overview = []
    forecast_overview = []

    for article in news_data:
        article_overview = {
            'title': article['title'],
            'url': article['url'],
        }
        news_overview.append(article_overview)
    
    for day in forecast_data:
        day_overview = {
            'day': day['day'],
            'high_low': day['high_low'],
            'precip': day['precip']
        }
        forecast_overview.append(day_overview)

    weather_overview = {
        'temperature': weather_data['temperature'],
        'uv_index': weather_data['uv_index'],
        'precip': weather_data['precip'],
        'air_quality': weather_data['air_quality'],
        'high_low': weather_data['high_low']
    }

    overview_data = {
        'news': news_overview,
        'forecast': forecast_overview,
        'weather': weather_overview
    }

    return overview_data

def get_news_data():
    dotenv.load_dotenv()

    api_key = os.environ.get('NEWS_API_KEY')
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
    response = requests.get(url)
    news_data = []

    if response.status_code == 200:
        data = response.json()
        articles = data['articles']
        counter = 0

        for article in articles:
            if counter < 10:
                news_data.append({
                    'title': article['title'],
                    'description': article['description'],
                    'source': article['source']['name'],
                    'url': article['url'],
                    'image_url': article['urlToImage']
                })
                
                counter += 1
    else:
        return []

    return news_data
    
def get_current_weather_data():
    dotenv.load_dotenv()
    api_key = os.environ.get('WEATHER_API_KEY')

    params = {
        'access_key': api_key,
        'query': 'Mount Prospect',
        'units': 'f'
    }

    weather_response = requests.get('http://api.weatherstack.com/current', params)

    extra_weather_url = 'https://api.open-meteo.com/v1/forecast?latitude=42.0664&longitude=-87.9373&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset&temperature_unit=fahrenheit&windspeed_unit=mph&timezone=America%2FChicago&forecast_days=1'
    extra_weather_response = requests.get(extra_weather_url)

    air_quality_url = 'https://air-quality-api.open-meteo.com/v1/air-quality?latitude=42.0664&longitude=-87.9373&hourly=us_aqi&timezone=America%2FChicago'
    air_quality_response = requests.get(air_quality_url)

    def get_air_quality():
        air_quality = air_quality_response.json()
        current_time = dt.datetime.now().strftime("%Y-%m-%dT%H:00")
        hourly_times = air_quality["hourly"]["time"]

        try:
            target_index = hourly_times.index(current_time)
        except ValueError:
            return None

        aqi_values = air_quality["hourly"]["us_aqi"]
        aqi_value = aqi_values[target_index]
        aqi_category = ''

        match aqi_value:
            case value if value <= 50:
                aqi_category = 'Good'
            case value if value >= 51 and value <= 100:
                aqi_category = 'Moderate'
            case value if value >= 101 and value <= 150:
                aqi_category = 'Unhealty for sensitive groups'
            case value if value >= 151 and value <= 200:
                aqi_category = 'Unhealthy'
            case value if value >= 201 and value <= 300:
                aqi_category = 'Very Unhealthy'
            case value if value >= 301 and value <= 500:
                aqi_category = 'Hazardous'
            case _:
                aqi_category = ''

        return f"{aqi_value} {aqi_category}"

    if weather_response.status_code == 200 and extra_weather_response.status_code == 200 and air_quality_response.status_code == 200:
        weather = weather_response.json()
        extra_weather = extra_weather_response.json()

        weather_data = {
            'temperature': f"{weather['current']['temperature']}°",
            'weather_description': weather['current']['weather_descriptions'][0],
            'precip': f"{weather['current']['precip']}",
            'uv_index': f"{weather['current']['uv_index']}",
            'wind': f"{weather['current']['wind_speed']}mph {weather['current']['wind_dir']}",
            'visibility': weather['current']['visibility'],
            'humidity': weather['current']['humidity'],
            'pressure': weather['current']['pressure'],
            'feelslike': f"{weather['current']['feelslike']}°",
            'high_low': f"{extra_weather['daily']['temperature_2m_max'][0]}°/{extra_weather['daily']['temperature_2m_min'][0]}°",
            'sunrise': format_date(extra_weather['daily']['sunrise'][0], 'hour'),
            'sunset': format_date(extra_weather['daily']['sunset'][0], 'hour'),
            'air_quality': get_air_quality()
        }

        return weather_data
    
    else :
        return {}
    
def get_forecast_data():
    url = 'https://api.open-meteo.com/v1/forecast?latitude=42.0664&longitude=-87.9373&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max,precipitation_probability_max,windspeed_10m_max&temperature_unit=fahrenheit&windspeed_unit=mph&timezone=America%2FChicago&forecast_days=14'
    api_response = requests.get(url)
    forecast_data = []
    
    if api_response.status_code == 200:
        forecast = api_response.json()
        
        for day in range(len(forecast['daily']['time'])):
            forecast_data.append({
                'day': format_date(forecast['daily']['time'][day], 'day'),
                'high_low': f"{forecast['daily']['temperature_2m_max'][day]}°/{forecast['daily']['temperature_2m_min'][day]}°",
                'sunrise': format_date(forecast['daily']['sunrise'][day], 'hour'),
                'sunset': format_date(forecast['daily']['sunset'][day], 'hour'),
                'uv_index': forecast['daily']['uv_index_max'][day],
                'precip': f"{forecast['daily']['precipitation_probability_max'][day]}%",
                'wind_speed': f"{forecast['daily']['windspeed_10m_max'][day]} mph"
            })
            
        return forecast_data

    else:
        return []
    
def format_date(date_str, with_format):
    if with_format == 'day':
        date_obj = dt.datetime.strptime(date_str, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%A, %b %d')

        return formatted_date
    elif with_format == 'hour':
        date_obj = dt.datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        formatted_date = date_obj.strftime('%I:%M %p')

        return formatted_date
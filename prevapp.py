import requests
from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

API_KEY = "9c73fe3d75a19e7a79f2fe4b3d836f75"  # Replace with your own API key
DATA_FILE = 'weather_data.json'

def save_to_json(data):
    """Saves weather data to a JSON file."""
    try:
        # Load existing data (if any)
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                all_weather_data = json.load(f)
        else:
            all_weather_data = []

        # Append new data to the existing list
        all_weather_data.append(data)

        # Save the updated data back to the JSON file
        with open(DATA_FILE, 'w') as f:
            json.dump(all_weather_data, f, indent=4)
    except Exception as e:
        print(f"Error saving data to file: {e}")

def get_weather_by_location(lat, lon, unit='metric'):
    """Fetch the current weather details from OpenWeather API using latitude and longitude."""
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units={unit}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        main_data = data['main']
        weather_data = data['weather'][0]
        wind_data = data['wind']

        city_name = data['name']
        temperature = main_data['temp']
        humidity = main_data['humidity']
        description = weather_data['description']
        wind_speed = wind_data['speed']
        icon = f"wi wi-{weather_data['icon']}"

        return {
            'city_name': city_name,
            'temperature': temperature,
            'humidity': humidity,
            'description': description.capitalize(),
            'wind_speed': wind_speed,
            'icon': icon
        }
    else:
        return None

def get_forecast_by_location(lat, lon, unit='metric'):
    """Fetch the 5-day weather forecast from OpenWeather API using latitude and longitude."""
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units={unit}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        forecast_dict = {}

        for entry in data['list']:
            date_str = entry['dt_txt'].split(" ")[0]  # Get only the date part
            temp = entry['main']['temp']
            description = entry['weather'][0]['description']
            icon = f"wi wi-{entry['weather'][0]['icon']}"

            if date_str not in forecast_dict:
                forecast_dict[date_str] = {
                    'temperature': temp,
                    'description': description,
                    'icon': icon,
                    'count': 1
                }
            else:
                forecast_dict[date_str]['temperature'] += temp
                forecast_dict[date_str]['count'] += 1
        
        forecast_list = []
        for date, details in forecast_dict.items():
            avg_temp = details['temperature'] / details['count']
            forecast_list.append({
                'date': date,
                'temperature': round(avg_temp, 2),
                'description': details['description'],
                'icon': details['icon']
            })

        return forecast_list[:5]
    else:
        return None

@app.route('/')
def index():
    """Render the main HTML page."""
    return render_template('index.html')

@app.route('/get_weather')
def get_weather_route():
    """Handle city weather requests."""
    city = request.args.get('city')
    unit = request.args.get('unit', 'metric')  # Default to metric
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={unit}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        main_data = data['main']
        weather_data = data['weather'][0]
        wind_data = data['wind']

        city_name = data['name']
        temperature = main_data['temp']
        humidity = main_data['humidity']
        description = weather_data['description']
        wind_speed = wind_data['speed']
        icon = f"wi wi-{weather_data['icon']}"

        weather_info = {
            'city_name': city_name,
            'temperature': temperature,
            'humidity': humidity,
            'description': description.capitalize(),
            'wind_speed': wind_speed,
            'icon': icon
        }

        forecast_info = get_forecast_by_location(data['coord']['lat'], data['coord']['lon'], unit)

        # Save current weather and forecast data to the JSON file
        save_to_json({
            'current_weather': weather_info,
            'forecast': forecast_info,
            'average_temperature': 0,  # Placeholder if data is not available
            'temp_std_dev': 0         # Placeholder if data is not available
        })

        return jsonify({
            'current_weather': weather_info,
            'forecast': forecast_info,
            'average_temperature': 0,  # Placeholder if data is not available
            'temp_std_dev': 0         # Placeholder if data is not available
        })
    else:
        return jsonify({'error': 'City not found or invalid request'}), 404

@app.route('/get_weather_by_location')
def get_weather_by_location_route():
    """Handle geolocation requests.""" 
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    unit = request.args.get('unit', 'metric')  # Default to metric
    
    weather_info = get_weather_by_location(lat, lon, unit)
    forecast_info = get_forecast_by_location(lat, lon, unit)
    
    if weather_info and forecast_info:
        # Save current weather and forecast data to the JSON file
        save_to_json({
            'current_weather': weather_info,
            'forecast': forecast_info,
            'average_temperature': 0,  # Placeholder if data is not available
            'temp_std_dev': 0         # Placeholder if data is not available
        })

        return jsonify({
            'current_weather': weather_info,
            'forecast': forecast_info,
            'average_temperature': 0,  # Placeholder if data is not available
            'temp_std_dev': 0         # Placeholder if data is not available
        })
    else:
        return jsonify({'error': 'Unable to fetch weather data for the given location'}), 404

if __name__ == '__main__':
    app.run(debug=True)

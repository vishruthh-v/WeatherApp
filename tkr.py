import tkinter as tk
import requests

# Your OpenWeather API Key
API_KEY = "9c73fe3d75a19e7a79f2fe4b3d836f75"  # Replace with your own API key

def get_weather(city):
    """Fetch the weather details from OpenWeather API."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
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
        
        # Return the weather information
        return city_name, temperature, humidity, description, wind_speed
    else:
        return None

def display_weather():
    """Fetch and display weather information."""
    city = city_entry.get()
    weather_info = get_weather(city)
    
    if weather_info:
        city_name, temperature, humidity, description, wind_speed = weather_info
        result_label.config(text=f"Weather in {city_name}:\n"
                                f"Temperature: {temperature}°C\n"
                                f"Humidity: {humidity}%\n"
                                f"Description: {description.capitalize()}\n"
                                f"Wind Speed: {wind_speed} m/s")
        result_frame.pack(pady=20, fill='x')  # Show the result frame with fixed size and spacing
    else:
        result_label.config(text="City not found. Please try again.")
        result_frame.pack_forget()  # Hide the result frame if city not found

# Set up the Tkinter window
root = tk.Tk()
root.title("Weather App")
root.geometry("1280x720")  # Set the fixed size of 1280x720
root.config(bg="#f0f8ff")  # Light blue background

# Disable window resizing
root.resizable(False, False)

# Create a main frame to contain the input and result sections
main_frame = tk.Frame(root, bg="#f0f8ff")
main_frame.pack(pady=50, expand=True)

# Create a frame for the input section
top_frame = tk.Frame(main_frame, bg="#f0f8ff")
top_frame.pack(side="top", pady=20, expand=True)

# City input field and label
city_label = tk.Label(top_frame, text="Enter City Name:", font=("Arial", 18), bg="#f0f8ff")
city_label.pack(pady=10)

city_entry = tk.Entry(top_frame, font=("Arial", 14), width=20, bd=2, relief="solid")
city_entry.pack(pady=10)  # Padding for the Entry widget

# Button to fetch weather data
search_button = tk.Button(top_frame, text="Get Weather", font=("Arial", 16), command=display_weather, 
                           bg="#4CAF50", fg="white", relief="raised", padx=20, pady=10)
search_button.pack(pady=20)

# Create a result frame that will display weather data with a fixed size of 500x500
result_frame = tk.Frame(main_frame, bg="#ffffff", bd=5, relief="solid", width=500, height=500)
result_label = tk.Label(result_frame, text="", font=("Arial", 16), bg="#ffffff")
result_label.pack(padx=20, pady=20)

# Initially hide the result frame
result_frame.pack_forget()

# Run the Tkinter event loop
root.mainloop()

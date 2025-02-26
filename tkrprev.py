import tkinter as tk
from PIL import Image, ImageTk  # Import Pillow's Image and ImageTk modules
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

def on_focus_in(event):
    """Clear the placeholder text when the user clicks in the entry box."""
    if city_entry.get() == "Enter the city name":
        city_entry.delete(0, tk.END)

def on_focus_out(event):
    """Restore the placeholder text if the entry box is empty."""
    if city_entry.get() == "":
        city_entry.insert(0, "Enter the city name")

# Set up the Tkinter window
root = tk.Tk()
root.title("Weather App")
root.geometry("1000x700")  # Set the fixed size of 1280x720
root.config(bg="#f0f8ff")  # Light blue background

# Disable window resizing
root.resizable(False, False)

# Load and resize the logo image using Pillow
image = Image.open("icons/logo.png")  # Open the image with Pillow
image = image.resize((50, 50))  # Resize the image to 50x50 pixels
logo = ImageTk.PhotoImage(image)  # Convert the resized image to Tkinter-compatible format

# Create a Label widget to display the logo at the top-left corner
logo_label = tk.Label(root, image=logo, bg="#f0f8ff")
logo_label.place(x=10, y=10)  # Position logo in the top-left corner with a 10px margin

# Create a Label widget for the text next to the logo (Text Box)
app_name_label = tk.Label(root, text="Weather App", font=("Arial", 24, "bold"), bg="#f0f8ff")
app_name_label.place(x=70, y=15)  # Position the text box next to the logo (adjust y for alignment)

# Create a main frame to contain the input and result sections
main_frame = tk.Frame(root, bg="#f0f8ff")
main_frame.pack(pady=50, expand=True)

# Create a frame for the input section
top_frame = tk.Frame(main_frame, bg="#f0f8ff")
top_frame.pack(side="top", pady=20, expand=True)

# City input field and label
city_label = tk.Label(top_frame, text="Get Accurate and Realtime Predictions", font=("Calibri", 18), bg="#f0f8ff")

city_label.pack(pady=10)

# Placeholder text is set when the Entry widget is initialized
city_entry = tk.Entry(top_frame, font=("Caliri", 14), width=20, bd=2, relief="solid")
city_entry.insert(0, "Enter the city name")  # Set the placeholder text
city_entry.bind("<FocusIn>", on_focus_in)  # When the user clicks in the entry box
city_entry.bind("<FocusOut>", on_focus_out)  # When the user clicks out of the entry box
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

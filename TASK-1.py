import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox

# OpenWeatherMap API Details
API_KEY = "7a387891c7b9737314f8484357e00c40"
BASE_URL_WEATHER = "https://api.openweathermap.org/data/2.5/weather"

# Function to fetch weather data
def fetch_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # Use metric units for temperature in Celsius
    }
    response = requests.get(BASE_URL_WEATHER, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["description"]
        }
    else:
        raise ValueError("Could not fetch weather data. Please check the city name.")

# Function to display weather data and create visualization
def display_weather():
    city = city_entry.get()
    if not city.strip():
        messagebox.showerror("Input Error", "Please enter a city name.")
        return
    
    try:
        weather_data = fetch_weather(city)
        result_label.config(
            text=f"City: {weather_data['city']}\n"
                 f"Temperature: {weather_data['temperature']}°C\n"
                 f"Humidity: {weather_data['humidity']}%\n"
                 f"Condition: {weather_data['condition'].capitalize()}"
        )
        
        # Visualization
        labels = ["Temperature (°C)", "Humidity (%)"]
        values = [weather_data["temperature"], weather_data["humidity"]]
        
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.bar(labels, values, color=["blue", "green"])
        ax.set_title(f"Weather in {weather_data['city']}")
        ax.set_ylabel("Values")
        ax.set_ylim(0, max(values) + 10)
        
        # Embed Matplotlib chart in Tkinter
        for widget in chart_frame.winfo_children():
            widget.destroy()  # Clear any existing chart
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Create Tkinter window
root = tk.Tk()
root.title("Weather Dashboard")
root.geometry("600x500")

# City Input
city_label = tk.Label(root, text="Enter City Name:", font=("Arial", 14))
city_label.pack(pady=10)
city_entry = tk.Entry(root, font=("Arial", 14), width=30)
city_entry.pack(pady=5)

# Fetch Weather Button
fetch_button = tk.Button(root, text="Get Weather", font=("Arial", 14), command=display_weather)
fetch_button.pack(pady=10)

# Result Display
result_label = tk.Label(root, text="", font=("Arial", 12), justify="left")
result_label.pack(pady=10)

# Chart Frame
chart_frame = tk.Frame(root)
chart_frame.pack(pady=20)

# Run Tkinter event loop
root.mainloop()

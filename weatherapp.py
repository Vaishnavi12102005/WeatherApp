import requests
import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import logging

# Configure Logging
logging.basicConfig(filename="weather_app.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

# API Configuration
API_KEY = "69759590e0d4ef41d751b1aeb7687097"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Database Setup
def setup_database():
    try:
        conn = sqlite3.connect("weather_history.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            city TEXT,
                            temperature REAL,
                            humidity REAL,
                            wind_speed REAL,
                            timestamp TEXT
                        )''')
        conn.commit()
        conn.close()
        logging.info("Database setup completed.")
    except sqlite3.Error as e:
        logging.error(f"Database setup failed: {e}")

# Save Data to Database
def save_to_database(city, temperature, humidity, wind_speed):
    try:
        conn = sqlite3.connect("weather_history.db")
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO history (city, temperature, humidity, wind_speed, timestamp) VALUES (?, ?, ?, ?, ?)",
                       (city, temperature, humidity, wind_speed, timestamp))
        conn.commit()
        conn.close()
        logging.info(f"Weather data for {city} saved to database.")
    except sqlite3.Error as e:
        logging.error(f"Failed to save data to database: {e}")

# Fetch Weather Data
def get_weather_data(city):
    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            weather_info = {
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"]
            }
            save_to_database(city, weather_info["temperature"], weather_info["humidity"], weather_info["wind_speed"])
            return weather_info
        else:
            logging.warning(f"API error: {response.status_code}, {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return None

# GUI Setup
def display_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    weather = get_weather_data(city)
    if weather:
        result_label["text"] = (f"Weather in {city}:\n"
                                f"Temperature: {weather['temperature']} °C\n"
                                f"Humidity: {weather['humidity']}%\n"
                                f"Wind Speed: {weather['wind_speed']} m/s")
    else:
        messagebox.showerror("Error", "Could not fetch weather data. Please try again.")

# Generate Report
def generate_report():
    try:
        conn = sqlite3.connect("weather_history.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM history")
        rows = cursor.fetchall()
        with open("weather_report.txt", "w") as file:
            file.write("Weather History Report\n")
            file.write("=" * 50 + "\n")
            for row in rows:
                file.write(f"City: {row[1]}, Temperature: {row[2]} °C, Humidity: {row[3]}%, "
                           f"Wind Speed: {row[4]} m/s, Timestamp: {row[5]}\n")
        conn.close()
        messagebox.showinfo("Report Generated", "Weather report has been saved to 'weather_report.txt'.")
        logging.info("Weather report generated successfully.")
    except sqlite3.Error as e:
        logging.error(f"Failed to generate report: {e}")

# Display History in GUI
def view_history():
    try:
        conn = sqlite3.connect("weather_history.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM history")
        rows = cursor.fetchall()
        history_text.delete("1.0", tk.END)
        if rows:
            for row in rows:
                history_text.insert(tk.END, f"City: {row[1]}, Temp: {row[2]} °C, Humidity: {row[3]}%, "
                                            f"Wind: {row[4]} m/s, Time: {row[5]}\n")
        else:
            history_text.insert(tk.END, "No history found.")
        conn.close()
    except sqlite3.Error as e:
        logging.error(f"Failed to fetch history: {e}")
        messagebox.showerror("Error", "Could not fetch history. Please try again.")

# Main Application
setup_database()

# Tkinter GUI
app = tk.Tk()
app.title("Weather Application")
app.geometry("500x600")

# UI Elements
city_label = tk.Label(app, text="Enter City:")
city_label.pack(pady=5)

city_entry = tk.Entry(app, width=30)
city_entry.pack(pady=5)

fetch_button = tk.Button(app, text="Fetch Weather", command=display_weather)
fetch_button.pack(pady=10)

result_label = tk.Label(app, text="", font=("Arial", 12))
result_label.pack(pady=20)

report_button = tk.Button(app, text="Generate Report", command=generate_report)
report_button.pack(pady=10)

history_label = tk.Label(app, text="Weather History:")
history_label.pack(pady=10)

history_text = tk.Text(app, height=15, width=50)
history_text.pack(pady=10)

view_history_button = tk.Button(app, text="View History", command=view_history)
view_history_button.pack(pady=10)

# Run the Application
app.mainloop()

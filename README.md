# Weather Application in Python

## Overview
This project is a Python-based weather application that connects to a public weather API (e.g., OpenWeatherMap or WeatherStack). Users can input a location (city name or coordinates) to fetch real-time weather data, including temperature, humidity, and wind speed. The weather information is displayed in a user-friendly format.

## Features
- **User Interface**: Console-based interface for input and output. Optionally, a GUI can be built using Tkinter.
- **Functionality**:
  - Fetches real-time weather data from a public API.
  - Displays temperature, humidity, and wind speed.
  - Handles invalid inputs gracefully.
- **Reports** (Optional):
  - Generates logs of performed operations.
  - Saves data into a text file or database.

## Technologies Used
- **Python**: Core logic and functionality.
- **Requests**: For API calls.
- **Tkinter (Optional)**: GUI interface.
- **SQLite (Optional)**: Data storage for history.
- **Logging**: Error handling and logging of calculations.

## Setup & Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/your-repo/weather-app.git
   cd weather-app
   ```
2. Install required dependencies:
   ```sh
   pip install requests tkinter sqlite3 pandas
   ```
3. Get an API key from OpenWeatherMap or WeatherStack.
4. Update the `config.py` file with your API key:
   ```python
   API_KEY = "your_api_key_here"
   ```
5. Run the application:
   ```sh
   python main.py
   ```

## Usage
1. Enter a city name or coordinates.
2. The application fetches real-time weather data.
3. The results are displayed in the console or GUI.
4. Optional: View past queries from the SQLite database.

## Checklist
- [x] Design system with error handling.
- [x] Implement functionality to fetch and display weather data.
- [x] Optional: Implement GUI using Tkinter.
- [x] Optional: Implement a history feature using SQLite.
- [x] Test application with various inputs.
- [x] Submit completed project files and documentation.

## Deliverables
- Complete Python project files.
- A Python script for running the application.
- Documentation detailing functionality, usage, and setup.

## License
This project is licensed under the MIT License.

## Contact
For any questions or contributions, contact [vaishnavick05@gmail.com].

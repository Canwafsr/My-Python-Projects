import sys
import requests
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

# OpenWeatherMap API key
API_KEY = "YOUR_API_KEY"
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'

class WeatherFetcher:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_weather(self, city_name):
        
        # Fetches weather data for the given city from OpenWeatherMap API.
        
        complete_url = BASE_URL + "q=" + city_name + "&appid=" + self.api_key + "&units=metric"
        response = requests.get(complete_url)
        data = response.json()

        # If city is not found
        if data['cod'] == '404':
            return None, None

        # Extracting required information from the response
        main = data['main']
        weather = data['weather'][0]
        wind = data['wind']
        clouds = data['clouds']
        sys = data['sys']

        temperature = main['temp']
        feels_like = main['feels_like']
        temp_min = main['temp_min']
        temp_max = main['temp_max']
        pressure = main['pressure']
        humidity = main['humidity']
        weather_description = weather['description']
        weather_icon = weather['icon']
        wind_speed = wind['speed']
        wind_deg = wind['deg']
        cloudiness = clouds['all']
        country = sys['country']
        sunrise = datetime.fromtimestamp(sys['sunrise']).strftime('%H:%M:%S')
        sunset = datetime.fromtimestamp(sys['sunset']).strftime('%H:%M:%S')

        # Formatting weather information
        weather_info = (
            f"City: {city_name}, {country}\n"
            f"Temperature: {temperature}°C\n"
            f"Feels Like: {feels_like}°C\n"
            f"Min Temperature: {temp_min}°C\n"
            f"Max Temperature: {temp_max}°C\n"
            f"Pressure: {pressure} hPa\n"
            f"Humidity: {humidity}%\n"
            f"Weather: {weather_description}\n"
            f"Wind Speed: {wind_speed} m/s\n"
            f"Wind Direction: {wind_deg}°\n"
            f"Cloudiness: {cloudiness}%\n"
            f"Sunrise: {sunrise}\n"
            f"Sunset: {sunset}"
        )

        return weather_info, weather_icon

class WeatherApp(QWidget):
    def __init__(self, weather_fetcher):
        super().__init__()
        self.weather_fetcher = weather_fetcher
        self.initUI()

    def initUI(self):
        
        # Initializes the UI components of the application.
        
        self.setWindowTitle('Weather App')
        self.setGeometry(500, 200, 500, 300)

        main_layout = QVBoxLayout()

        # City input layout
        city_layout = QHBoxLayout()
        self.city_label = QLabel('City name:')
        city_layout.addWidget(self.city_label)
        self.city_entry = QLineEdit()
        city_layout.addWidget(self.city_entry)
        main_layout.addLayout(city_layout)

        # Button to show weather
        self.show_button = QPushButton('Show Weather')
        self.show_button.clicked.connect(self.show_weather)
        main_layout.addWidget(self.show_button, alignment=Qt.AlignCenter)

        # Image label for weather icon
        self.image_label = QLabel(self)
        main_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        # Label to display weather information
        self.weather_label = QLabel(self)
        self.weather_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.weather_label, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    def show_weather(self):
        """
        Fetches and displays the weather information for the entered city.
        """
        city_name = self.city_entry.text()
        weather_info, weather_icon = self.weather_fetcher.get_weather(city_name)
        if weather_info:
            self.weather_label.setText(weather_info)
            # Fetch and display the weather icon
            icon_url = f"http://openweathermap.org/img/wn/{weather_icon}@2x.png"
            image = QPixmap()
            image.loadFromData(requests.get(icon_url).content)
            self.image_label.setPixmap(image)
        else:
            QMessageBox.warning(self, "Error", "City not found.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_fetcher = WeatherFetcher(API_KEY)
    ex = WeatherApp(weather_fetcher)
    ex.show()
    sys.exit(app.exec_())

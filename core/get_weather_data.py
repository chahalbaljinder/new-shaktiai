import requests

city_name = "New Delhi"
API_KEY = 'aeb88e64cde7325df7186b541539cd42'
url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    main = data['main']
    wind = data['wind']
    weather = data['weather'][0]
    
    temperature = main['temp']
    pressure = main['pressure']
    humidity = main['humidity']
    wind_speed = wind['speed']
    description = weather['description']
    
    print(f"Temperature: {temperature}°C")
    print(f"Pressure: {pressure} hPa")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed} m/s")
    print(f"Weather Description: {description.capitalize()}")
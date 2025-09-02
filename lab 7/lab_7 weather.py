import requests

def get_weather(city_name, api_key):
    try:
        data = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                'q': city_name,
                'appid': api_key,
                'units': 'metric',
                'lang': 'ru'
            }
        ).json()
        
        print(f"\nПогода в {city_name}:")
        print(f"Температура: {data['main']['temp']}°C")
        print(f"Давление: {data['main']['pressure']} ")
        print(f"Влажность: {data['main']['humidity']}%")
       
        
    except Exception as e:
        print("Ошибка:", e)

get_weather(input("Город: "), "9deb9df930984bc4fdf1c672b78ff9c3")
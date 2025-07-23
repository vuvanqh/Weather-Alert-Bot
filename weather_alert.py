import pandas, requests, os, datetime

data_file = 'data.csv'
api_key = os.environ['OpenWeather_api_key']
bot_token = os.environ['Terry_tbot_token']
bot_id = os.environ['Terry_tbot_id']
lat = 52.2297
lon = 21.0122

if not os.path.exists(data_file):
    with open(data_file, 'w'):
        pandas.DataFrame(columns=['user_id', 'name', 'lat', 'lon']).to_csv(data_file)

def get_weather_message(latitude: float = lat, longitude: float = lon) -> str: #Warsaw by default
    call5 = f"https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
    response = requests.get(call5)
    response.raise_for_status()
    message = "Have a nice day and stay hydrated! 🧋\n"
    for i in range(0, 8):
        code = int(response.json()['list'][i]['weather'][0]['id'])
        if code in range(500, 600):
            message = "It's going to rain today. Remember to bring an umbrella ☔︎︎\n"
        elif code in range(600, 700):
            message = "It's going to snow today. Be careful and Merry Christmas ⋆꙳•❅‧*₊⋆☃︎‧*❆₊⋆\n"
        elif code in range(200, 300):
            message = "There's going to be a thunderstorm today. Be careful and stay safe ⛈️\n"
    return message

def terry_tbot_send():
    df = pandas.read_csv(data_file)
    for _,row in df.iterrows():
        message = get_weather_message(float(row['lat']),float(row['lon']))
        try:
            text = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={row['user_id']}&parse_mode=Markdown&text={message}"
            bot_response = requests.get(text)
            bot_response.raise_for_status()
        except Exception as e:
            log(e)

def log(message):
    with open('logs.txt','a') as file:
        file.write(f'[{datetime.datetime.now()}]: {message}\n')

if __name__ == "__main__":
    terry_tbot_send()
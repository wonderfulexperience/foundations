import requests
import json
import time

def send_message(this_message, this_subject, this_API):
    return requests.post(
        "https://api.mailgun.net/v3/sandbox1b96f86f57274a0b85260981f5da32f6.mailgun.org/messages",
        auth=("api", this_API),
        data={"from": "Alexander Trentin <postmaster@sandbox1b96f86f57274a0b85260981f5da32f6.mailgun.org>",
              "to": "[redacted]",
              "subject": this_subject,
              "text": this_message})

def get_weather(this_API):
   
    latitude= '40.806290'
    longitude = '-73.963005'
    link_DarkSky = 'https://api.darksky.net/forecast/'+this_API+\
    '/'+latitude+","+longitude+"?exclude=['hourly','minutely','flags']&units=si"

    response = requests.get(link_DarkSky)
    weather_data = response.json()
    
    temperature = weather_data['currently']['temperature']
    summary = weather_data['currently']['summary']
    high_temp = weather_data['daily']['data'][0]['temperatureMax']
    low_temp = weather_data['daily']['data'][0]['temperatureMin']
    if float(high_temp) > 30:
        temp_feeling = "hot"
    elif float(high_temp) > 20:
        temp_feeling = "warm"
    elif float(high_temp) > 10:
        temp_feeling = "moderate"
    else:
        temp_feeling = "cold"

    rain_check = weather_data['daily']['data'][0]['precipType']
    rain_warning = ""
    if rain_check == 'rain':
        rain_warning = " Bring your umbrella!"

    weather_message = "Right now it is "+str(int(round(temperature,0)))\
    +" degrees celsius and " + summary.lower()\
    + ". Today will be "+temp_feeling+" with a high of "+str(int(round(high_temp,0)))\
    + " degrees and a low of "+str(int(round(low_temp,0)))\
    + "." + rain_warning
    
    return weather_message

my_API_DarkSky = '[redacted]'
my_message = get_weather(my_API_DarkSky)

this_time = time.strftime("%I %p")
this_date = time.strftime("%B %d, %Y")

my_API_mailgun = "[redacted]"
my_subject = this_time + " weather forecast: "+ this_date

send_message(my_message, my_subject, my_API_mailgun)
import requests
val = input('Enter city: ')
url =  'http://wttr.in/{}'.format(val)
response = requests.get(url)
weather_data = response.text
print(weather_data)
run = True
while run:
    pass
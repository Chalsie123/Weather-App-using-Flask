from flask import Flask, redirect, render_template, request, url_for
import requests
import geocoder
from datetime import datetime
import flag
import config

app = Flask(__name__)
api_key = Your API Key

weather = {}

def changetime(sec_time):
    return datetime.fromtimestamp(sec_time).strftime("%d %b %Y | %I:%M:%S %p")

def settemp(temp):
    return str("{:.2f}".format(temp- 273.15))+" (\u00B0C)"

def setloc(loc):
    return f"{loc}\u00B0"

# def setflag(coun):
#     coun_flag = flag.flag(coun)
#     print(coun_flag)
    # return coun+coun_flag

def getdata(weather_data_city):
    curr_loc = f"https://api.openweathermap.org/data/2.5/weather?q={weather_data_city}&appid={api_key}"
    curr_loc_data = requests.get(curr_loc).json()
    weatherdata = curr_loc_data['name']
    # curr_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")
    weather['Longitude'] = setloc(curr_loc_data['coord']['lon'])
    weather['Latitude'] = setloc(curr_loc_data['coord']['lat'])
    weather['Country'] = curr_loc_data['sys']['country']
    weather['Current Temperature'] = settemp(curr_loc_data['main']['temp'])
    weather['Maximum Temperature'] = settemp(curr_loc_data['main']['temp_max'])
    weather['Minimum Temperature'] = settemp(curr_loc_data['main']['temp_min'])
    weather['Weather Description'] = curr_loc_data['weather'][0]['description'].capitalize()
    weather['Humidity'] = str(curr_loc_data['main']['humidity'])+"%"
    weather['Wind Speed'] = str(curr_loc_data['wind']['speed']) + " miles/hour"
    weather['Pressure'] = str(curr_loc_data['main']['pressure'])+" hpa"
    weather['Visibility'] = str(curr_loc_data['visibility'])+" m"
    weather['Cloud Level'] = str(curr_loc_data['clouds']['all'])+"%"
    # rain_level_1h = curr_loc_data['rain']['1h']
    # rain_level_3h = curr_loc_data['rain']['3h']
    # snow_level_1h = curr_loc_data['snow']['1h']
    # snow_level_3h = curr_loc_data['snow']['3h']
    weather['Sunrise Time'] = changetime(curr_loc_data['sys']['sunrise'])
    weather['Sunset Time'] = changetime(curr_loc_data['sys']['sunset'])
    id = curr_loc_data["id"]

    return (weather, weatherdata, id)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method=="POST":
        city = request.form['cityname']
        return redirect(url_for('searchcity', cityname=city))
    
    weather_data = geocoder.ip('me')
    weather_data_city = weather_data.city
    weather, city_name, city_id = getdata(weather_data_city)
    return render_template('index.html', weather=weather, city_name=city_name, city_id=city_id)
    

@app.route("/weather/<cityname>", methods=['GET', 'POST'])
def searchcity(cityname):
    if request.method=="POST":
        cit = request.form['cityname']
        return redirect(url_for('searchcity', cityname=cit))

    weather, city_name, city_id = getdata(cityname)
    return render_template('index.html', weather=weather, city_name=city_name, city_id=city_id)

if __name__=="__main__":
    app.run(debug=True)

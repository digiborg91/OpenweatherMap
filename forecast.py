from bottle import route, request, debug, run, template, static_file, redirect
import sqlite3, urllib2, datetime, json

# places = {'Dublin': [53.3498, -6.2603], #use to re add places
#           'Belfast': [54.5973, -5.9301],
#           'Cork': [51.8969, -8.4863],
#           'Athlone': [53.4239, -7.9407],
#           'Limerick': [52.6680, -8.6305],
#           'Galway': [53.2707, -9.0568],
#           'Waterford': [52.2993, -7.1101],
#           'Donegal': [54.6538, -8.1096],
#           'Armagh': [54.3503, -6.6528],
#           'Derry': [54.9966, -7.3086],
#           'Coleraine': [55.1326, -6.6646],
#           'Tralee': [52.2713, -9.6999],
#           'Sligo': [54.2766, -8.4761]
#           }

places = {}


def databasebuilder():
    global places
    places = {}
    connect = sqlite3.connect('forecast.db')
    cursor = connect.cursor()
    cursor.execute("SELECT name ,latitude, longitude FROM Locations")
    locationname = cursor.fetchall()
    for row in locationname:
        places[row[0]] = [row[1], row[2]]
    connect.commit()
    cursor.close()
    connect.close()
    #print places


def url_builder(endpoint, lat, lon):
    # as previous (including modification from c4.3.1)
    user_api = '2975d8fae93d5fb86bc1e9f0349a3500'
    unit = 'metric'  # For Fahrenheit use imperial, for Celsius use metric, and the default is Kelvin.
    mode = 'json'
    return 'http://api.openweathermap.org/data/2.5/' + endpoint + \
           '?mode=' + mode + \
           '&units=' + unit + \
           '&APPID=' + user_api + \
           '&lat=' + str(lat) + \
           '&lon=' + str(lon)


def fetch_data(full_api_url):
    # as previous
    url = urllib2.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    return json.loads(output)


def time_converter(timestamp):
    # as previous
    return datetime.datetime.fromtimestamp(timestamp).strftime('%d %b %I:%M %p')


def convertCoordinates(lat, lon):
    mapWidth, mapHeight = 540, 700
    leftLon, rightLon = -10.663, -5.428
    topLat, bottomLat = 55.384, 51.427
    lonRange = abs(leftLon - rightLon)
    latRange = abs(topLat - bottomLat)
    result = []
    result.append(int(round(abs(mapWidth * ((abs(leftLon) - abs(lon)) / lonRange)))))
    result.append(int(round(abs(mapHeight * ((abs(topLat) - abs(lat)) / latRange)))))
    return result


def getForecastData():
    global places
    databasebuilder()
    connect = sqlite3.connect('forecast.db')
    cursor = connect.cursor()
    cursor.execute("DELETE FROM forecasts")
    for place in places:
        json_data = fetch_data(url_builder('forecast', places[place][0], places[place][1]))
        for forecast in json_data['list']:
            temperature = int(round(forecast['main']['temp'], 0))
            symbol = forecast['weather'][0]['icon']
            timestamp = forecast['dt']
            cursor.execute("INSERT INTO forecasts(location, temperature, symbol, timestamp) VALUES(?,?,?,?)",
                           (place, temperature, symbol, timestamp))
    connect.commit()

    cursor.execute("SELECT DISTINCT timestamp FROM forecasts ORDER BY timestamp ASC")
    timestamps = cursor.fetchall()
    mapData = []
    timestampData = []
    for timestamp in timestamps:
        cursor.execute("SELECT * FROM forecasts WHERE timestamp = ?", (timestamp[0],))
        allLocationData = cursor.fetchall()
        singleMapData = []
        for locationData in allLocationData:
            place = locationData[1]
            symbol = locationData[3]
            imageCoords = convertCoordinates(places[place][0], places[place][1])
            symbolURL = "http://openweathermap.org/img/w/" + symbol + ".png"
            singleMapData.append([imageCoords[0], imageCoords[1], symbolURL, locationData[2], place])
        mapData.append(singleMapData)
        timestampData.append(time_converter(timestamp[0]))
    cursor.close()
    connect.close()
    return mapData, timestampData


# mapData = []
# forecastData = []
mapData, timestampData = getForecastData()


@route('/manage')
def choosePlace():
    global places, timestampData
    databasebuilder()
    return template('manage.tpl', places=places, timestampData=timestampData)
    # change back to options.tpl if errors exist


@route('/showWeatherMap')
def choosePlace():
    return template('showWeatherMap.tpl')


@route('/addPlace', method='post')
def addPlace():
    connect = sqlite3.connect("forecast.db")
    cursor = connect.cursor()

    newPlace = request.forms.get('name')
    latitude = request.forms.get('latitude')
    longitude = request.forms.get('longitude')
    cursor.execute("INSERT INTO Locations(name, latitude, longitude) Values(?,?,?)",(newPlace, latitude, longitude))
    connect.commit()
    cursor.close()
    connect.close()
    databasebuilder()
    redirect("/manage")


@route('/images/<ireland>')
def send_image(ireland):
    return static_file(ireland, root='./images/')


@route('/')
@route('/<id>')
def showMap(id=0):
    global mapData, timestampData
    databasebuilder()
    mapData, timestampData = getForecastData()
    id = int(id)
    prev = id - 1 if id > 0 else id
    next = id + 1 if id < len(mapData) - 1 else len(mapData) - 1
    # print mapData[id]
    return template('showWeatherMap.tpl', mapData=mapData[id], timestampData=timestampData[id], prev=prev, next=next)


databasebuilder()
mapData, timestampData = getForecastData()
debug(True)
run(reloader=True)

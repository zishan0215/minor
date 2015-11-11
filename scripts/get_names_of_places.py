import os
import sqlite3
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from time import sleep

def execute_query(line, lines):
    geolocator = Nominatim()
    latlon = line[1:3]

    try:
        location = geolocator.reverse(latlon, language='en')
        print(location.raw['address']['postcode'])
        line[6] = location.address
        lines.append(line)
    except GeocoderTimedOut:
        sleep(10)
        execute_query(line, lines)
    except GeocoderServiceError:
        sleep(10)
        execute_query(line, lines)

def get_names():
    cur_path = os.getcwd()
    path = cur_path[:-7] + "data/"
    os.chdir(path)

    lines = []

    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    query = "SELECT * FROM PLACES limit 1"

    for line in c.execute(query):
        execute_query(list(line), lines)

    # for line in lines:
    #     new_query = "UPDATE places SET name = '" + line[6] + "' WHERE id = " + str(line[0])
    #     c.execute(new_query)
    #     conn.commit()

    conn.close()
    os.chdir(cur_path)

if __name__ == '__main__':
    get_names()
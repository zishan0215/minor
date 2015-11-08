from functions import get_folder
import os
import sqlite3

def weights():
    cur_path = os.getcwd()
    path = cur_path[:-7] + "data/"
    os.chdir(path)
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    query = "SELECT * FROM places"

    places = [list(place) for place in c.execute(query)]
    print(len(places))

    for u in range(0, 1):
        user = get_folder(u)
        query = "SELECT * FROM master" + user
        for location in c.execute(query):
            location = list(location)
            if location in places:
                index = places.index(location)
                places[index][5] += 1
    for place in places:
        pass
    conn.close()
    os.chdir(cur_path)

if __name__ == '__main__':
    weights()

from functions import get_folder
import os
import sqlite3
import time

def weights():
    print("Assigning weights to places. Process started at: " + time.ctime())
    start_time = time.time()
    cur_path = os.getcwd()
    path = cur_path[:-7] + "data/"
    os.chdir(path)

    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    query = "SELECT * FROM places"
    places = []
    t_places = []
    for place in c.execute(query):
        place = list(place)
        places.append(place)
        t_places.append(place[1:5])

    for u in range(0, 120):
        user = get_folder(u)
        query = "SELECT * FROM master" + user
        for location in c.execute(query):
            location = list(location[1:])
            if location in t_places:
                index = t_places.index(location)
                places[index][5] += 1
        print("Processed user: " + user)

    print("Processed all users. Updating the database...")
    for place in places:
        if place[5] != 0:
            query = "UPDATE places SET weight = " + str(place[5]) + " WHERE id = " + str(place[0])
            c.execute(query)
            conn.commit()

    conn.close()
    os.chdir(cur_path)
    print("Database updated.")
    end_time = time.time()
    total_time = (end_time - start_time) / 60
    print("Process completed at " + time.ctime())
    print("Total running time: " + str(total_time) + " minutes")

if __name__ == '__main__':
    weights()

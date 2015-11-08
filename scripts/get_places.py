from functions import get_distance, get_folder
import os
import sqlite3
import time

def find_place(places, line):
    '''
    :param places:
    :param line:
    :return: Return true if the the distance between the coordinates is within 15 meters from any coordinate in places
    '''
    if len(places) == 0:
        return False
    low = 0
    high = len(places)
    while low <= high:
        mid = int((low + high)/2)
        if get_distance(places[mid], line) <= 15:
            return False
        else:
            high = mid - 1
    # for p in places:
    #     if get_distance(p, line) < 15:
    #         return False
    return True

def get_places():
    cur_path = os.getcwd()
    path = cur_path[:-7] + "data/"
    os.chdir(path)
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    places = []
    query = "SELECT * FROM places"
    for line in c.execute(query):
        places.append(line[1:5])
    for u in range(40, 50):
        user = get_folder(u)
        query = "SELECT * FROM master" + user
        lines = []
        now = time.time()
        for line in c.execute(query):
            lines.append(line[1:])
        for line in lines:
            if line not in places:
                if not find_place(places, line):
                    c.execute("INSERT INTO places(latitude, longitude, dated, timed) VALUES (?, ?, ?, ?)", line)
                    places.append(line)
            if time.time() - now > 60:
                print("Processing user: ", user)
                now = time.time()
        print("User: ", user)
        print("Num Places: ", len(places))
        print("Num Lines", len(lines))
        conn.commit()
    conn.close()
    os.chdir(cur_path)

if __name__ == '__main__':
    get_places()

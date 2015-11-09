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
        line = list(line[1:5])
        if len(places) == 0:
            line.append(0)
        else:
            line.append(get_distance(line, places[0]))
            places.append(line)

    for u in range(0, 120):
        user = get_folder(u)
        query = "SELECT * FROM master" + user
        lines = []
        now = time.time()
        for line in c.execute(query):
            line = list(line[1:])
            if len(places) == 0:
                line.append(0)
            else:
                line.append(get_distance(line, places[0]))
            lines.append(line)
        for line in lines:
            if line not in places:
                if not find_place(places, line):
                    if line[4] == 0 and len(places) != 0:
                        line[4] = get_distance(line, places[0])
                    places.append(line)
                    # print(line)
            if time.time() - now > 60:
                print("Processing user: ", user)
                print("Line: ", line)
                now = time.time()
        print("User: ", user)
        print("Num Places: ", len(places))
        print("Num Lines", len(lines))

        places.sort(key=lambda place: place[4])

        query = "DELETE FROM places"
        c.execute(query)
        query = "DELETE FROM sqlite_sequence WHERE NAME = 'places'"
        c.execute(query)

        for place in places:
            c.execute("INSERT INTO places(latitude, longitude, dated, timed) VALUES (?, ?, ?, ?)", place[0:4])
            print(place[0:4])
        conn.commit()
    conn.close()
    os.chdir(cur_path)

if __name__ == '__main__':
    get_places()

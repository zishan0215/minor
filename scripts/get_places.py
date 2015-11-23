from functions import get_distance, get_folder, change_path_to_data, back_to_path, get_minutes
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

def places_using_time():
    cur_path = change_path_to_data()
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    initial = []
    final = []
    added_to_final = True
    added_to_initial = False
    for u in range(0, 1):
        user = get_folder(u)
        query = "SELECT * FROM master" + user
        last = []
        for line in c.execute(query):
            line = list(line)
            line[4] = line[4][:-1]
            # print(line)
            if added_to_initial:
                if get_minutes(line[4], last[4]) > 10:
                    # print("adding to final: ", line)
                    final.append(line)
                    added_to_final = True
                    added_to_initial = False
                    continue
            if added_to_final:
                # print("adding to initial: ", line)
                initial.append(line)
                added_to_initial = True
                added_to_final = False
            last = line
        if added_to_initial:
            final.append(last)

    # print(len(initial))
    # print(len(final))

    for i in range(0, len(initial) - 1):
        values = [initial[i][0], final[i][0]]
        query = "INSERT INTO finit VALUES({},{})".format(initial[i][0], final[i][0])
        c.execute(query)

    conn.commit()
    conn.close()
    back_to_path(cur_path)

def get_places_by_date_time():
    cur_path = change_path_to_data()
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # Get all dates from the database
    query = "SELECT DISTINCT dated FROM master000"
    dates = []
    for line in c.execute(query):
        dates.append(line[0])

    places = []

    # For each date in the database, get all the locations and extract places based on 10 minute difference
    for d in dates:
        query = "SELECT * FROM master000 WHERE dated = '" + str(d) + "'"
        # print(query)
        prev = 0
        for line in c.execute(query):
            line = list(line)
            line[4] = line[4][:-1]
            if prev == 0:
                # print(line, prev)
                places.append(line)
                prev += 1
            else:
                minutes = get_minutes(places[prev-1][4], line[4])
                # print(minutes)
                if minutes > 15:
                    # print(line, minutes, prev)
                    places.append(line)
                    prev += 1

    # Remove entries from new_places table
    query = "DELETE FROM new_places"
    c.execute(query)
    query = "DELETE FROM sqlite_sequence WHERE NAME = 'new_places'"
    c.execute(query)

    for place in places:
        c.execute("INSERT INTO new_places(latitude, longitude, dated, timed) VALUES (?, ?, ?, ?)", place[1:])
        print(place[0:4])

    conn.commit()
    conn.close()
    back_to_path(cur_path)

if __name__ == '__main__':
    # get_places()
    # places_using_time()
    get_places_by_date_time()
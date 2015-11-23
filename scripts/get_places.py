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

def find_place_linear(places, p):
    for i in range(len(places)):
        distance = get_distance(places[i][1:3], p[1:3])
        if distance <= 15:
            return i

    return -1

def get_places_by_date_time():
    cur_path = change_path_to_data()
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    new_places = []

    for u in range(0, 5):
        user = get_folder(u)

        # Get all dates from the database
        query = "SELECT DISTINCT dated FROM master" + user      # 6367 for 000, 256 for 001
        dates = []
        for line in c.execute(query):
            dates.append(line[0])

        places = []

        # places.append([172042, 39.955832, 116.329224, '2009-07-05', '04:44:31'])
        # For each date in the database, get all the locations and extract places based on 10 minute difference
        for d in dates:
            query = "SELECT * FROM master" + user + " WHERE dated = '" + str(d) + "'"
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
                        distance = get_distance(places[prev-1][1:3], line[1:3])
                        if distance > 20:
                            if line not in places:
                                # line.append(1)
                                # print(line, minutes, distance)
                                places.append(line)
                                prev += 1

        # Add entries to new_places
        initial = len(new_places)
        if len(new_places) == 0:
            for p in places:
                p.append(1)
                new_places.append(p)
        else:
            for p in places:
                index = find_place_linear(new_places, p)
                if index == -1:
                    p.append(1)
                    new_places.append(p)
                else:
                    new_places[index][5] += 1

        print("User: ", user)
        print("Number of places: ", len(places))
        print("Number of places added: ", len(new_places) - initial)

    # print(new_places)
    print("Total new places: ", len(new_places))
    # Remove entries from new_places table
    query = "DELETE FROM new_places"
    c.execute(query)
    query = "DELETE FROM sqlite_sequence WHERE NAME = 'new_places'"
    c.execute(query)

    for place in places:
        c.execute("INSERT INTO new_places(latitude, longitude, dated, timed, weight) VALUES (?, ?, ?, ?, ?)", place[1:6])
        # print(place[0:4])

    conn.commit()
    conn.close()
    back_to_path(cur_path)

if __name__ == '__main__':
    # get_places()
    # places_using_time()
    get_places_by_date_time()
from functions import get_distance, get_folder
import os
import sqlite3

def find_place(places, line):
    '''
    :param places:
    :param line:
    :return: Return true if the the distance between the coordinates is within 15 meters from any coordinate in places
    '''
    if len(places) == 0:
        return False
    for p in places:
        if get_distance(p, line) < 15:
            return False
    return True

def places():
    cur_path = os.getcwd()
    path = cur_path[:-7] + "data/"
    os.chdir(path)
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    places = []
    query = "SELECT * FROM places"
    for line in c.execute(query):
        places.append(line)
    for fol in range(9, 20):                        # 0-19 done
        folder = get_folder(fol)
        query = "SELECT * FROM master" + folder
        lines = []
        for line in c.execute(query):
            lines.append(line)
        for line in lines:
            if line not in places:
                if not find_place(places, line):
                    c.execute("INSERT INTO places VALUES (?, ?, ?, ?)", line)
                    places.append(line)
        print("Num Places: ", len(places))
        print("Num Lines", len(lines))
        conn.commit()
    conn.close()
    os.chdir(cur_path)

if __name__ == '__main__':
    places()

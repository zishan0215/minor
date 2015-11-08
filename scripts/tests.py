from functions import get_distance
import os
import sqlite3

def test_places():
    cur_path = os.getcwd()
    path = cur_path[:-7] + "data/"
    os.chdir(path)
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    places = []
    distances = []
    query = "SELECT * FROM places LIMIT 10"
    for line in c.execute(query):
        places.append(line[1:5])
    for place in places:
        distance = get_distance(place, places[0])
        distances.append(distance)
    if all(distances[i] <= distances[i+1] for i in range(len(distances)-1)):
        print("Its sorted :D")
    else:
        print("Not sorted.")

if __name__ == '__main__':
    test_places()

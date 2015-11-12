from functions import get_distance, change_path_to_data, back_to_path
import sqlite3

def test_places():
    cur_path = change_path_to_data()
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    places = []
    distances = []
    query = "SELECT * FROM places"
    for line in c.execute(query):
        places.append(line[1:5])
    for place in places:
        distance = get_distance(place, places[0])
        distances.append(distance)
    if all(distances[i] <= distances[i+1] for i in range(len(distances)-1)):
        print("Its sorted :D")
    else:
        print("Not sorted.")
    back_to_path(cur_path)

def test_distance():
    cur_path = change_path_to_data()

    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    places = []
    distances = []
    query = "SELECT * FROM master000"
    for line in c.execute(query):
        places.append(list(line))

    for place in places:
        place.append(get_distance(place[1:], places[0][1:]))

    places.sort(key=lambda place: -place[5])

    count = 0
    for place in places:
        print(str(place[0]) + ": " + str(place[5]))
        count += 1
        if count == 20:
            break

    back_to_path(cur_path)

if __name__ == '__main__':
    # test_places()
    test_distance()
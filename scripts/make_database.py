from functions import get_folder
import os
import sqlite3

def master():
    cur_path = os.getcwd()
    path = "/home/zishan/development/minor/data/"
    os.chdir(path)
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    for fol in range(1, 182):
        folder = get_folder(fol)
        path = "/home/zishan/development/minor/data/"
        path += folder
        os.chdir(path)
        table_name = "master" + folder
        query = "CREATE TABLE IF NOT EXISTS " + table_name + " (latitude real, longitude real, dated date, timed time)"
        c.execute(query)
        with open("master.csv", "r") as f:
            for line in f:
                line = line.split(",")
                c.execute("INSERT INTO " + table_name + " values (?, ?, ?, ?)", line)
                print(line)
    conn.commit()
    conn.close()
    os.chdir(cur_path)

if __name__ == '__main__':
    master()
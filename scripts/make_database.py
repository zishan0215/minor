from functions import get_folder, change_path_to_data, back_to_path
import os
import sqlite3

def master():
    cur_path = os.getcwd()
    path = cur_path[:-7] + "data/"
    os.chdir(path)
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    for fol in range(0, 182):
        folder = get_folder(fol)
        path = "/home/zishan/development/minor/data/"
        path += folder
        os.chdir(path)
        table_name = "master" + folder
        query = "CREATE TABLE IF NOT EXISTS " + table_name + ''' (id integer primary key autoincrement not null,
                  latitude real not null, longitude real not null, dated date not null, timed time not null)'''
        c.execute(query)
        with open("master.csv", "r") as f:
            for line in f:
                line = line.split(",")
                c.execute("INSERT INTO " + table_name + "(latitude, longitude, dated, timed) values (?, ?, ?, ?)", line)
                print(line)
    conn.commit()
    conn.close()
    os.chdir(cur_path)

def place():
    cur_path = os.getcwd()
    path = cur_path[:-7] + "data/"
    os.chdir(path)
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    query = '''CREATE TABLE IF NOT EXISTS places (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                latitude REAL NOT NULL, longitude REAL NOT NULL, dated DATE NOT NULL,
                timed TIME NOT NULL, weight INTEGER NOT NULL DEFAULT 0)
            '''
    c.execute(query)
    conn.commit()
    conn.close()
    os.chdir(cur_path)

def alter_places():
    cur_path = os.getcwd()
    path = cur_path[:-7] + "data/"
    os.chdir(path)
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    query = "ALTER TABLE places ADD COLUMN name TEXT"
    c.execute(query)
    conn.commit()
    conn.close()
    os.chdir(cur_path)

def create_finit():
    cur_path = change_path_to_data()
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    query = "CREATE TABLE IF NOT EXISTS finit (initial INTEGER NOT NULL, final INTEGER NOT NULL)"
    c.execute(query)
    conn.commit()
    conn.close()
    back_to_path(cur_path)

if __name__ == '__main__':
    # master()
    # place()
    # alter_places()
    create_finit()

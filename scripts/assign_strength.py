from functions import get_distance, get_folder
import os

def find_place(line):
    pass

def strength():
    cur_path = os.getcwd()
    places = []
    lines = []
    for fol in range(0, 1):
        folder = get_folder(fol)
        path = "/home/zishan/development/minor/data/"
        path += folder
        os.chdir(path)
        files = os.listdir()
        with open("master.csv", "r") as f:
            for line in f:
                line = line.split(",")[:2]
                lines.append(line)
        for line in lines:
            if line not in places:
                if not find_place(line):
                    places.append(line)
    os.chdir(cur_path)
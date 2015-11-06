from rename_files import get_folder
import os

def master():
    cur_path = os.getcwd()
    for fol in range(0, 182):
        folder = get_folder(fol)
        folder += "/Trajectory/"
        path = "/home/zishan/development/minor/data/"
        path += folder
        os.chdir(path)
        files = os.listdir()
        total_content = ""
        print("Number of files: ", len(files))
        for n in range(1, len(files)+1):
            with open(str(n)+".plt", 'r') as f:
                for i in range(0, 6):
                    f.readline()

                for line in f:
                    line = line.split(',')
                    line = line[:2] + line[5:]
                    content = ','.join(line)
                    # content += '\n'
                    print(content)
                    total_content += content
        folder = get_folder(fol)
        path = "/home/zishan/development/minor/data/"
        path += folder
        os.chdir(path)
        with open("master.csv", 'w') as f:
            f.write(total_content)
        # print(total_content)
        print("Total records: ", len(total_content))
    os.chdir(cur_path)


if __name__ == '__main__':
    master()
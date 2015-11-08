import math

def get_distance(initial, final):
    distance = []
    for i in range(0, len(initial)):
        R = 6371000
        phi1 = math.radians(float(initial[i][0]))
        phi2 = math.radians(float(final[i][0]))
        dphi = math.radians(float(final[i][0]) - float(initial[i][0]))
        dl = math.radians(float(final[i][1]) - float(initial[i][1]))
        a = (math.sin(dphi/2)**2) + (math.cos(phi1) * math.cos(phi2) * math.sin(dl/2)**2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = R * c
        distance.append(d)
    return distance

def get_folder(f):
    if f == 0:
        return "000"
    folder = str(f)
    length = 0
    while f != 0:
        length += 1
        f /= 10
        f = int(f)
    while length != 3:
        folder = "0" + folder
        length += 1
    return folder

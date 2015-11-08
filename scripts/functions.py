import math

def get_distance(initial, final):
    '''
    :param initial (list: [latitide, longitude]):
    :param final (list: [latitide, longitude]):
    :return: distance in meters
    '''
    R = 6371000
    phi1 = math.radians(float(initial[0]))
    phi2 = math.radians(float(final[0]))
    dphi = math.radians(float(final[0]) - float(initial[0]))
    dl = math.radians(float(final[1]) - float(initial[1]))
    a = (math.sin(dphi/2)**2) + (math.cos(phi1) * math.cos(phi2) * math.sin(dl/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d

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

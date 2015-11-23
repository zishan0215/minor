from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from functions import change_path_to_data, back_to_path
import sqlite3

def plot():
    cur_path = change_path_to_data()
    # make sure the value of resolution is a lowercase L,
    #  for 'low', not a numeral 1
    map = Basemap(projection='merc', lat_0=50, lon_0=-100,
                  resolution='h', area_thresh=0.1,
                  # llcrnrlat=39.596377, llcrnrlon=115.08728,
                  # urcrnrlat=40.604778, urcrnrlon=121.107788)
                  llcrnrlat=39.831715, llcrnrlon=116.169605,
                  urcrnrlat=40.144738, urcrnrlon=116.757374)
    # map = Basemap(projection='merc', lat_0=57, lon_0=-135,
    #               resolution='h', area_thresh=0.1,
    #               llcrnrlon=-136.25, llcrnrlat=56,
    #               urcrnrlon=-134.25, urcrnrlat=57.75)

    map.drawcoastlines()
    map.drawcountries()
    # map.fillcontinents(color='coral')
    map.drawmapboundary()

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    # query = "SELECT * FROM master000 WHERE id IN (SELECT initial FROM finit)"
    query = "SELECT * FROM master000 LIMIT 50000"
    # query = "SELECT * FROM new_places"
    lats = []
    lons = []
    labels = []
    for line in c.execute(query):
        lats.append(line[1])
        lons.append(line[2])
        # labels.append(str(line[0]) + " " + str(line[3]) + " " + str(line[4]))
        # lon = -135.3318
        # lat = 57.0799

    x, y = map(lons, lats)
    map.plot(x, y, 'bo', markersize=6)

    # for label, xpt, ypt in zip(labels, x, y):
    #     plt.text(xpt, ypt, label)

    conn.close()
    plt.show()
    back_to_path(cur_path)

if __name__ == '__main__':
    plot()

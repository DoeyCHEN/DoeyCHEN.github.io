import pandas as pd
import numpy as np
from lshash import LSHash

data = pd.read_csv("/Users/cz/Desktop/Traj_1000_SH_UTM.csv")
path = pd.DataFrame()

rec = []
path = np.zeros((1000, 44107))
for index, item in data.iterrows():
    point = (int(item['X']) - 346000) / 20 + (int(item['Y'] - 3448600))/20 * 840

    if point not in rec:
        rec.append(point)
    
    path[int(item['Tid'])-1][rec.index(point)]=1

lsh = LSHash(10, len(rec))
for index in range(0, 1000):
    lsh.index(path[index], index+1)

cmp = [15, 250, 480, 690, 900]
for item in cmp:
    clustre = lsh.query(path[item-1])
    for i in clustre:
        print i[0][1],
    print
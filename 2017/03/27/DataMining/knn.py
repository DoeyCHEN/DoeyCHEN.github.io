import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

data = pd.read_csv("/Users/cz/Desktop/Traj_1000_SH_UTM.csv")
path = pd.DataFrame()

rec = []
path = np.zeros((1000, 44107))
for index, item in data.iterrows():
    point = (int(item['X']) - 346000) / 20 + (int(item['Y'] - 3448600))/20 * 840

    if point not in rec:
        rec.append(point)
    
    path[int(item['Tid'])-1][rec.index(point)]=1

nbrs=NearestNeighbors(n_neighbors=5,algorithm='ball_tree').fit(path)
cmp = [path[14], path[249], path[479], path[689], path[899]]
indices = nbrs.kneighbors(cmp)[1]

for item in indices:
    print item
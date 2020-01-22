import numpy as np
import matplotlib.pyplot as plt
import json


with open("metadata.json") as myL:
    data = json.load(myL)

data_points = [data[x]["weight"] for x in data]

# %matplotlib inline
data_points = np.random.normal(size=100000000)
plt.hist(data_points, density=True, bins=500)
print(sum(data_points) / len(data_points))
plt.ylabel('Probability')
plt.show()

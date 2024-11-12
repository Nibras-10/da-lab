import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv('ktry.csv')
X=df.values

k=int(input("enter the number of clusters"))
centroids=X[np.random.choice(X.shape[0],k,replace=False)]

for i in range(100):
    clusters=[[] for i in range(k)]

    for x in X:
        distance=[np.sqrt(np.sum((x-centroid)**2)) for centroid in centroids]
        cluster=np.argmin(distance)
        clusters[cluster].append(x)

    new_centroid=np.array([np.mean(cluster,axis=0) for cluster in clusters])

    if np.all(centroids==new_centroid):
        break
    centroids=new_centroid

clusters=[np.array(cluster) for cluster in clusters]

for i,c in enumerate(clusters):
    print(f"cluster:{i+1}")
    print(c)
    print()

print("Final centroids")
print(centroids)

for i,cluster in enumerate(clusters):
    plt.scatter(cluster[:, 0],cluster[:, 1],s=100,c='red',label=f'cluster:{i+1}')

plt.scatter(centroids[:, 0],centroids[:, 1],c='blue',s=300, marker='X',label='centroids')
plt.title('K means clustering')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend()
plt.show()


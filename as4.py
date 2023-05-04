import requests
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

url = "https://api.ebird.org/v2/data/obs/US-MD/recent"
key = "5mpno5doc1qv"

params = {
    "maxResults": 1000, 
    "back": 30,  
    "detail": "simple",  
}

response = requests.get(url, headers={"X-eBirdApiToken": key}, params=params)

data = pd.json_normalize(response.json())
print(data)

# select relevant features
selected_features = ["comName", "lat", "lng", "obsDt"]
X = data[selected_features].dropna()
X["obsDt"] = pd.to_datetime(X["obsDt"])
X["dayOfYear"] = X["obsDt"].dt.dayofyear
X["isMigratory"] = X["comName"].str.contains("warbler|vireo|thrush|finch|sparrow", case=False)
X = X[X["isMigratory"]].drop(columns=["comName", "obsDt", "isMigratory"])
X_scaled = StandardScaler().fit_transform(X)

# perform dimensionality reduction using PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# determine optimal number of clusters using elbow method
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(X_pca)
    wcss.append(kmeans.inertia_)
plt.plot(range(1, 11), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.show()

# clustering
kmeans = KMeans(n_clusters=3)
y_pred = kmeans.fit_predict(X_pca)

# visualize clustering results
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y_pred)
plt.title("Clustering Bird Migrations in Maryland")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.show()

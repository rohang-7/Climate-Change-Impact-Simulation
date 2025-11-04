import numpy as np
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler

def run_kmeans(df, k=3, use_cols=None, random_state=42):
    use_cols = use_cols or ["temp_c", "humidity"]
    X = df[use_cols].to_numpy()
    km = KMeans(n_clusters=k, random_state=random_state, n_init="auto")
    labels = km.fit_predict(X)
    return labels

def run_dbscan(df, eps=0.12, min_samples=10, use_cols=None):
    use_cols = use_cols or ["lat","lon"]
    X = df[use_cols].to_numpy()
    Xs = StandardScaler().fit_transform(X)
    db = DBSCAN(eps=eps, min_samples=min_samples)
    labels = db.fit_predict(Xs)
    return labels

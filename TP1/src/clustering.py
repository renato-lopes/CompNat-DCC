from pyclustering.cluster.kmeans import kmeans
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.utils.metric import distance_metric, type_metric

from sklearn.metrics.cluster import v_measure_score

class Metric():
    def __init__(self, tree):
        self.tree = tree
    
    def __call__(self, point1, point2):
        all_points = point1 + point2
        return self.tree.evaluate(all_points)

def cluster_data(X, k, metric):
    custom_metric = distance_metric(type_metric.USER_DEFINED, func=metric)
    
    initial_centers = kmeans_plusplus_initializer(X, k).initialize()

    kmeans_instance = kmeans(X, initial_centers, metric=custom_metric)
    kmeans_instance.process()
    clusters = kmeans_instance.get_clusters()

    return clusters

def compute_fmi(k, clusters, y):
    y_pred = y.copy()
    for i in range(len(clusters)):
        y_pred.loc[clusters[i]] = i+1
    return v_measure_score(y, y_pred)

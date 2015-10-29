# Various plotting and other util functions

from collections import defaultdict
from math import hypot
from operator import itemgetter
from itertools import chain
import math



def clusterise(assignments):
   from collections import defaultdict
   
   clusters = defaultdict(list)
   for i, entry in enumerate(assignments):
       clusters[entry[1]].append((i, entry[0]))

   return clusters


def plot_assignments(cl):
    import matplotlib.pyplot as plt

    clusters = clusterise(cl)
    for k, v in clusters.iteritems():
        xs = list(item[1][0] for item in v)
        ys = list(item[1][1] for item in v)
        
        plt.plot(xs, ys, 'o', label=k)


    plt.legend()
    plt.show()

    
def find_intervals(clusters):
    ## clusters :: ((Float, Float), Int) - output of ml.kmeans
    ## returns :: ((Int, Int), Int)

    def same_cluster(es):
        e, e1 = es
        return e[1] == e1[1]
    
    tpoints = list(i+1 for i, es in enumerate(zip(clusters, clusters[1:]))
                   if not same_cluster(es))

    tpoints = [0] + tpoints + [len(clusters)]

    return list(((p, p1-1), clusters[p][1]) for p, p1 in zip(tpoints, tpoints[1:]))


def merge_clusters(clusters):
    values = []
    for k, v in clusters.iteritems():
        nv = [e + (k, ) for e in v]
        values.append(nv)
        
    events = list(chain(*values))

    events = sorted(events, key=itemgetter(0))

    return list((e[1], e[2]) for e in events)


def calc_mean(cl):
    attrs1 = list(item[1][0] for item in cl)
    attrs2 = list(item[1][1] for item in cl)

    return sum(attrs1)/len(attrs1), sum(attrs2)/len(attrs2)


def dist(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
        
    return hypot(x2 - x1, y2 - y1)


def trim(cl, a):
    avg = calc_mean(cl)
    n = len(cl)
    
    event_dists = sorted(list(event + (dist(event[1], avg), ) for event in cl),
                         key=itemgetter(2))
    cutoff = int(math.ceil(a*n))
    tevent_dists = sorted(event_dists[:(n-cutoff)], key=itemgetter(0))

    return list((event[0], event[1]) for event in tevent_dists)

    
def remove_outliers(cl, a):
    #clusters :: [(Float, Float), Int)] - output of ml.kmeans 
    # a :: Float from 0 to 1
    #
    #returns :: [(Float, Float), Int)]

    clusters = clusterise(cl)
    trimmed_clusters = {}
    
    for k, v in clusters.iteritems():
        trimmed_clusters[k] = trim(v, a)


    return merge_clusters(trimmed_clusters)


        

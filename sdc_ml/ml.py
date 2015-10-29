# Simple kmeans clustering alg. Works for any k but for now it only works in 2-d :/

from operator import itemgetter
import random
from itertools import groupby
from math import hypot


def random_means(dataset, k):
    # Randomly choose k values from dataset as means
    return list(random.choice(dataset) for i in range(k))

    
def make_assignments(dataset, centres):
    assignments = list()
    
    def dist(point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        
        return hypot(x2 - x1, y2 - y1)

    def min_index(A):
        return min(enumerate(A), key=itemgetter(1))[0]
    
    for entry in dataset:
        a = min_index([dist(entry, c) for c in centres])
        assignments.append((entry, a))

    return assignments


def update_centres(assignments, centres):
    get_cl = itemgetter(1)
    classes = sorted(assignments, key=get_cl)
    
    clusters = [list(grp) for k, grp in groupby(classes, get_cl)]

    for i, cl in enumerate(clusters):
        n = len(cl)
        cl1 = sum(item[0][0] for item in cl) / n
        cl2 = sum(item[0][1] for item in cl) / n

        centres[i] = (cl1, cl2)

    return centres


def kmeans(dataset, k):
    centres = random_means(dataset, k)
    assignments = make_assignments(dataset, centres)
    
    for i in range(100):
        centres = update_centres(assignments, centres)
        assignments = make_assignments(dataset, centres)

    return assignments


def main():
    events = sdc.main()
    fevents = sdc.reshape(events)
    a = kmeans(fevents, 4)
    

if __name__ == "__main__":
    main()

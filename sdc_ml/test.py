import data_processing as dp
import ml
import utils
import json


def main():
    json_fn = "data/stephanie_2015_06_21.json"
    
    with open(json_fn) as fin:
        js = json.loads(fin.read())

    events = dp.get_events(js)
    events = dp.select_attrs(events, ["vspeed", "hspeed"])

    clusters = ml.kmeans(events, 4)

    #some tests/post-processing for the clustering
    clusters = utils.remove_outliers(clusters, 0.05)

    intervals = utils.find_intervals(clusters)
    print intervals
    
    #utils.plot(clusters) 

    
if __name__ == "__main__":
    main()

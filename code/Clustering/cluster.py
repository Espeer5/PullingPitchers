""" This module contains all the functions needed to compute and analyze the 
kmeans clustering for the pitching arsenal data. 

Author: Edward Speer
Date: 5/9/23
"""

from Clustering.scraper import collect
import pickle
import statistics
import copy

PICKLEPATH = "../../pickles"


def clean_empt(arsenals):
    """For pitchers who do not throw a certain pitch, automatically defines 
    their metrics for that pitch as 4 deviations less than the population mean
    in order to handle empty values in the dataset.
    
    Arguments: arsenals - A dictionary from the Scraper module mapping pitchers
                          to arsenal data
    """
    for player in arsenals:
        for key in arsenals[player]:
            if arsenals[player][key] == '':
                arsenals[player][key] = -4


def get_ars():
    """Fetches pitching arsenal data from the scraper module, then normalizes 
    and pre-processes that data for clustering via mean standardization"""
    ars = collect()
    vecs = normalize(ars)
    clean_empt(vecs)
    return list(arrays(vecs))


def get_mean(feature, arsenals):
    """ Returns the mean value of the given feature over all pitchers who throw 
    the pitch with the feature in the given arsenals dictionary.

    Arguments: feature - The pitch arsenal feature to take the mean over
               arsenals - A dictionary from the Scraper module mapping pitchers
                          to arsenal data
    """
    total = 0
    occ = 0
    for player in arsenals:
        val = arsenals[player][feature]
        if val != '':
            total += float(val)
            occ += 1
    try:
        return total / occ
    except:
        return 0


def get_std_dev(feature, arsenals):
    """ Returns the standard deviation of the given feature over all pitchers 
    who throw the pitch with the feature in the given arsenals dictionary.

    Arguments: feature - The pitch arsenal feature to take the mean over
               arsenals - A dictionary from the Scraper module mapping pitchers
                          to arsenal data
    """
    vals = []
    for player in arsenals:
        val = arsenals[player][feature]
        if val != '':
            vals.append(float(val))
    try:
        return statistics.stdev(vals)
    except statistics.StatisticsError:
        return .01


def normalize(arsenals):
    """Performs mean normalization of every arsenal feature vector from the 
    arsenals dictionary in order to standardize the metrics for kmeans 
    clustering. This populates each feature in the arsenals dictionary with 
    standard deviations from the norm for each feature.
    
    Arguments: arsenals - A dictionary from the Scraper module mapping pitchers
                          to arsenal data
    """
    vecs = copy.deepcopy(arsenals)
    for feature in arsenals['554430']:
        std_dev = get_std_dev(feature, arsenals)
        mean = get_mean(feature, arsenals)
        for player in vecs:
            val = arsenals[player][feature]
            if val != '':
                vecs[player][feature] = (float(val) - mean) / std_dev
    clean_empt(vecs)
    return vecs
    

def arrays(arsenals):
    """Reformats the pitch arsenal data found in the arsenals dictionary into 
    vectors which may be consumed by kmeans.
    
    Arguments: arsenals - A dictionary from the Scraper module mapping pitchers
                          to arsenal data
    """
    features = []
    for key in arsenals['554430']:
        if key not in ['last_name', ' first_name', 'pitcher']:
            features.append([float(arsenals[player][key]) for player in arsenals])
    return zip(*features)


def get_clusters(arsenals, kmeans):
    """Returns a dictionary mapping the cluster number from the passed kmeans 
    object to the players and arsenal data in that cluster.
    
    Arguments: arsenals - A dictionary from the Scraper module mapping pitchers
                          to arsenal data
               kmeans - The kmeans data structure from which to retrieve the 
                        clusters
    """
    i = 0
    dict = {}
    for player in arsenals:
        dict[arsenals[player]['last_name']] = kmeans.labels_[i]
        i += 1
    return dict


def get_group(arsenals, kmeans, group, clusters):
    """ Retrieves the data for a specified cluster number from the kmeans 
    clustering object of the specified number of clusters
    
    Arguments: arsenals - A dictionary from the Scraper module mapping pitchers
                          to arsenal data
               kmeans - The kmeans data structure from which to retrieve the 
                        clusters
               group - The cluster number to be retrieved from the clustering
               clusters - the number of clusters in the desired clustering
    """
    dict = {i : [] for i in range(clusters)}
    i = 0
    for label in kmeans.labels_:
        dict[label].append(list(arsenals)[i])
        i += 1
    return dict[group]


def get_group_ids(clusters, group):
    """ Get the player ID's of all players in a group from a clustering of
    a given size

    Arguments: clusters: the number of clusters in the clustering 
               group: the group number to get from the clustering
    """
    kmeans = get_pickle(clusters)
    arsenals = collect()
    arsenals = normalize(arsenals)
    clean_empt(arsenals)
    return get_group(arsenals, kmeans, group, clusters)


def to_pickle(kmeans, i):
    """ Saves the kmeans data structure specified to a pickle file to be
    accessed and analyzed in a later session

    Arguments: kmeans - the kmeans data structure to be pickled
               i - the number of clusters in the kmeans object
    """
    with open(f'{PICKLEPATH}/cluster{i}.pickle', 'wb') as pick:
        pickle.dump(kmeans, pick)


def get_pickle(i):
    """Retrieves a kmeans clustering from a pickle file which it was saved to
    
    Arguments: i - the number of clusters in the desired clustering
    """
    with open(f'{PICKLEPATH}/cluster{i}.pickle', 'rb') as pick:
        toRet = pickle.load(pick)
    return toRet

"""
This module contains a series of plotting utilities used to plot clusters 
and their characteristics returned from the kmeans clustering percormed by the
cluster module.

Author: Edward Speer
Date: 5/10/23
"""

from cluster import *
import matplotlib.pyplot as plt

PLTPATH = "../../paper/figs"


def cluster_percG(group, n):
    """Plots the relative frequencies in standard deviation from the mean 
    of how often a cluster of pitchers throws each pitch in a bar chart.

    Arguments: group - The cluster number to be plotted from the clustering
               n - The number of clusters in the desired clustering
    """
    kmeans = get_pickle(n)
    arsenals = collect()
    arsenals = normalize(arsenals)
    clean_empt(arsenals)
    cluster = get_group(arsenals, kmeans, group, n)
    keys = ['n_ff', 'n_si', 'n_fc', 'n_sl', 'n_ch', 'n_cu', 'n_fs', 'n_kn', 'n_st', 'n_sv']
    pct = [0 for key in keys]
    i=0
    for player in cluster:
        j = 0
        for key in keys:
            pct[j] += float(arsenals[player][key])
            if pct[j] == -4:
                pct[j] = 0
            j += 1
        i += 1
    pct = [pct[l] / i for l in range(len(pct))]
    plt.bar(keys, pct)
    plt.title(f'Cluster {group} Pitch Use Percentages')
    with open(f'{PLTPATH}/pct{group}_{n}.png', 'wb') as file:
        plt.savefig(file)
    plt.clf()


def cluster_pcts(max):
    """Saves the cluster pitch frequency bar chart for each group in the 
    specified clustering to pngs.
    
    Arguments: max - The number of clusters in the desired clustering.
    """
    for i in range(max):
        cluster_percG(i, max)


def show_cls_feat(feature, max):
    """ Plots the passed in feature for each cluster in the n-clustering.

    Arguments: feature - The string label for the feature to be plotted 
               max - The number of clusters in the desired clustering
    """
    kmeans = get_pickle(max)
    arsenals = collect()
    arsenals = normalize(arsenals)
    avgs = []
    clean_empt(arsenals)
    for i in range(max):
        avg = 0
        cls = get_group(arsenals, kmeans, i, max)
        j = 0
        for player in cls:
            avg += arsenals[player][feature]
            j += 1
        avg = avg / j
        if avg > -3:
            avgs.append(avg)
        else:
            avgs.append(0)
    plt.bar(range(max), avgs)
    plt.title(f'Average {feature} for Each Cluster')
    plt.xlabel('Cluster')
    plt.ylabel(feature)
    plt.show()


def plot_inertias(max):
    """ Plots the clustering inertia series for each clustering up to the 
    specified clustering as a visualization of the elbow method for determining 
    cluster number.

    Arguments: max - The number of clusters in the desired clustering
    """
    inertias = []
    for i in range(1, max + 1):
        kmeans = get_pickle(i)
        inertias.append(kmeans.inertia_)
    plt.plot(range(1, max + 1), inertias, marker = 'o')
    plt.title("Convergence of Clusters via Elbow Method")
    plt.xlabel("Number of Clusters")
    plt.ylabel("Clustering Inertia")
    plt.show()

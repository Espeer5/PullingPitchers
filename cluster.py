import csv
import pickle
import matplotlib.pyplot as plt
import statistics
import copy

def collect():
    arsenals = {}
    with open("./csvs/pitch_arsenals.csv", "r") as spn:
        spn_rd = csv.DictReader(spn, restval = 0)
        for row in spn_rd:
            arsenals[row['pitcher']] = row
    with open("./csvs/pitch_arsenals_pct.csv", 'r') as pct:
        pct_rd = csv.DictReader(pct, restval = 0)
        for row in pct_rd:
            arsenals[row['pitcher']].update(row)
    with open("./csvs/pitch_arsenals_spd.csv", 'r') as spd:
        spd_rd = csv.DictReader(spd, restval = 0)
        for row in spd_rd:
            arsenals[row['pitcher']].update(row)
    clean_strs(arsenals)
    return arsenals


def clean_strs(arsenals):
    for player in arsenals:
        dict = arsenals[player]
        for str in ['pitcher', ' first_name', 'last_name']:
            dict.pop(str)


def clean_empt(arsenals):
    for player in arsenals:
        for key in arsenals[player]:
            if arsenals[player][key] == '':
                arsenals[player][key] = -4


def get_ars():
    ars = collect()
    vecs = normalize(ars)
    clean_empt(vecs)
    return list(arrays(vecs))


def get_mean(feature, arsenals):
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
    features = []
    for key in arsenals['554430']:
        if key not in ['last_name', ' first_name', 'pitcher']:
            features.append([float(arsenals[player][key]) for player in arsenals])
    return zip(*features)


def to_pickle(kmeans, i):
    with open(f'./pickles/cluster{i}.pickle', 'wb') as pick:
        pickle.dump(kmeans, pick)


def get_clusters(arsenals, kmeans):
    i = 0
    dict = {}
    for player in arsenals:
        dict[arsenals[player]['last_name']] = kmeans.labels_[i]
        i += 1
    return dict


def plot_inertias(max):
    inertias = []
    for i in range(1, max + 1):
        kmeans = get_pickle(i)
        inertias.append(kmeans.inertia_)
    plt.plot(range(1, max + 1), inertias, marker = 'o')
    plt.title("Convergence of Clusters via Elbow Method")
    plt.xlabel("Number of Clusters")
    plt.ylabel("Clustering Inertia")
    plt.show()


def get_group(arsenals, kmeans, group, clusters):
    dict = {i : [] for i in range(clusters)}
    i = 0
    for label in kmeans.labels_:
        dict[label].append(list(arsenals)[i])
        i += 1
    return dict[group]


def get_pickle(i):
    with open(f'./pickles/cluster{i}.pickle', 'rb') as pick:
        toRet = pickle.load(pick)
    return toRet


def cluster_percG(group, n):
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
    with open(f'./paper/figs/pct{group}_{n}.png', 'wb') as file:
        plt.savefig(file)
    plt.clf()
    

def cluster_pcts(max):
    for i in range(max):
        cluster_percG(i, max)
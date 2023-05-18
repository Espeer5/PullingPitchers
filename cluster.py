import csv
import pickle
import matplotlib.pyplot as plt

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
    return arsenals

def clean_empt(arsenals):
    for player in arsenals:
        for key in arsenals[player]:
            if arsenals[player][key] == '':
                arsenals[player][key] = 0


def get_ars():
    ars = collect()
    clean_empt(ars)
    return ars

def arrays(arsenals):
    features = []
    for key in arsenals['554430']:
        if key not in ['last_name', ' first_name', 'pitcher']:
            features.append([float(arsenals[player][key]) for player in arsenals])
    return zip(*features)


def get_clusters(arsenals, kmeans):
    i = 0
    dict = {}
    for player in arsenals:
        dict[arsenals[player]['last_name']] = kmeans.labels_[i]
        i += 1
    return dict

def get_group(arsenals, kmeans, group, clusters):
    dict = {i : [] for i in range(clusters)}
    i = 0
    for label in kmeans.labels_:
        dict[label].append(list(arsenals)[i])
        i += 1
    return dict[group]

def get_pickle(i):
    with open(f'./pickles/cls{i}.pickle', 'rb') as pick:
        toRet = pickle.load(pick)
    return toRet

def cluster_percG(arsenals, group, n):
    kmeans = get_pickle(n)
    cluster = get_group(arsenals, kmeans, group, n)
    keys = ['n_ff', 'n_si', 'n_fc', 'n_sl', 'n_ch', 'n_cu', 'n_fs', 'n_kn', 'n_st', 'n_sv']
    pct = [0 for key in keys]
    i=0
    for player in cluster:
        j = 0
        for key in keys:
            pct[j] += float(arsenals[player][key])
            j += 1
        i += 1
    pct = [pct[l] / i for l in range(len(pct))]
    plt.bar(keys, pct)
    plt.title(f'Cluster {group} Pitch Use Percentages')
    plt.show()
    


if __name__ == '__main__':
    arsenals = collect()
    clean_empt(arsenals)
    cluls = 8
    for i in range(cluls):
        cluster_percG(arsenals, i, cluls)
    # inertias = [get_pickle(i).inertia_ for i in range(1, 13)]
    # plt.plot(range(1, 13), inertias, marker = 'o')
    # plt.title("Convergence of K-Means, Pitchers")
    # plt.xlabel("Number of Clusters")
    # plt.ylabel("Inertia")
    # plt.show()
       

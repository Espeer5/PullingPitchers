import matplotlib.pyplot as plt

def plot_game_series(series):
    plt.plot(range(series.shape[0]), series)
    plt.show()
import Clustering.cluster as cl
import Regression.finder as fn
import Regression.analyze as az
import pickle
import Regression.vizu as v


if __name__ == "__main__":
    with open("temp.pickle", 'rb') as pick:
        events = pickle.load(pick)
    for event in events:
        print(event['inning'])
    print(events[1])
    print(events[1]['pitch_number'])
    velos = az.fb_velo(events[1])
    v.plot_game_series(velos.rolling(10).mean())
    cvs = az.cv_spin(events[1])
    v.plot_game_series(cvs.rolling(10).mean())
    print(velos)
    print(cvs)
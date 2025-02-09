from vis import get_compressed_data
from occupancy_scraper import load_csv
import numpy as np
import pandas as pd
from sklearn.gaussian_process.kernels import RBF
import datetime

class CompressedOccupancy:
    def __init__(self, data):
        pass

class FlattenedOccupancy:
    def __init__(self, df=load_csv()):
        unsorted_times = np.array(dropdates(df['date']))
        times, counts = sortboth(unsorted_times, df['amount'].to_numpy())
        self.times = times
        self.datetimes = datetimes = time2datetime(times)
        self.tmin, self.tmax = datetimes.min(), datetimes.max()
        self.X = normalize_time(datetimes)
        self.counts = self.y = counts
        self.ddates = time2datetime(times)


# class RBF:
#     def __init__(self, gamma):
#         self.gamma = gamma

#     def __call__(self, x, xp):
#         return np.exp(- (x - xp)**2 / self.gamma)

def dropdates(times):
    return np.array([d.time() for d in times])

def time2datetime(times, zero=datetime.date(2018,1,1)):
    return np.array([datetime.datetime.combine(zero,t) for t in times])

def sortboth(x,y):
    sort = np.argsort(x)
    return x[sort], y[sort]

def normalize(x):
    return (x - x.min()) / (x.max()-x.min())

def normalize_time(times):
    tmin = times.min()
    deltas = np.array([(t - tmin).total_seconds() for t in times])
    dtmax = deltas.max()
    return deltas / dtmax

def weighted_mean_std(xs, ws):
    xm = np.average(xs, weights=ws)
    return xm, np.sqrt(np.average((xs - xm)**2, weights=ws))

class OccupancyPredictor:
    def __init__(self, data, gamma=0.05):
        self.data = data
        self.rbf = RBF(gamma)

    def pred_from_normtime(self, x):
        ws = self.rbf(np.array([x]),self.data.X.reshape(-1,1)).reshape(-1)
        ws = ws / ws.sum()
        return weighted_mean_std(self.data.y, ws)

    def pred_from_normtimes(self, x):
        means = []
        stds = []
        for x_i in x:
            xm, xstd = self.pred_from_normtime(x_i)
            means.append(xm)
            stds.append(xstd)

        return np.array(means), np.array(stds)


    def __call__(self, hour, min):
        pass


if __name__ == '__main__':
    pass

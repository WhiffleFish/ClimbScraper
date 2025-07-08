from SpotOccupancy.vis import get_compressed_data
from SpotOccupancy.occupancy_scraper import load_csv
import numpy as np
import pandas as pd
from sklearn.gaussian_process.kernels import RBF
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class CompressedOccupancy:
    def __init__(self, data):
        pass

class FlattenedOccupancy:
    def __init__(self, when='weekday'):
        df = load_csv(when=when)
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

def floats2dt(v, td, t0):
    return t0 + v * td

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

    def plot(self, xs=np.linspace(0, 1, 50), z=1, markeralpha=0.5):
        dts = time2datetime(self.data.times)
        t0 = dts[0]
        td = (dts[-1] - dts[0])
        xs_dt = floats2dt(xs, td, t0)
        xm, xstd = self.pred_from_normtimes(xs)
        fig, ax = plt.subplots(1, 1)
        ax.scatter(floats2dt(self.data.X, td, t0), self.data.y, alpha=markeralpha)
        ax.plot(xs_dt, xm)
        ax.fill_between(
            xs_dt,
            xm - z * xstd,
            xm + z * xstd,
            alpha = 0.5,
        )
        ax.set_ylim(bottom=0)
        fig.axes[0].xaxis.set_major_formatter(mdates.DateFormatter('%H'))
        return fig, ax



if __name__ == '__main__':
    pass

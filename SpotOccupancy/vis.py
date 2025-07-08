import matplotlib.pyplot as plt
from SpotOccupancy.occupancy_scraper import OCCUPANCY_FILE, load_csv
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import datetime
import os

def get_compressed_data():
    df = load_csv()
    dates = df['date'].apply(lambda x : x.date())
    times = df['date'].apply(lambda x: x.time())
    occupancy = df['amount']
    unique_dates = dates.unique()

    times_mat = []
    amts_mat = []
    faux_day = datetime.date(2014, 7, 15)

    for _date in unique_dates:
        mask = dates == _date
        _times = times[mask]
        times_mat.append(np.array([datetime.datetime.combine(faux_day, time) for time in _times]))
        amts_mat.append(occupancy[mask].to_numpy())


    max_len = max(len(x) for x in times_mat)

    def pad(x, l, val=np.nan):
        diff = l - len(x)
        if diff == 0:
            return x
        elif diff > 0:
            return np.concatenate((x,np.full(diff, val)), axis=0)
        else:
            assert False

    times_mat = np.stack([pad(_times, max_len, _times[-1]) for _times in times_mat]).T
    amts_mat = np.stack([pad(_amts, max_len) for _amts in amts_mat]).T
    return times_mat, amts_mat

def show_compressed_data(**kwargs):
    # all days together
    times, amts = get_compressed_data()
    fig, ax = plt.subplots(1, 1, **kwargs)
    ax.plot(times, amts, c='C0')
    fig.axes[0].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    return fig, ax

if __name__ == '__main__':
    fig, ax = show_compressed_data()
    plt.show(block=True)

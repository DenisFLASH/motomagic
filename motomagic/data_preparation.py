# -*- coding  utf-8 -*-

import os
import numpy as np
import pandas as pd


MIN_SPEED = 5  # TODO add to configuration file


def get_trip_ids(folder):
    """
    Read folder, extract trip ids.

    :param folder: path to input folder
    :return: list of str: ids of all trip files found in the folder
    """
    filenames = [fname for fname in os.listdir(folder)]
    return filenames


def load_trip(folder, filename):
    """
    Read file, extract and sensor data.

    :return: pandas.DataFrame of trip's sensor data
    """
    path = os.path.join(folder, filename)
    trip = pd.read_csv(path)
    return trip


def preprocess_trip(trip):
    trip_centered = _subtract_average_accelerations(trip)
    trip_filtered = _filter_data(trip_centered, MIN_SPEED)
    return trip_filtered


def show_distr_ranges_from_data(dfs, cols):
    for col in cols:
        min_list = [df[col].min() for df in dfs]
        max_list = [df[col].max() for df in dfs]
        min_value = min(min_list)
        max_value = max(max_list)
        print("{}. min (among all trips): {}; max (among all trips): {}".format(col, min_value, max_value))


def get_distr_ranges():
    return {'gyroRotationX': (0, 1.5), 'accelerometerAccelerationX': (-2, 2), 'accelerometerAccelerationY': (-1.5, 1.5), 'accelerometerAccelerationZ': (-2.5, 2.5)}
    # TODO fix min a max values for all features, not just some of them
    # TODO parametrize


def _filter_data(df, min_speed):
    """
    Filter trip data using a threshold speed

    :param df:          log data of one trip
    :param min_speed:   speed threshold for filtering
    :return:            filtered dataframe
    """
    filtered = df[(df['locationSpeed'] >= min_speed) & np.isfinite(df['motionRoll'])]
    # TODO speed and motionRoll conditions only? consider other combinations
    return filtered


# TODO 1) which columns exactly? perform tests with Rajesh, find out orientation-dependant columns
# TODO 2) is it a satisfactory method for calibration?
# TODO 3) how to calibrate in case of 10-sec blocks
def _subtract_average_accelerations(df):
    # Center several columns (to have zero average)
    for col in ['accelerometerAccelerationX', 'accelerometerAccelerationY', 'accelerometerAccelerationZ']:
        avg = df[col].mean()
        df[col] = df[col] - avg
        print('\t', col, 'subtracting avg', avg)
    return df



# -*- coding  utf-8 -*-

import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

from motomagic.data_preparation.block import Block


# TODO add to configuration file
MIN_SPEED = 5
BLOCK_SIZE = 10
RATIO_OVER_MIN_SPEED_IN_BLOCK = 0.8


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

    :param df:          log data of one trip/block
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


def _read_datetime(datetime_str):
    return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f")


def split_trip_into_blocks(trip):
    trip_centered = _subtract_average_accelerations(trip)  # TODO validate this step

    block_indices = get_blocks_indices(trip_centered)
    blocks = list()
    for idx_start, idx_end in block_indices:
        #print(idx_start, "...", idx_end)
        block_data = trip[idx_start:idx_end+1].copy().reset_index()
        start_time = block_data['loggingTime'][0][:19]
        filtered_block_data = _filter_data(block_data, MIN_SPEED)
        filtered_ratio = len(filtered_block_data) / len(block_data)
        block = Block(device_id="device_id_123", start_time=start_time, size=BLOCK_SIZE,
                      filtered_ratio=filtered_ratio, data=filtered_block_data)
        if filtered_ratio >= RATIO_OVER_MIN_SPEED_IN_BLOCK:
            blocks.append(block)
            print("block {} added, filter ratio ok: {}".format(block.start_time, block.filtered_ratio))
        else:
            print("block {} ignored, insufficient filter ratio: {}".format(block.start_time, block.filtered_ratio))
    return blocks


def get_blocks_indices(trip):
    trip = trip.copy()
    trip['time'] = np.vectorize(_read_datetime)(trip['loggingTime'])
    N = len(trip)
    block_indices = list()
    idx_start = 0
    max_time = trip.time[N-1]
    while idx_start < N:
        t_start = trip.time[idx_start]
        t_end = t_start + timedelta(0, BLOCK_SIZE, 0)
        if t_end > max_time:
            break
        else:
            for idx in range(idx_start+1, N):
                if trip.time[idx] >= t_end:
                    block_indices.append((idx_start, idx))
                    idx_start = idx+1
                    break
    return block_indices

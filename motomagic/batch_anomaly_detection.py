# -*- coding  utf-8 -*-

import sys

from anomaly_detection import calc_anomaly_scores
from data_preparation import get_trip_ids, load_trip, show_distr_ranges_from_data, split_trip_into_blocks
from tools.database import insert_block

#########################################
#### Create features, plot histograms ###
#########################################


if __name__ == '__main__':


    ########################################
    ###  Load trips into dataframe dict  ###
    ########################################
    DATA_DIR = '../data/new_logger_short/'
    HISTOGRAMS_DIR = '../plots/2017-03/accelerationX_centered_gyroRotationX/'  # TODO parametrize folder name, calculate automatically out of date and feature columns

    trip_ids = get_trip_ids(DATA_DIR)

    #blocks = dict()
    for trip_id in trip_ids:
        trip = load_trip(DATA_DIR, trip_id)
        #trip_clean = preprocess_trip(trip)
        #print("{}: shape {} ==> {} ({:.1f} %) after cleaning"
        #      .format(trip_id, trip.shape[0], trip_clean.shape[0], 100 * trip_clean.shape[0] / trip.shape[0]))
        print("\ntrip", trip_id)
        current_trip_blocks = split_trip_into_blocks(trip)
        for block in current_trip_blocks:
            block_id = block.start_time
            #blocks[block_id] = block
            insert_block(block)
        #trips[trip_id] = trip_clean

    #print('total blocks in dictionary:', len(blocks))
    #block_ids = list(blocks.keys())
    #print(block_ids)

    sys.exit(0)

    #FEATURE_COLS = ['accelerometerAccelerationX', 'accelerometerAccelerationY','accelerometerAccelerationZ']
    #FEATURE_COLS = ['gyroRotationX']  #, 'gyroRotationY','gyroRotationZ']
    #FEATURE_COLS = ['gyroRotationX', 'gyroRotationY','gyroRotationZ', 'motionRotationRateX', 'motionRotationRateY','motionRotationRateZ']
    # TODO select a good combination of feature columns
    FEATURE_COLS = ['accelerometerAccelerationX', 'gyroRotationX']

    show_distr_ranges_from_data(blocks.values(), FEATURE_COLS)

    plot_histograms(blocks, block_ids, FEATURE_COLS, HISTOGRAMS_DIR)

    ######################
    ####  Features #######
    ######################
    X = create_feature_matrix(blocks, block_ids, FEATURE_COLS)
    print("X.shape:", X.shape)



################################
## Anomaly score calculation ###
################################

scores = calc_anomaly_scores(X, block_ids)
with open('../results/sorted_scores_{}_trips.txt'.format(len(trip_ids)), 'w') as scores_file:
    for key, score in scores:
        scores_file.write('{}:   {:.3f}\n'.format(key, score))

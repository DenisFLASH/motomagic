# -*- coding  utf-8 -*-

from data_preparation import get_trip_ids, load_trip, preprocess_trip, show_distr_ranges_from_data, get_distr_ranges
from feature_engineering import plot_histograms, create_feature_matrix
from anomaly_detection import calc_anomaly_scores




#########################################
#### Create features, plot histograms ###
#########################################


if __name__ == '__main__':


    ########################################
    ###  Load trips into dataframe dict  ###
    ########################################
    DATA_DIR = '../data/new_logger/'
    HISTOGRAMS_DIR = '../plots/2017-02/accelerationX_centered_gyroRotationX/'

    trip_ids = get_trip_ids(DATA_DIR)

    trips = dict()
    for trip_id in trip_ids:
        trip = load_trip(DATA_DIR, trip_id)
        trip_clean = preprocess_trip(trip)
        print("{}: shape {} ==> {} ({:.1f} %) after cleaning"
              .format(trip_id, trip.shape[0], trip_clean.shape[0], 100 * trip_clean.shape[0] / trip.shape[0]))
        trips[trip_id] = trip_clean

    print('total trips in dictionary:', len(trips))



    #FEATURE_COLS = ['accelerometerAccelerationX', 'accelerometerAccelerationY','accelerometerAccelerationZ']
    #FEATURE_COLS = ['gyroRotationX']  #, 'gyroRotationY','gyroRotationZ']
    #FEATURE_COLS = ['gyroRotationX', 'gyroRotationY','gyroRotationZ', 'motionRotationRateX', 'motionRotationRateY','motionRotationRateZ']
    # TODO select a good combination of feature columns
    FEATURE_COLS = ['accelerometerAccelerationX', 'gyroRotationX']

    show_distr_ranges_from_data(trips.values(), FEATURE_COLS)

    plot_histograms(trips, trip_ids, FEATURE_COLS, HISTOGRAMS_DIR)

    ######################
    ####  Features #######
    ######################
    X = create_feature_matrix(trips, trip_ids, FEATURE_COLS)
    print("X.shape:", X.shape)



################################
## Anomaly score calculation ###
################################

calc_anomaly_scores(X, trip_ids)

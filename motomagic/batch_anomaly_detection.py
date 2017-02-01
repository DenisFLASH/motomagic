import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.covariance import EllipticEnvelope


# TODO 1) which columns exactly? perform tests with Rajesh, find out orientation-dependant columns
# TODO 2) is it a satisfactory method for calibration?
# TODO 3) how to calibrate in case of 10-sec blocks
def subtract_average_accelerations(df):
    # Center several columns (to have zero average)
    for col in ['accelerometerAccelerationX', 'accelerometerAccelerationY', 'accelerometerAccelerationZ']:
        avg = df[col].mean()
        df[col] = df[col] - avg
        print('\t', col, 'subtracting avg', avg)
    return df


# TODO speed and motionRoll conditions only?
def filter_data(df, min_speed):
    """
    Filter trip data using a threshold speed

    :param df:          log data of one trip
    :param min_speed:   speed threshold for filtering
    :return:            filtered dataframe
    """
    filtered = df[(df['locationSpeed'] >= min_speed) & np.isfinite(df['motionRoll'])]
    return filtered


def calc_hist_values(values, bins):
    # Normalization
    weights = np.ones_like(values) / len(values)
    hist_values, _ = np.histogram(values, bins=bins, weights=weights)
    return hist_values


########################################
###  Load trips into dataframe dict  ### TODO move to data_preparation.py
########################################

# Read folder, create dict of filtered dataframes
DATA_DIR = '../data/new_logger_november_december/'
filenames = [filename for filename in os.listdir(DATA_DIR) if filename.endswith('zip')]
trips = dict()

MIN_SPEED = 5  # TODO add to configuration file

for filename in filenames:
    if 'JEEP' in filename:
        continue

    # Read a single trip into dataframe
    path = os.path.join(DATA_DIR, filename)
    trip = pd.read_csv(path)
    # Data preprocessing
    trip = subtract_average_accelerations(trip)
    # Filter
    trip_filt = filter_data(trip, MIN_SPEED)
    # Add to dictionary
    trip_id = filename.replace('.zip', '')
    trips[trip_id] = trip_filt
    print('{}, shape {} ==> {} ({:.1f} %) after filtering by max_speed'
          .format(trip_id, trip.shape[0], trip_filt.shape[0], 100 * trip_filt.shape[0] / trip.shape[0]))

trip_ids = sorted(trips.keys())
print('total files read:', len(trip_ids))


#########################################
#### Create features, plot histograms ###
#########################################

# TODO fix ranges independently of a seen dataset (it mustn't change from one set of trips to another)
def extract_column_range(all_dfs, col_name):
    min_list = [df[col_name].min() for df in all_dfs]
    max_list = [df[col_name].max() for df in all_dfs]
    return min(min_list), max(max_list)

#feature_columns = ['accelerometerAccelerationX', 'accelerometerAccelerationY','accelerometerAccelerationZ']
#feature_columns = ['gyroRotationX']  #, 'gyroRotationY','gyroRotationZ']
#feature_columns = ['gyroRotationX', 'gyroRotationY','gyroRotationZ', 'motionRotationRateX', 'motionRotationRateY','motionRotationRateZ']
feature_columns = ['accelerometerAccelerationX', 'gyroRotationX']

distr_ranges = dict()
for feature_col in feature_columns:
    min_value, max_value = extract_column_range(trips.values(), feature_col)
    distr_ranges[feature_col] = (min_value, max_value)
print("distr_ranges:", distr_ranges)

# TODO fix min a max values for all features, not just some of them
# Override ranges with custom values for certain columns
distr_ranges['gyroRotationX'] = (0, 1.5)
distr_ranges['accelerometerAccelerationX'] = (-2, 2)
distr_ranges['accelerometerAccelerationY'] = (-1.5, 1.5)
distr_ranges['accelerometerAccelerationZ'] = (-2.5, 2.5)
print("new distr_ranges:", distr_ranges)


######################
####  Features #######  TODO move to feature_engineering.py
######################
N_BINS = 20  # TODO parameter for feature engineering
features_dict = dict()
for trip_id in trip_ids:
    features_dict[trip_id] = dict()
    trip = trips[trip_id]
    print(trip_id, end='\t')

    for feature_col in feature_columns:
        print(feature_col, end='\t')
        col_values = trip[feature_col].values
        col_min_value, col_max_value = distr_ranges[feature_col]
        col_bins = np.linspace(col_min_value, col_max_value, num=N_BINS+1)
        # print('bins:', col_bins)
        col_values_distr = calc_hist_values(col_values, col_bins)
        # print('values_distr:', col_values_distr)
        features_dict[trip_id][feature_col] = col_values_distr
    print()


######################
### Feature matrix ###  TODO move to feature_engineering.py
######################
feature_vectors = list()
for trip_id in trip_ids:
    # Create feature vector for the current trip
    feature_vectors.append(np.hstack(tuple(features_dict[trip_id].values())))

X = np.vstack(feature_vectors)
print("X.shape:", X.shape)

# Histogram set for the each trip
N = len(feature_columns)
# n_feat_to_grid = {2: ()}
a = int(np.ceil(np.sqrt(N)))

for trip_id in trip_ids:

    # Plot a set of histograms for the current trip
    plt.close('all')
    f, axarr = plt.subplots(a, a)
    for feat_index, feat_col in enumerate(feature_columns):

        # calculate plot position on the grid
        col_id = feat_index // a
        row_id = feat_index % a
        feat_values = trips[trip_id][feat_col].values
        col_min_value, col_max_value = distr_ranges[feat_col]
        col_bins = np.linspace(col_min_value, col_max_value, num=N_BINS + 1)
        if N > 1:
            values, bins, _ = axarr[row_id, col_id].hist(feat_values, bins=col_bins,
                                                         weights=np.ones_like(feat_values) / len(feat_values))
            axarr[row_id, col_id].set_title('{}'.format(feat_col))
            axarr[row_id, col_id].set_ylim([0.0, 0.4])
        else:
            values, bins, _ = axarr.hist(feat_values, bins=col_bins,
                                         weights=np.ones_like(feat_values) / len(feat_values))
            axarr.set_title('{}'.format(feat_col))
            axarr.set_ylim([0.0, 0.4])
    out_folder = '../plots/2017-01/accelerationX_centered_gyroRotationX/'
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
        print("folder created", out_folder)
    path = os.path.join(out_folder, '{}.png'.format(trip_id))
    print('saving', path)
    plt.savefig(path)


#########################################
### Dimensionality reduction using PCA ## TODO move to anomaly_detection.py
#########################################
pca = PCA(n_components=2)
X_2D = pca.fit_transform(X)
print("X_2D:", X_2D)

################################
## Anomaly score calculation ### TODO move to anomaly_detection.py
################################
outliers_fraction = 0.15  # TODO parametrize
clf = EllipticEnvelope(contamination=outliers_fraction)
clf.fit(X_2D)
y_pred = clf.predict(X_2D)
scores_pred = clf.decision_function(X_2D)
trip_scores = dict()
for pred, name in zip(scores_pred, trip_ids):
    trip_scores[name] = pred
for key, score in sorted(trip_scores.items(), key=lambda x: x[1]):
    print('{}.csv :   {:.3f}'.format(key, score))

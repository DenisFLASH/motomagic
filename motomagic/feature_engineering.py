# -*- coding  utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt

from data_preparation import get_distr_ranges


N_BINS = 20  # TODO parameter for feature engineering
HIST_Y_LIM = [0.0, 0.4]  # TODO parametrize or calculate for each hist


def calc_hist_values(values, bins):
    # Normalization
    weights = np.ones_like(values) / len(values)
    hist_values, _ = np.histogram(values, bins=bins, weights=weights)
    return hist_values


def create_feature_matrix(trips, trip_ids, feature_cols):
    features_dict = _build_features_dict(trips, trip_ids, feature_cols)
    feature_vectors = list()
    for trip_id in trip_ids:
        # Create feature vector for the current trip
        feature_vectors.append(np.hstack(tuple(features_dict[trip_id].values())))
    X = np.vstack(feature_vectors)
    return X


def _build_features_dict(trips, trip_ids, feature_cols):
    distr_ranges = get_distr_ranges()
    print("distr_ranges (hardcoded):", distr_ranges)

    features_dict = dict()
    for trip_id in trip_ids:
        features_dict[trip_id] = dict()
        trip = trips[trip_id]
        print(trip_id, end='\t')

        for feature_col in feature_cols:
            print(feature_col, end='\t')
            col_values = trip[feature_col].values
            col_min_value, col_max_value = distr_ranges[feature_col]
            col_bins = np.linspace(col_min_value, col_max_value, num=N_BINS + 1)
            # print('bins:', col_bins)
            col_values_distr = calc_hist_values(col_values, col_bins)
            # print('values_distr:', col_values_distr)
            features_dict[trip_id][feature_col] = col_values_distr
        print()

    return features_dict


def plot_histograms(trips, trip_ids, feature_cols, out_folder):
    """
    Histogram set for the each trip
    """
    nb_features = len(feature_cols)
    grid_size = int(np.ceil(np.sqrt(nb_features)))
    distr_ranges = get_distr_ranges()

    for trip_id in trip_ids:

        # Plot a set of histograms for the current trip
        plt.close('all')
        f, axarr = plt.subplots(grid_size, grid_size)
        for feat_index, feat_col in enumerate(feature_cols):

            # calculate plot position on the grid
            col_id = feat_index // grid_size
            row_id = feat_index % grid_size
            feat_values = trips[trip_id][feat_col].values
            col_min_value, col_max_value = distr_ranges[feat_col]
            col_bins = np.linspace(col_min_value, col_max_value, num=N_BINS+1)
            if nb_features > 1:
                # TODO reuse existing method for hist calculation, do not duplicate code
                values, bins, _ = axarr[row_id, col_id].hist(feat_values, bins=col_bins,
                                                             weights=np.ones_like(feat_values) / len(feat_values))
                axarr[row_id, col_id].set_title(feat_col)
                axarr[row_id, col_id].set_ylim(HIST_Y_LIM)
            else:
                values, bins, _ = axarr.hist(feat_values, bins=col_bins,
                                             weights=np.ones_like(feat_values) / len(feat_values))
                axarr.set_title('{}'.format(feat_col))
                axarr.set_ylim([0.0, 0.4])
        if not os.path.exists(out_folder):
            os.makedirs(out_folder)
            print("folder created", out_folder)
        path = os.path.join(out_folder, '{}.png'.format(trip_id))
        print('saving', path)
        plt.savefig(path)

from sklearn.covariance import EllipticEnvelope
from sklearn.decomposition import PCA


OUTLIER_FRACTION = 0.15  # TODO parametrize


def calc_anomaly_scores(X, trip_ids):
    X_PCA = _feature_matrix_PCA(X, 2)
    clf = EllipticEnvelope(contamination=OUTLIER_FRACTION)
    clf.fit(X_PCA)
    # y_pred = clf.predict(X_PCA)
    scores_pred = clf.decision_function(X_PCA)

    trip_scores = dict()
    for pred, name in zip(scores_pred, trip_ids):
        trip_scores[name] = pred
    for key, score in sorted(trip_scores.items(), key=lambda x: x[1]):
        print('{}.csv :   {:.3f}'.format(key, score))



def _feature_matrix_PCA(X, n_dim=2):
    #########################################
    ### Dimensionality reduction using PCA ##
    #########################################
    pca = PCA(n_components=n_dim)
    X_PCA = pca.fit_transform(X)
    print("X_PCA.shape:", X_PCA.shape)
    print("X_PCA:", X_PCA)
    return X_PCA


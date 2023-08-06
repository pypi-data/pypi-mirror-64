import numpy as np
import pandas as pd

from sklearn.base import TransformerMixin, BaseEstimator

from collections import Counter

import eif


class OutlierIQR(TransformerMixin, BaseEstimator):
    """
    Documentation:
        Description:
            identifies outliers using inter_quartile range method.
        Parameters:
            outlier_count : int
                minimum number of values across all features that need to be outliers
                in order for an observation to be flagged.
            iqr_step : float
                multiplier that controls level of sensitivity of outlier detection method.
                higher values for iqr_step will cause OutlierIQR to only detect increasingly
                extreme values.
            features : list
                list of features to be evaluated for outliers.
            drop_outliers : bool, default=False
                if True, drops outliers from the input data.
        Returns:
            x : array
                dataset with outlier observations removed.
    """

    def __init__(self, outlier_count, iqr_step, features, drop_outliers=False):
        self.outlier_count = outlier_count
        self.iqr_step = iqr_step
        self.features = features
        self.drop_outliers = drop_outliers

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        outlier_indices = []

        # iterate over features(columns)
        for col in self.features:
            q1 = np.percentile(X[col], 25)
            q3 = np.percentile(X[col], 75)
            iqr = q3 - q1

            # outlier step
            outlier_step = self.iqr_step * iqr

            # determine a list of indices of outliers for feature col
            outlier_list_col = X[
                (X[col] < q1 - outlier_step) | (X[col] > q3 + outlier_step)
            ].index

            # append the found outlier indices for col to the list of outlier indices
            outlier_indices.extend(outlier_list_col)

        # select observations containing more than 'outlier_count' outliers
        outlier_indices = Counter(outlier_indices)

        self.outliers = list(
            k for k, v in outlier_indices.items() if v >= self.outlier_count
        )

        if self.drop_outliers:
            X = X.drop(self.outliers, axis=0).reset_index(drop=True)

        return X


class ExtendedIsoForest(TransformerMixin, BaseEstimator):
    """
    Documentation:
        Description:
            identifies outliers using extended isolation forest method.
        Parameters:
            columns : list
                columns to be evaluated by extended isolation forest
            n_trees : int
                number of trees to be used.
            sample_size : int
                sub_sample size for creating each trees. values must be smaller that input dataset
                row count.
            ExtensionLevel : int
                degrees of freedom for choosing hyperplanes that divide data. value must be smaller
                than input dataset column count.
            anomalies_ratio : float
                percent of input dataset observations to identify as outliers.
            drop_outliers : bool, default=False
                dictates whether identified outliers are removed from input dataset.
        Returns:
            x : array
                dataset with outlier observations removed.
    """

    def __init__(
        self,
        columns,
        n_trees,
        sample_size,
        extension_level,
        anomalies_ratio,
        drop_outliers=False,
    ):
        self.columns = columns
        self.n_trees = n_trees
        self.sample_size = sample_size
        self.extension_level = extension_level
        self.anomalies_ratio = anomalies_ratio
        self.drop_outliers = drop_outliers

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        ext_iso = eif.iForest(
            X=X[self.columns].values,
            ntrees=self.n_trees,
            sample_size=self.sample_size,
            ExtensionLevel=self.extension_level,
        )

        # calculate anomaly scores
        anomaly_scores = ext_iso.compute_paths(X_in=X[self.columns].values)

        anomaly_scores_sorted = pd.DataFrame(
            anomaly_scores, index=X.index, columns=["anomaly score"]
        ).sort_values(["anomaly score"], ascending=False)

        self.outliers = np.array(
            anomaly_scores_sorted[
                : int(np.ceil(self.anomalies_ratio * X.shape[0]))
            ].index
        )

        if self.drop_outliers:
            X = X.drop(self.outliers, axis=0).reset_index(drop=True)

        return X


def outlier_summary(self, iqr_outliers, if_outliers, eif_outliers):
    """
    Documentation:
        Description:
            creates Pandas DataFrame summarizing which observations were flagged
            as outliers and by which outlier detection method each observation was
            identified.
        Parameters:
            iqr_outliers : array
                array contains indexes of observations identified as outliers using
                iqr method.
            if_outliers : array
                array contains indexes of observations identified as outliers using
                isolition forest method.
            eif_outliers : array
                array contains indexes of observations identified as outliers using
                extended isolition forest method.
        Returns:
            outlier_summary : Pandas DataFrame
                DataFrame summarizing outlier
    """
    # merge and de_duplicate outlier index values
    outlier_ixs = np.unique(np.concatenate([iqr_outliers, if_outliers, eif_outliers]))

    # create shell dataframe
    outlier_summary = pd.DataFrame(columns=["iqr", "if", "eif"], index=outlier_ixs)

    # fill nulls based on index value match
    outlier_summary["iqr"] = outlier_summary["iqr"].loc[iqr_outliers].fillna(value="x")
    outlier_summary["if"] = outlier_summary["if"].loc[if_outliers].fillna(value="x")
    outlier_summary["eif"] = outlier_summary["eif"].loc[eif_outliers].fillna(value="x")

    # add summary columns and sort
    outlier_summary["count"] = outlier_summary.count(axis=1)
    outlier_summary = outlier_summary.sort_values(["count"], ascending=False)

    outlier_summary = outlier_summary.fillna("")
    return outlier_summary

def outlier_IQR(self, data, iqr_step):
    """
    Documentation:
        Description:
            identifies outliers using inter_quartile range method.
        Parameters:
            data : Pandas Series
                input data array.
            iqr_step : float
                multiplier that controls level of sensitivity of outlier detection method.
                higher values for iqr_step will cause OutlierIQR to only detect increasingly
                extreme values.
        Returns:
            outlier_index : array
                index of outliers in original data array.
    """
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1

    # outlier step
    outlier_step = iqr_step * iqr

    # outlier index values
    outlier_index = data[(data < q1 - outlier_step) | (data > q3 + outlier_step)].index

    return outlier_index


# -*- coding: utf-8 -*-
import logging
import pandas as pd
import numpy as np
from .preprocess import preprocess
from .util import create_sliding_windows, normalize_column

__author__ = "Jannik Frauendorf"
__copyright__ = "Jannik Frauendorf"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def detect_anomalies(data, season_length, window_size=3):
    """

    Assigns an anomaly score to each data point of a pandas Series by using the Seasonal Behavior Deviation algorithm.

    :param data: a pandas Series containing the time series with evenly distributed values (i.e., no gaps allowed)
    :param season_length: an integer specifying the number of rows that make up one season
    :param window_size:  This parameter specifies how fine SBD should narrow down the discords.
        With smaller window_size, the anomaly_score vector becomes spikier, and the single anomalies become clear.
        By choosing higher values, the score curve becomes smoother. Moreover, with greater window_sizes, multiple close
        anomalies can be summarized to one large anomaly.
    :return: pandas DataFrame containing original index, original time series data, anomaly scores, and normal behavior
    """

    df, value_column_name, previous_index_name = preprocess(data=data, season_length=season_length)

    normal_behavior = extract_normal_behavior(df, value_column_name)

    # join normal behavior with original data
    df = pd.merge(df, normal_behavior, how='inner', on='season_step')

    # the join operation removes the order of the rows => reset the ordering to the original index column
    df = df.set_index(previous_index_name, drop=False)

    # sort by index
    df = df.sort_index()

    # generate sliding window data frame over the normal behavior vector and the value vector (both normalized)
    normal_behavior_windows = create_sliding_windows(df.loc[:, 'normal_behavior'], window_size)
    series_behavior_windows = create_sliding_windows(df.loc[:, value_column_name], window_size)

    # compute scores as row-wise Euclidean Distance between normal behavior and the actual values
    scores = df_euclidean_distance(normal_behavior_windows, series_behavior_windows)

    # move anomaly scores to center of window
    first_part = int((window_size - 1) / 2)
    second_part = window_size - 1 - first_part
    df.loc[:, 'score'] = np.concatenate((np.zeros(first_part), scores, np.zeros(second_part)))

    # normalize score
    df = normalize_column(df=df, column_name="score")

    # set index to original index
    df = df.set_index(previous_index_name, drop=True)

    # filter columns to be returned
    df = df.filter([value_column_name, "score", "normal_behavior"])

    return df


def extract_normal_behavior(df, value_column_name):
    """
    Extracts the normal behavior as the median of each season step.

    :param df: pandas DataFrame
    :param value_column_name: (str) the name of column that contains the time series values.
    :return: pandas DataFrame
    """

    # create normal behavior vector
    normal_behavior = df.groupby('season_step').agg({value_column_name: "median"})
    return normal_behavior.rename(columns={value_column_name: "normal_behavior"})


def df_euclidean_distance(df1, df2):
    """
    Computes the Euclidean Distance row-wise between two DataFrames.

    :param df1: pandas DataFrame containing numerical values
    :param df2: pandas DataFrame containing numerical values
    :return: pandas Series containing the Euclidean Distance
    """

    return pd.Series(np.linalg.norm(df1.values - df2.values, axis=1))


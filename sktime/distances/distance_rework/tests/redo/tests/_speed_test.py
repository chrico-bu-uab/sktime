# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

from sktime.distances import distance_factory
from sktime.distances.distance_rework.tests.redo import BaseDistance, _EuclideanDistance
from sktime.distances.distance_rework.tests.redo.tests._utils import (
    _time_distance,
    create_test_distance_numpy,
)

distances_to_test = [
    (_EuclideanDistance(), "euclidean"),
    ("euclidean", "euclidean_old", False),
]

if __name__ == "__main__":
    print("\n")
    average_amount = 10

    starting_timepoints = 100
    ending_timepoints = 300
    increment_timepoints = 100

    starting_dims = 0
    ending_dims = 100
    increment_dims = 50

    sizes = []
    for i in range(starting_dims, ending_dims, increment_dims):
        dims = i
        if dims == 0:
            dims = 1
        for j in range(starting_timepoints, ending_timepoints, increment_timepoints):
            timepoints = j
            if timepoints == 0:
                timepoints = 1
            sizes.append(f"{dims}x{timepoints}")

    timing_df = pd.DataFrame({"Size": sizes})

    def _run_for_distance(distance_obj, dist_name, is_dist_obj=True):
        dependent_times = []
        independent_times = []
        for i in range(starting_dims, ending_dims, increment_dims):
            dims = i
            if dims == 0:
                dims = 1
            for j in range(
                starting_timepoints, ending_timepoints, increment_timepoints
            ):
                timepoints = j
                if timepoints == 0:
                    timepoints = 1
                distances = create_test_distance_numpy(2, dims, timepoints)
                x = distances[0]
                y = distances[1]
                if is_dist_obj is True:
                    curr_dist_ind = distance_obj.distance_factory(
                        x, y, strategy="independent"
                    )
                    curr_dist_dep = distance_obj.distance_factory(
                        x, y, strategy="dependent"
                    )
                else:
                    curr_dist_dep = distance_factory(x, y, metric=distance_obj)
                    curr_dist_ind = curr_dist_dep
                dist_time_ind = _time_distance(curr_dist_ind, x, y, average_amount)
                dist_time_dep = _time_distance(curr_dist_dep, x, y, average_amount)
                row_str = f"{i}x{i}"
                if not (timing_df["Size"] == row_str).any():
                    timing_df.append([row_str, curr_dist_ind, curr_dist_dep])

                dependent_times.append(dist_time_dep)
                independent_times.append(dist_time_ind)

        timing_df[dist_name + "_independent"] = independent_times
        timing_df[dist_name + "_dependent"] = dependent_times

    for dist in distances_to_test:
        is_dist_obj = True
        if len(dist) == 3:
            is_dist_obj = dist[2]

        _run_for_distance(dist[0], dist[1], is_dist_obj)

    timing_df.to_csv("timing_df.csv", index=False)
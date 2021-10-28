import time

import numpy as np

from htc_ground_truth import HTCTracker

# Parameters

eps_time = 70
path_to_save = "logs/data_set_ground_true_test_4.txt"


def main():
    tracker = HTCTracker(calibration_config_id=2, calibrate=False, config_path="config")
    data_set = []
    start_time = time.time()
    while time.time() - start_time < eps_time:
        current_time = time.time()
        measurement = tracker.get_filtered_coordinates(verbose=True)
        stamped_measurement = np.concatenate((measurement, np.array([current_time])))
        data_set.append(stamped_measurement)
    np.savetxt(path_to_save, data_set)


if __name__ == "__main__":
    main()

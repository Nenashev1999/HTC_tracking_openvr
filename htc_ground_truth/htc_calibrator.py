import os.path

import numpy as np


class HTCCalibrator:
    def __init__(self, config_path):
        self._ground_truth = np.zeros((0, 3))
        self._config_path = config_path

    def set_new_ground_truth_data_config(self, config_id):
        self._ground_truth = np.loadtxt(os.path.join(self._config_path, f"preset_data_calibration_{config_id}.txt"))

    def ground_truth_length(self):
        return len(self._ground_truth)

    def calibrate(self, measurements):
        # linear transformation
        mean_real_coordinates = np.mean(self._ground_truth, axis=0)
        mean_measurements = np.mean(measurements, axis=0)

        linear_shift = mean_measurements - mean_real_coordinates
        adjusted_measurements = measurements - linear_shift
        print('mean_real_coordinates', mean_real_coordinates)
        print('adjusted_measurements', adjusted_measurements)
        # rotation transformation
        cross_covariance = self._ground_truth.T @ adjusted_measurements
        v, d, u = np.linalg.svd(cross_covariance)
        rotation = v @ u.T
        rotation_shift = rotation

        rotated_measurements = (rotation @ adjusted_measurements.T).T

        translation_mean_final = rotated_measurements - mean_real_coordinates
        errors_final = np.mean(abs(translation_mean_final), axis=0)
        print('Final error x = ', errors_final[0], ' y = ', errors_final[1])
        print('Average error = ', np.mean((errors_final[0:2])))

        return linear_shift, rotation_shift

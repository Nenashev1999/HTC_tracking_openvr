import numpy as np


class CalibrationHTC:
    def __init__(self):
        self.preset_data_for_calibration = np.loadtxt("config/preset_data_calibration.txt")

    def get_length(self, num_of_calibration):
        return len(self.preset_data_for_calibration)

    def calibration(self, num_of_calibration, measurements):
        for i in range(len(measurements)):
            print(measurements[i])
        linear_parameter, rotation_parameter = self.calculation_shift(self.preset_data_for_calibration,
                                                                      measurements)
        np.savetxt("logs/test_1_measured_coordinates", measurements)
        np.savetxt("logs/test_1_real_coordinates", self.preset_data_for_calibration)
        return linear_parameter, rotation_parameter

    def calculation_shift(self, true_data, measurements):
        # linear transformation
        mean_real_coordinates = np.mean(true_data, axis=0)
        mean_measurements = np.mean(measurements, axis=0)

        linear_shift = mean_measurements - mean_real_coordinates
        adjusted_measurements = measurements - linear_shift
        print('mean_real_coords', mean_real_coordinates)
        print('adjucted_measurements', adjusted_measurements)
        # rotation transformation
        cross_covariance = true_data.T @ adjusted_measurements
        v, d, u = np.linalg.svd(cross_covariance)
        rotation = v @ u.T
        rotation_shift = rotation

        rotated_measurements = (rotation @ adjusted_measurements.T).T

        translation_mean_final = rotated_measurements - mean_real_coordinates
        errors_final = np.mean(abs(translation_mean_final), axis=0)
        print('Final error x = ', errors_final[0], ' y = ', errors_final[1])
        print('Average error = ', np.mean((errors_final[0:2])))

        np.savetxt("config/lin_shift.txt", linear_shift)
        np.savetxt("config/rot_shift.txt", rotation_shift)
        return linear_shift, rotation_shift
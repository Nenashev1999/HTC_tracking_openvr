import triad_openvr
import numpy as np
DEFAULT_TRANSFORM = np.array([[1, 0, 0, 1.5],
                               [0, -1, 0, 1],
                               [0, 0, 1, 0]])
DEFAULT_TRACKER_NAME = "tracker_1"


class HtcTracking:
    def __init__(self, tracker_name=DEFAULT_TRACKER_NAME, default_transform=DEFAULT_TRANSFORM):
        self._device = triad_openvr.triad_openvr()
        self._device.print_discovered_objects()
        self._tracker_name = tracker_name
        self.main_coordinates = None
        self.preset_data = np.array([[0.042, 0.042, 0], [0.042, 1.958, 0], [2.958, 1.958, 0], [2.958, 0.042, 0],
                                     [2.55, 0.515, 0], [2.547, 1.091, 0], [1.897, 0.802, 0],
                                     [1.1, 0.8, 0], [0.445, 1.089, 0], [0.442, 0.515, 0]])
        self.linear_shift = np.loadtxt("/home/cobotar/Documents/projects/triad_openvr/lin_shift")
        self.rotation_shift = np.loadtxt("/home/cobotar/Documents/projects/triad_openvr/rot_shift")
        self._default_transform = default_transform

    def get_transformed_coordinates(self):
        htc_coordinates = self._get_htc_coordinates()
        transformed_coordinates = self._transform_coordinate_to_world_frame(htc_coordinates)
        return transformed_coordinates

    def _transform_coordinate_to_world_frame(self, coordinates):
        return self.transform_point(coordinates, self._default_transform)

    @staticmethod
    def transform_point(point, transformation):
        vector = point[0], point[2], point[1]
        result = transformation[:3, :3] @ vector + transformation[:, 3:].T
        return result[0]

    def _get_htc_coordinates(self):
        return list(self._device.devices[self._tracker_name].get_pose_euler())

    def calibration_1(self):
        measured_coordinates = []
        for i in range(len(self.preset_data)):
            print("Enter ", i + 1, " coordinate")
            input()
            measured_coordinates.append(self.get_transformed_coordinates())
            print(measured_coordinates[i])
        for i in range(len(measured_coordinates)):
            print(measured_coordinates[i])
        self.calculation_shift(self.preset_data, measured_coordinates)
        np.savetxt("test_1_measured_coordinates", measured_coordinates)
        np.savetxt("test_1_real_coordinates", self.preset_data)

    def calculation_shift(self, true_data, measurements):
        # linear transformation
        mean_real_coordinates = np.mean(true_data, axis=0)
        mean_measurements = np.mean(measurements, axis=0)

        self.linear_shift = mean_measurements - mean_real_coordinates
        adjusted_measurements = measurements - self.linear_shift
        print('mean_real_coords', mean_real_coordinates)
        print('adjucted_measurements', adjusted_measurements)
        # rotation transformation
        cross_covariance = true_data.T @ adjusted_measurements
        v, d, u = np.linalg.svd(cross_covariance)
        rotation = v @ u.T
        self.rotation_shift = rotation

        rotated_measurements = (rotation @ adjusted_measurements.T).T

        translation_mean_final = rotated_measurements - mean_real_coordinates
        errors_final = np.mean(abs(translation_mean_final), axis=0)
        print('Final error x = ', errors_final[0], ' y = ', errors_final[1])
        print('Average error = ', np.mean((errors_final[0:2])))

        np.savetxt("lin_shift", self.linear_shift)
        np.savetxt("rot_shift", self.rotation_shift)

    def get_filtered_coordinates(self, verbose=False):
        htc_coordinates = self._get_htc_coordinates()
        transformed_coordinates = self._transform_coordinate_to_world_frame(htc_coordinates)
        self.main_coordinates = self.main_filter(transformed_coordinates)
        if verbose:
            print(self.main_coordinates)
        return self.main_coordinates

    def main_filter(self, data):
        data = data - self.linear_shift
        data = (self.rotation_shift @ data.T).T
        return data


def main():
    tracker = HtcTracking()
    tracker.calibration_1()
    while(1):
        tracker.get_filtered_coordinates(verbose=True)


if __name__ == "__main__":
    main()

import os.path

import numpy as np

from .htc_calibrator import HTCCalibrator
from .triad_openvr import triad_openvr

DEFAULT_TRANSFORM = np.array([[1, 0, 0, 1.5],
                              [0, -1, 0, 1],
                              [0, 0, 1, 0]])
DEFAULT_TRACKER_NAME = "tracker_1"


class HTCTracker:
    def __init__(self, tracker_name=DEFAULT_TRACKER_NAME, default_transform=DEFAULT_TRANSFORM, calibration_config_id=0,
                 calibrate=False, config_path=None):
        self._device = triad_openvr()
        self._device.print_discovered_objects()
        self._tracker_name = tracker_name
        self.main_coordinates = None
        self._default_transform = default_transform
        self._config_path = config_path

        self._calibrator = HTCCalibrator(config_path)
        self._calibrator.set_new_ground_truth_data_config(calibration_config_id)
        self.linear_shift = np.loadtxt(os.path.join(config_path, "lin_shift.txt"))
        self.rotation_shift = np.loadtxt(os.path.join(config_path, "rot_shift.txt"))
        if calibrate:
            self.linear_shift, self.rotation_shift = self.calibrate()
            self._save_calibration_config()

    def calibrate(self):
        measurement_count = self._calibrator.ground_truth_length()
        measurements = self.input_measurements_for_calibration(measurement_count)
        return self._calibrator.calibrate(measurements)

    def _save_calibration_config(self):
        np.savetxt(os.path.join(self._config_path, "lin_shift.txt"), self.linear_shift)
        np.savetxt(os.path.join(self._config_path, "rot_shift.txt"), self.rotation_shift)

    def input_measurements_for_calibration(self, measurement_count):
        measurements = []
        for i in range(measurement_count):
            print("Put tracker in ", i + 1, " coordinate and then press enter")
            input()
            measurement = self.get_transformed_coordinates()
            print(measurement)
            measurements.append(measurement)
        return measurements

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

import triad_openvr
import numpy as np
from lib import calibration

DEFAULT_TRANSFORM = np.array([[1, 0, 0, 1.5],
                              [0, -1, 0, 1],
                              [0, 0, 1, 0]])
DEFAULT_TRACKER_NAME = "tracker_1"


class HtcTracking:
    def __init__(self, tracker_name=DEFAULT_TRACKER_NAME, default_transform=DEFAULT_TRANSFORM, calibrate=0):
        self._device = triad_openvr.triad_openvr()
        self._device.print_discovered_objects()
        self._tracker_name = tracker_name
        self.main_coordinates = None
        self._default_transform = default_transform
        if calibrate != 0:
            self.calibration_module(calibrate)
        else:
            self.linear_shift = np.loadtxt("config/lin_shift.txt")
            self.rotation_shift = np.loadtxt("config/rot_shift")

    def calibration_module(self, num_of_calibration):
        calibrate_parameters = calibration.CalibrationHTC()
        num_of_coordinates = calibrate_parameters.get_length(num_of_calibration)
        measured_coordinates = []
        for i in range(num_of_coordinates):
            print("Put tracker in ", i + 1, " coordinate and then press enter")
            input()
            measured_coordinates.append(self.get_transformed_coordinates())
            print(measured_coordinates[i])
        self.linear_shift, self.rotation_shift = calibrate_parameters.calibration(num_of_calibration,
                                                                                  measured_coordinates)

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


def main():
    tracker = HtcTracking(calibrate=1)
    while True:
        tracker.get_filtered_coordinates(verbose=True)


if __name__ == "__main__":
    main()

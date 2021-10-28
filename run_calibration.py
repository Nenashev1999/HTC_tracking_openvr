import time

import numpy as np

from htc_ground_truth import HTCTracker


# noinspection PyTypeChecker
def main():
    tracker = HTCTracker(calibration_config_id=2, calibrate=False, config_path="config")
if __name__ == "__main__":
    main()

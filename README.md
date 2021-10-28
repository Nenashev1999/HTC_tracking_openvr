# HTC_tracking_openvr

## Overview

This project related to estimation position of the object using HTC VR tracking system.
This algorithm can help to calibrate and geting position of the object.

### Preparation

You should have HTC tracking VR system and tracker or controller.
First you should download Steam software and in Steam you should download SteamVR.
After you should launch the SteamVR and turn on all devices ralated to VR.
Next step is calibration of space for calibration click right button in VR application and press "room setup" and follow the instruction.

After calibration you can use software, but you need to calibrate shifting of global coordinates. 
For this step make some points on your plane, and measure it true coordinates x, y, z, and add it to the "config/preset_data_calibration_*.txt" where * is your number of calibration.
For checking coordinate system without transformation check file config/tracker_name and write "tracker_1" if you use tracker, or write "controller_1" if you are using controller, and then run:

```
python3 run_htc_tracker.py
```
Output of program is coordinates of tracker x, y, z

Example: 
Creating file in config/preset_data_calibration_3.txt:
```
0.042 0.042 0
0.042 1.958 0
2.958 1.958 0
2.958 0.042 0
.
.
.
```
After creating coordinates, we should create coordinates matrix in file config/transformation_matrix.txt
```
1 0 0 1.5
0 1 0 1
0 0 1 0
```
where elements from [0,0] to [2,2] is our coordinates in my case I don't change coordinates by multiplying, and matrix from [3,0] to [3,2] is shifting of coordinates in my case, I shift x + 1.5 and y + 1

### Calibration of algorithm
Open the file run_calibration.py and change the parametr of calibration "calibration_config_id= '*' ".
Where * is a number of your file with coordinates for calibration.
Run the calibration
```
python3 run_calibration.py
```
Follow to instruction.
### Running the algorithm
After calibration all parameters will be saved in config and you can run the algorithm, it will work 50sec and write data into a file, to change this parameters open the file run_htc_tracker and change parameter eps_time and path_to_save

```
python3 run_htc_tracker.py
```

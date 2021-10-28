# HTC_tracking_openvr

## Overview

This project related to estimation position of the object using HTC VR tracking system.
This algorithm can help to calibrate and geting position of the object.

### Preparation

You should have HTC tracking VR system and tracker of controller.
First you should download Steam software and in Steam you should download SteamVR
After you should launch the SteamVR and turn on all devices ralated to VR.
Next step is calibration of space for calibration press right button and press "room setup" and follow the instruction.

After calibration you can use software, but you need to calibrate shifting of global coordinates. 
For this step make some points on your plane, and measure it true coordinates x, y, z, and add it to the "config/preset_data_calibration_*.txt" where * is your number of calibration.

Example: 
Creating file in config/preset_data_calibration_3.txt:
'''
0.042 0.042 0
0.042 1.958 0
2.958 1.958 0
2.958 0.042 0
.
.
.
'''

After creating coordinates

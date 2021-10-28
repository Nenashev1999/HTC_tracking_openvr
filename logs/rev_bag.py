import rosbag
import numpy as np
bagfile = rosbag.Bag("data_set_measurements_test_3.bag")
translations = []
coords = []
coord_x_odom = coord_y_odom = coord_x_main = coord_y_main = 0
for topic, msg, t in bagfile.read_messages(topics="/tf"):

    if msg.transforms[0].child_frame_id == "main_robot":
        coord_x_main = msg.transforms[0].transform.translation.x
        coord_y_main = msg.transforms[0].transform.translation.y
    if msg.transforms[0].child_frame_id == "main_robot_odom":
        coord_x_odom = msg.transforms[0].transform.translation.x
        coord_y_odom = msg.transforms[0].transform.translation.y
    coords.append([coord_x_odom + coord_x_main, coord_y_odom + coord_y_main])

np.savetxt("meas.txt", coords)
bagfile.close()

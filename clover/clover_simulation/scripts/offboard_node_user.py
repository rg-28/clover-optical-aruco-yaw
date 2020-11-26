#!/usr/bin/env python

import rospy
import time
import math
from clover import srv
from std_srvs.srv import Trigger
from aruco_pose.msg import MarkerArray

rospy.init_node('flight') # 'flight' is name of the ROS node

# Creating proxies for the required services before calling them in the script
get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
land = rospy.ServiceProxy('land', Trigger)

aruco_id = 'aruco_4' #Default aruco marker id
def markers_callback(msg):
    for marker in msg.markers:
        aruco_id = 'aruco_' + str(msg.markers[0].id)
#Each time a message is posted in aruco_detect/markers, the markers_callback function
#is called with this message as its argument.

rospy.Subscriber('aruco_detect/markers', MarkerArray, markers_callback)

# The navigate_wait() function is used to fly the drone towards a point and then wait for the drone's arrival
# with a tolerance level of +-0.1 m from the required position
def navigate_wait(x=0, y=0, z=0, yaw=float('nan'), speed=0.5, frame_id='', auto_arm=False, tolerance=0.1):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)
    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)

navigate_wait(x=0.0, y=0.0, z=0.5, speed=1.0, frame_id='body', auto_arm=True)
#Initial take-off of the drone to detect the aruco marker id below it

while(True):

    print 'Please select the mode of action you want the drone to perform: '
    print 'Mode = 0 (Land the drone and exit.)'
    print 'Mode = 1 (Fly the drone along the z-axis.)'
    print 'Mode = 2 (Rotate the drone along the z-axis.)'
    print '\n'

    mode = int(input("Enter the mode: "))

    if(mode == 0):
        navigate_wait(frame_id=aruco_id, x=0, y=0, z=0.4, speed=1.0)
        print 'Landing on ' + aruco_id
        res = land()
        if res.success:
            print 'drone has landed'
        break

    elif(mode == 1):
        req_height = float(input("Enter the required height: "))
        speed_vz = float(input("Enter the required vertical velocity: "))
        navigate_wait(x=0.0, y=0.0, z=req_height, speed=speed_vz, frame_id=aruco_id)
        rospy.sleep(10.0)
        print 'Success'
        print '\n'

    elif(mode == 2):
        angle_in_degrees = int(input("Enter the required yaw angle: "))
        req_yaw_rate = float(input("Enter the required yaw_rate: "))
        angle_in_radians = float(0.0174 * angle_in_degrees)
        delay_time = angle_in_radians / req_yaw_rate
        # The delay_time is calculated by firstly converting the required yaw angle (angle_in_degrees)
        # into radians (angle_in_radians) and then dividing it by the required yaw rate (req_yaw_rate).
        telemetry = get_telemetry(frame_id=aruco_id)
        navigate(x=0.0, y=0.0, z=telemetry.z, yaw=float('nan'), yaw_rate=req_yaw_rate, frame_id=aruco_id)
        rospy.sleep(delay_time) 
        print 'Success'
        navigate(x=0.0, y=0.0, z=telemetry.z, yaw=float('nan'), yaw_rate=0.0, frame_id=aruco_id)
        rospy.sleep(3.0)
        print '\n'

    else:
        print 'Wrong Input Mode Selected'
        print 'Try Again'
        print '\n'

rospy.sleep(5.0)
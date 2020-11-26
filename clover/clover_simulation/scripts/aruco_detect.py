#!/usr/bin/env python

import rospy
from aruco_pose.msg import MarkerArray

rospy.init_node('my_node')
# ...

aruco_id = 'aruco_4'
def markers_callback(msg):
    # print 'Detected markers:'
    for marker in msg.markers:
        # print 'Marker: %s' % marker
        aruco_id = 'aruco' + str(msg.markers[0].id)
        print aruco_id
# Create a Subscription object. Each time a message is posted in aruco_detect/markers, the markers_callback function
#is called with this message as its argument.

rospy.Subscriber('aruco_detect/markers', MarkerArray, markers_callback)
# ...

rospy.spin()
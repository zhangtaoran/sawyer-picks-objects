#!/usr/bin/python2
import cv2
import numpy as np
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String
from geometry_msgs.msg import Pose
import cv_bridge
import tf
import math

def image_callback(ros_img)
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("shoot")
    img_counter = 0

    while True:
        ret, frame = cam.read()
        cv2.imshow("shoot", frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1

if __name__ == '__main__':
    rospy.init_node('shoot', anonymous=True)  # Initialze ROS node

    bridge = cv_bridge.CvBridge()  # Initialize CV Bridge object
    # Subscribe to camera image topic
    sub = rospy.Subscriber('/cameras/image', Image,
                            image_callback, queue_size=1)

    rospy.spin()  # sleep
    cv2.destroyAllWindows()  # Destroy CV image window on shut_down

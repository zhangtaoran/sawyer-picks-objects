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

def image_callback(ros_img):
    frame = cv2.imread('left.png', cv2.IMREAD_COLOR)
    frame2 = cv2.imread('right.png', cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_red = np.array([0,100,0])
    upper_red = np.array([10,255,255])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_red, upper_red)
    mask2 = cv2.inRange(hsv2, lower_red, upper_red)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    res2 = cv2.bitwise_and(frame2,frame2, mask= mask2)
    cv2.imshow('frame',frame)
    cv2.imshow('frame2',frame2)
    # cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    cv2.imshow('res2',res2)
    # cv2.waitKey(0)

    # convert image to grayscale image
    gray_image = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(res2, cv2.COLOR_BGR2GRAY)
 
    # convert the grayscale image to binary image
    ret,thresh = cv2.threshold(gray_image,127,255,0)
    ret2,thresh2 = cv2.threshold(gray_image2,127,255,0)
 
    # calculate moments of binary image
    M = cv2.moments(thresh)
    M2 = cv2.moments(thresh2)
 
    # calculate x,y coordinate of center
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    cX2 = int(M2["m10"] / M2["m00"])
    cY2 = int(M2["m01"] / M2["m00"])
 
    # put text and highlight the center
    cv2.circle(res, (cX, cY), 5, (255, 255, 255), -1)
    cv2.putText(res, "centroid1", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.circle(res2, (cX2, cY2), 5, (255, 255, 255), -1)
    cv2.putText(res2, "centroid2", (cX2 - 25, cY2 - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
 
    # display the image
    cv2.imshow("Image", res)
    cv2.imshow("Image2", res2)
    cv2.waitKey(0)

    # Values found from camera_calibration.py in scripts directory
    f=397
    # print cX,cY,cX2,cY2
    d=cX2-cX
    D=145
    l=(f*D)/d
    print l

if __name__ == '__main__':
    rospy.init_node('depthsensing', anonymous=True)  # Initialze ROS node

    bridge = cv_bridge.CvBridge()  # Initialize CV Bridge object
    # Subscribe to camera image topic
    sub = rospy.Subscriber('/cameras/image', Image,
                            image_callback, queue_size=1)

    rospy.spin()  # sleep
    cv2.destroyAllWindows()  # Destroy CV image window on shut_down

#!/usr/bin/env python
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import PoseWithCovarianceStamped
from geometry_msgs.msg import TwistWithCovarianceStamped
import random
import time

prev_x = 0
prev_time = 0
frame_no = 0

def transfer(data, pub):
    global prev_x, prev_time, frame_no
    frame_no += 1

    to_send = PoseWithCovarianceStamped()
    to_send.header.seq = frame_no
    to_send.header.stamp = rospy.Time.now()
    to_send.header.frame_id = "map"

    to_send.pose.pose.position.x = data.x + (random.random()/10)
    to_send.pose.pose.position.y = 0
    to_send.pose.pose.position.z = 0
    to_send.pose.pose.orientation.w = 1
    to_send.pose.pose.orientation.x = 0
    to_send.pose.pose.orientation.y = 0
    to_send.pose.pose.orientation.z = 0
    to_send.pose.covariance[0] = 10
    # to_send.pose.covariance[1:] = 0


    to_send_twist = TwistWithCovarianceStamped()
    to_send_twist.header.seq = frame_no
    to_send_twist.header.stamp = rospy.Time.now()
    to_send_twist.header.frame_id = "base_link"

    to_send_twist.twist.twist.linear.x = (to_send.pose.pose.position.x - prev_x) / (time.time()-prev_time)
    to_send_twist.twist.twist.linear.y = 0
    to_send_twist.twist.twist.linear.z = 0
    to_send_twist.twist.twist.angular.x = 0
    to_send_twist.twist.twist.angular.y = 0
    to_send_twist.twist.twist.angular.z = 0
    to_send_twist.twist.covariance[0] = 500
    # to_send_twist.twist.covariance[1:] = 0


    prev_x = to_send.pose.pose.position.x
    prev_time = time.time()


    pub[0].publish(to_send)
    pub[1].publish(to_send_twist)


def position():
    rospy.init_node('odom_generator', anonymous=True)
    pubp = rospy.Publisher('turtle1/sensors/pose',PoseWithCovarianceStamped, queue_size=10)
    pubv = rospy.Publisher('turtle1/sensors/twist',TwistWithCovarianceStamped, queue_size=10)
    rospy.Subscriber('/turtle1/pose',Pose, callback= transfer, callback_args=[pubp, pubv])

    rospy.spin()




if __name__ == '__main__':
    try:
        position()
    except rospy.ROSInterruptException:
        pass
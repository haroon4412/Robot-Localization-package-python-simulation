#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

def transfer(data, pub):
    vel = data.twist.twist.linear.x
    # x = Odometry()
    # x.twist.twist.linear.x
    to_send = Twist()
    to_send.linear.x = vel

    pub.publish(to_send)


def follow():
    rospy.init_node('mimic', anonymous=True)
    pub = rospy.Publisher('/follower/cmd_vel',Twist, queue_size=10)
    rospy.Subscriber('/odometry/filtered_twist',Odometry, callback= transfer, callback_args=pub)

    rospy.spin()


if __name__ == '__main__':
    try:
        follow()
    except rospy.ROSInterruptException:
        pass
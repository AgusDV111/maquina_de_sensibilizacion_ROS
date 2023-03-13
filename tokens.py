#!/usr/bin/env python3
import rospy
from std_msgs.msg import Bool
from gpiozero import DistanceSensor
from time import sleep

class US():
    def __init__(self):
        self.sensor=DistanceSensor(23,25)
        self.flag = False
        self.rate = rospy.Rate(60)
        self.flag_sub = rospy.Subscriber("/flag",Bool,self.flag_Callback)
        self.token_pub = rospy.Publisher("/token",Bool,queue_size=10)

    def flag_Callback(self,msg):
        self.flag = msg.data

    def distance(self):
        while True:
            print('La distancia al objeto es: ', sensor.distance*100, 'cm')
            sleep(0.5)


    def main(self):
        while not rospy.is_shutdown():
	           try:
	                  self.video_reader()
	           except Exception as e:
	                  print(e)
	                  print("wait")
	           self.rate.sleep()


if __name__ == '__main__':
	try:
		ultraSonico = US()
		ultraSonico.main()
	except (rospy.ROSInterruptException, rospy.ROSException('Topic was interrupted')):
		pass

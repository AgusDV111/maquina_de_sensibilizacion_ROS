#!/usr/bin/env python3
import rospy
from std_msgs.msg import Bool
import cv2
import os
import random
import time
import pygame


class VideoListReader():
    def __init__(self):
        rospy.init_node("main_video")
        pygame.mixer.init()
        self.token_sub = rospy.Subscriber("/token",Bool,self.token_Callback)
        self.pub = rospy.Publisher("/flag",Bool,queue_size=10)
        self.rate = rospy.Rate(60)
        self.token = False
        self.videofolderPath = '/home/agustin/Documents/cam_teleton/catkin_ws/src/teleton_cam/src/videos'
        self.audiofolderPath = '/home/agustin/Documents/cam_teleton/catkin_ws/src/teleton_cam/src/audio'
        self.videoTokensfolderPath = '/home/agustin/Documents/cam_teleton/catkin_ws/src/teleton_cam/src/agradecimiento/video_1.mp4'
        self.windowName = "video"

    def token_Callback(self,msg):
        self.token = msg.data

    def videoThanxInterrupt(self):
        video_path = self.videoTokensfolderPath
        video = cv2.VideoCapture(video_path)

        cv2.namedWindow(self.windowName, cv2.WND_PROP_FULLSCREEN)

        cv2.setWindowProperty(self.windowName,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)


        while True:
            time.sleep(.015)
            ret, frame = video.read()
            if not ret:
                break
            cv2.imshow("video", frame)
            cv2.waitKey(1)
        self.pub.publish(True)
        time.sleep(.015)
        video.release()
        pygame.mixer.music.load(video_path)
        pygame.mixer.music.play()

    def video_reader(self):
        for video_name in os.listdir(self.videofolderPath):
            if self.token == True:
                self.videoThanxInterrupt()
            self.pub.publish(False)
            video_path = os.path.join(self.videofolderPath, video_name)
            video = cv2.VideoCapture(video_path)
            cv2.namedWindow(self.windowName, cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty(self.windowName,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
            audio, ext = os.path.splitext(video_name)
            pygame.mixer.music.load(self.audiofolderPath + "/" + audio + ".mp3")
            pygame.mixer.music.play()
            while True:
                time.sleep(.018)
                ret, frame = video.read()
                if not ret:
                    break
                cv2.imshow("video", frame)
                cv2.waitKey(1)

            video.release()


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
		vid = VideoListReader()
		vid.main()
	except (rospy.ROSInterruptException, rospy.ROSException('Topic was interrupted')):
		pass

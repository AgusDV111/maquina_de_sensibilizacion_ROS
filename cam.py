#!/usr/bin/env python3
import rospy
from std_msgs.msg import Bool
import cv2
import os
import random
import time
from ffpyplayer.player import MediaPlayer


class VideoListReader():
    def __init__(self):
        rospy.init_node("main_video")
        self.token_sub = rospy.Subscriber("/token",Bool,self.token_Callback)
        self.pub = rospy.Publisher("/flag",Bool,queue_size=10)
        self.rate = rospy.Rate(60)
        self.token = False
        self.videofolderPath = '/home/agustin/Documents/cam_teleton/catkin_ws/src/teleton_cam/src/videos'
        self.videoTokensfolderPath = '/home/agustin/Documents/cam_teleton/catkin_ws/src/teleton_cam/src/agradecimiento/video_1.mp4'
        self.windowName = "video"

    def token_Callback(self,msg):
        self.token = msg.data

    def videoThanxInterrupt(self):
        video_path = self.videoTokensfolderPath
        video = cv2.VideoCapture(video_path)

        cv2.namedWindow(self.windowName, cv2.WND_PROP_FULLSCREEN)

        cv2.setWindowProperty(self.windowName,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        player = MediaPlayer(video_path)

        while True:
            time.sleep(.015)
            ret, frame = video.read()
            audio_frame, val = player.get_frame()
            if not ret:
                break
            cv2.imshow("video", frame)
            if val != 'eof' and audio_frame is not None:
                #audio
                img, t = audio_frame
            cv2.waitKey(1)
        self.pub(True)
        time.sleep(.015)
        video.release()
        PlayVideo(video_path)

    def video_reader(self):
        for video_name in os.listdir(self.videofolderPath):
            if self.token == True:
                self.videoThanxInterrupt()
            self.pub(False)
            video_path = os.path.join(self.videofolderPath, video_name)
            video = cv2.VideoCapture(video_path)
            cv2.namedWindow(self.windowName, cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty(self.windowName,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
            player = MediaPlayer(video_path)

            while True:
                time.sleep(.018)
                ret, frame = video.read()
                audio_frame, val = player.get_frame()
                if not ret:
                    break
                cv2.imshow("video", frame)
                if val != 'eof' and audio_frame is not None:
                    #audio
                    img, t = audio_frame
                cv2.waitKey(1)

            video.release()
        PlayVideo(video_path)

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

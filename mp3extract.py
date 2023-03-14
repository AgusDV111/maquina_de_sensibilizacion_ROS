#!/usr/bin/env python3
import subprocess
import os
import sys

def convert_video_to_audio_ffmpeg(video_file, output_ext="mp3"):
    """Converts video to audio directly using `ffmpeg` command
    with the help of subprocess module"""
    filename, ext = os.path.splitext(video_file)
    subprocess.call(["ffmpeg", "-y", "-i", video_file, f"{filename}.{output_ext}"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)

if __name__ == "__main__":
    videofolderPath = '/home/agustin/Documents/cam_teleton/catkin_ws/src/teleton_cam/src/videos'
    for video_name in os.listdir(videofolderPath):
        vf = os.path.join(videofolderPath, video_name)
        convert_video_to_audio_ffmpeg(vf)

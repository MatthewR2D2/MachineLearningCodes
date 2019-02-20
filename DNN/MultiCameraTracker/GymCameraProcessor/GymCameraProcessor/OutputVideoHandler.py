"""
Created on Wed Nov  3 16:03:30 2018
@author: Matthew Millar
What it does:
This creates video handlers to write files out to a disk
"""
import cv2

'''
@brief This creates a writer for use for both color or black and white videos  
@note You need a 0 for black and white to fix the channels for writing 
@raises None
@param[in] H/W this is the height and width of the output (must match the video you want to write out)
@param[in] video_title the name of the save file 
@param[in] black_or_white boolean that sets the recoding to either color or black and white 
@returns This returns the writer for video file
'''


def createWriters(H, W, video_title, color):
    fourcc = cv2.VideoWriter_fourcc(*'MPEG')
    if color:
        return cv2.VideoWriter(video_title, fourcc, 30.0, (H, W))
    else:
        return cv2.VideoWriter(video_title, fourcc, 30.0, (H, W), 0)  # Need a 0 at the end for black and white videos

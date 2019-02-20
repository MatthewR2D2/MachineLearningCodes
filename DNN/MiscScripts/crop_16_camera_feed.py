#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 11:39:59 2018

@author: ben
"""

def crop_to_camera(img, selection):
        """From a 16 grid camera layout provide a selection of:
           cameras 1 to 16 (integer) or string "3x3"/"4x4" to crop to this""" 
        
        cam_h=270
        cam_w=360
        
        left_offset=240
        
        if selection in [1,2,3,4]:
            #Camera 1 or 2 or 3 or 4 
            y=0
            x=left_offset + (selection-1)*cam_w 
            
        if selection in [5,6,7,8]:
            y=cam_h
            x=left_offset + (selection-5)*cam_w 
        
        if selection in [9,10,11,12]:
            y=cam_h*2
            x=left_offset + (selection-9)*cam_w 
            
        if selection in [13,14,15,16]:
            y=cam_h*3
            x=left_offset + (selection-13)*cam_w 
            
        vid_height=cam_h
        vid_width=cam_w
        
        if selection == "3x3":
            #3x3 top-left box.
            y=0
            vid_height=cam_h*3 
            x=left_offset
            vid_width=cam_w*3
            
        if selection == "4x4":
            y=0
            vid_height=cam_h*4 
            x=left_offset
            vid_width=cam_w*4
            
        img = img[y:y+vid_height, x:x+vid_width]
        
        return img
        
        
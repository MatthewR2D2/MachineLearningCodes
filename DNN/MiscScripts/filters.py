#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Collection of filters to use with OpenCV

Created on Fri Nov 16 18:11:10 2018

@author: ben
"""
import cv2
from skimage import exposure
import numpy as np

def scipy_equalize_adapthist(img):
    img = exposure.equalize_adapthist(img, clip_limit=0.01)
    return img

def adaptive_histogram(img, clipLimit=2.0, tileGridSize=(8,8) ):    
    ### Adaptive Histrogram Equalisation of the Contrast 
    ### CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=tileGridSize)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
    l, a, b = cv2.split(lab)  # split on 3 different channels
    l2 = clahe.apply(l)  # apply CLAHE to the L-channel
    lab = cv2.merge((l2,a,b))  # merge channels
    img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)  # convert from LAB to BGR
    return img

def contrast_brightness_curve(img, phi=1, theta=20):
    ### Brightness/contrast  
    # https://stackoverflow.com/questions/19363293/whats-the-fastest-way-to-increase-color-image-contrast-with-opencv-in-python-c/19384041
    maxIntensity = 255.0 # depends on dtype of image data
    # Parameters for manipulating image data
    # Increase intensity such that bright pixels become slightly bright
    newImage0 = (maxIntensity/phi)*(img/(maxIntensity/theta))**0.5
    img = np.array(newImage0,dtype=np.uint8)
    
    # visualise the applied levels:
    #import matplotlib.pyplot as plt
    #x = np.arange(maxIntensity) 
    #y = (maxIntensity/phi)*(x/(maxIntensity/theta))**0.5 + x 
    #plt.plot(x,y,'r-')
    #plt.show()
    return img
    
def saturation(img, saturation=1.75):
    ### Adjust color saturation 
    imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype("float32")
    (h, s, v) = cv2.split(imghsv)
    s = s*saturation
    s = np.clip(s,0,255)
    imghsv = cv2.merge([h,s,v])
    img = cv2.cvtColor(imghsv.astype("uint8"), cv2.COLOR_HSV2BGR)
    return img 

def bilateral_filter(img, pixel_diameter=8, intensity=112):
    return cv2.bilateralFilter(img,pixel_diameter,intensity,intensity)   

def unsharpen_mask(img, a=0.3, b=1.5, c=-0.5):
    # Despite the name, is used to sharpen an image (https://en.wikipedia.org/wiki/Unsharp_masking#Digital_unsharp_masking)
    blur = cv2.GaussianBlur(img, (0, 0), a)
    img  = cv2.addWeighted(blur, b, img, c, 0)
    return img 

def sharpen(img, alpha=0.5):
    # Alpha is just the fraction of the sharpened image 
    # to include as an overlay. 1.0 = fully sharpened. 0 = no sharpening. 
    kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]]) #sharpen
    filtered = cv2.filter2D(img, -1, kernel)
    img = cv2.addWeighted(filtered, alpha, img, 1-alpha, 0);
    return img 


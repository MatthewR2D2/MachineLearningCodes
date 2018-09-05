# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 09:25:50 2018
@author: Matthew Millar
What it does:
What it needs:
Related Classes:

"""

import numpy as np
import cv2

sift = cv2.xfeatures2d.SIFT_create()

cap = cv2.VideoCapture(0)

onlyonetime = True
out = cv2.VideoWriter()

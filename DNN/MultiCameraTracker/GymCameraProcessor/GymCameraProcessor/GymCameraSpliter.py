"""
Created on Wed Oct  3 16:03:30 2018
@author: Matthew Millar
What it does:
These methods are utility methods that are used to split up each camera based on the input cam number
and the method.
What it needs:
Related Classes:
"""


'''
  Global Variables for camera specs
  '''
# Height and width of each camera in pixels
h = 270
w = 360
# Helper variables for getting each camera
row1 = 0
row2 = 270
row3 = 540
row4 = 810
row5 = 1080
col1 = 242
col2 = 602
col3 = 962
col4 = 1322
col5 = 1440

'''
Get just one camera for analysis
'''


def crop_camera_by_number(frame, cam_number):
    if cam_number == 1:
        return frame[row1:row1 + h, col1:col1 + w]
    elif cam_number == 2:
        return frame[row1:row1 + h, col2:col2 + w]
    elif cam_number == 3:
        return frame[row1:row1 + h, col3:col3 + w]
    elif cam_number == 4:
        return frame[row1:row1 + h, col4:col4 + w]
    elif cam_number == 5:
        return frame[row2:row2 + h, col1:col1 + w]
    elif cam_number == 6:
        return frame[row2:row2 + h, col2:col2 + w]
    elif cam_number == 7:
        return frame[row2:row2 + h, col3:col3 + w]
    elif cam_number == 8:
        return frame[row2:row2 + h, col4:col4 + w]
    elif cam_number == 9:
        return frame[row3:row3 + h, col1:col1 + w]
    elif cam_number == 10:
        return frame[row3:row3 + h, col2:col2 + w]
    elif cam_number == 11:
        return frame[row3:row3 + h, col3:col3 + w]
    elif cam_number == 12:
        return frame[row3:row3 + h, col4:col4 + w]
    elif cam_number == 13:
        return frame[row4:row4 + h, col1:col1 + w]
    elif cam_number == 14:
        return frame[row4:row4 + h, col2:col2 + w]
    elif cam_number == 15:
        return frame[row4:row4 + h, col3:col3 + w]
    elif cam_number == 16:
        return frame[row4:row4 + h, col4:col4 + w]
    else:
        return frame[row1:row1 + h, col1:col1 + w]  # Default it to cam 1


def get_all_cameras(frame):
    return frame[row1:row1 + row5, col1:col1 + col5]



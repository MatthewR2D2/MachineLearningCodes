#!/usr/bin/env python

'''
# Short Description@
# 
# Full Description@

Say we have a peak business hours like below in Tokyo time:

Sun|22:00-23:59|Mon|00:00-08:28,22:00-23:59|Tue|00:00-08:28,22:00-23:59|Wed|00:00-08:28,22:00-23:59|Thu|00:00-08:28,22:00-23:59|Fri|00:00-08:28

Write a python script which will convert that to London time.”
# 
__author__ = "Matthew Millar"
__copyright__ = ""
__credits__ =
__license__ = ""
__version__ = "0.0.0"
__maintainer__ = "Matthew Millar"
__email__ = "matthew.millar@igniterlabs.com"
__status__ = "Dev"

'''

import re
from textwrap import wrap

# 0am in japan is 1500 pervious day in London so its 9 hours behind
# What I need to do.
# parse out the day from the string
# parse out the start time
# parse out the end time
# Parse out the 2nd start
# Parse out the 2nd end

inputString = "Sun|22:00-23:59|Mon|00:00-08:28,22:00-23:59|Tue|00:00-08:28,22:00-23:59|Wed|00:00-08:28,22:00-23:59|Thu|00:00-08:28,22:00-23:59|Fri|00:00-08:28"

split1 = inputString.split('|')

sun = []
mon = []
tue = []
wed = []
thu = []
fri = []

index = 0
for part in split1:
    if part == "Sun":
        print("Sunday")

        sun.append(part)




print(sun)




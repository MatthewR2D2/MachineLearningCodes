#!/usr/bin/env python

'''
# Short Description@
# 
# Full Description@
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

from SmartAdFSM.AdUtility import YahooJsonParser as yjp
from tkinter import *


def CreateYahooAdList(jsonSource, yahooAdList, adList):
    # Test Ad simulate call from API
    # TODO: Create call to API for Yahoo Ad to get every ad that is available
    readFromAPI = jsonSource
    # read in the file
    parsedFile = yjp.readinJson(readFromAPI)
    # create objects for each ad and add them into the Yahoo Ad list
    yjp.createAdObjects(yahooAdList, parsedFile)

    # Then add all the new Yahoo parsed ads (Now Ad Objects) into the myAds list
    for ad in yahooAdList:
        adList.append((ad))


'''
This method will get values from a Json file 
In the future it will pull it off the Yahoo API
@:param textFeildValues = adTitles[] from SimpleUIControler
@:param comboValues = ddMenuValues[] from SimpleUIControler
@:param ads = currentAds from SimpleUIControler
'''


def UpdateUIValues(comboValues, currentAds):
    for ad in currentAds:
        title = ad.title
        status = ad.status
        comboValues.append(title + ':' + status)



def UpdateUI(dropdownWidget, dropdownValues):
    dropdownWidget['values'] = dropdownValues
    # The init value
    dropdownWidget.current(0)

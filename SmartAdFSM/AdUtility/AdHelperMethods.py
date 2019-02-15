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

'''
This method is for reading in a json from a file or a URL
@:param readFromFile - boolean tell which method to read from file/url
@:param myjson - this is the json source file/url
@:param yahooAdList - this holds all the ads from yahoo
@:param currentAds - This holds every ad that is from all service providers.
'''


def CreateYahooAdList(readFromFile, myjson, yahooAdList, currentAds):
    # Clear all arrays Do this to make sure array is cleared
    currentAds.clear()
    yahooAdList.clear()

    if readFromFile:
        readFromAPI = myjson
        # read in the file
        parsedFile = yjp.readinJson(readFromAPI)
        # create objects for each ad and add them into the Yahoo Ad list
        yjp.createAdObjects(yahooAdList, parsedFile)
    else:
        # create objects for each ad and add them into the Yahoo Ad list
        yjp.createAdObjects(yahooAdList, myjson)

    # Then add all the new Yahoo parsed ads (Now Ad Objects) into the myAds list

    for ad in yahooAdList:
        currentAds.append(("Yahoo", ad))


'''
This method will get values from a Json file 
In the future it will pull it off the Yahoo API
@:param textFeildValues = adTitles[] from SimpleUIControler
@:param comboValues = ddMenuValues[] from SimpleUIControler
@:param ads = currentAds from SimpleUIControler
'''


def UpdateUIValues(dropdownValues, currentAds):
    # clear array that holds list of values for the dropdown box
    dropdownValues.clear()
    for ad in currentAds:
        apiHost = ad[0]  # Where the ad is hosted
        title = ad[1].title  # The title from the ad
        status = ad[1].status  # The curent status of the ad
        dropdownValues.append(apiHost + ":" + title + ':' + status)  # Create the list string for the drop down menu


'''
This method is to update the UI for the dropdownWidget
@:param dropdownWidget - is the dropdown menu that displays the currently available ads
@:param dropdownValues - is the list of available ads from every vendor
'''


def UpdateUI(dropdownWidget, listboxWidget,  dropdownValues):
    getItemsPerLine(dropdownValues, listboxWidget)
    dropdownWidget['values'] = dropdownValues
    # The init value
    dropdownWidget.current(0)

def getItemsPerLine(dropdownValues, listboxWidget):
    # Clear the list
    listboxWidget.delete(0,'end')
    x = 1
    for item in dropdownValues:
        listboxWidget.insert(x, item)
        x += 1
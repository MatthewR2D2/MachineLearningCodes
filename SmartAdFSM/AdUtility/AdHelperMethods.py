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


def CreateYahooAdList(jsonSource, yahooAdList, currentAds):
    # Test Ad simulate call from API
    # TODO: Create call to API for Yahoo Ad to get every ad that is available
    readFromAPI = jsonSource
    # read in the file
    parsedFile = yjp.readinJson(readFromAPI)

    # Clear all arrays Do this to make sure array is cleared
    currentAds.clear()
    yahooAdList.clear()

    # create objects for each ad and add them into the Yahoo Ad list
    yjp.createAdObjects(yahooAdList, parsedFile)

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
        apiHost = ad[0]        # Where the ad is hosted
        title = ad[1].title    # The title from the ad
        status = ad[1].status  # The curent status of the ad
        dropdownValues.append(apiHost + ":" + title + ':' + status)  # Create the list string for the drop down menu



def UpdateUI(dropdownWidget, dropdownValues):
    print(dropdownValues)
    dropdownWidget['values'] = dropdownValues
    # The init value
    dropdownWidget.current(0)

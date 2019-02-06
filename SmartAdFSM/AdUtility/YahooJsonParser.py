#!/usr/bin/env python

'''
# Short Description@ This is the Yahoo Ad parser.
#
# Full Description@ This is the parser that will go through the JSON file from the Yahoo API and
    parse out all the items into its own object using the YahooAdObject.py file (Defines the Object)
    It will then return the parse file for further use in the program
#
__author__ = "Matthew Millar"
__copyright__ = ""
__credits__ =
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "Matthew Millar"
__email__ = "matthew.millar@igniterlabs.com"
__status__ = "Dev"

'''

import json
from SmartAdFSM.AdObjects import YahooAdObject as yao

'''
This method will read in a Json file from the Yahoo API
@:param jsonFile- this is the read in file recived from the YahooAd API
'''


def readinJson(jsonFile):
    # Read in the json file and save it into a variable
    with open(jsonFile, 'r') as file:
        readJson = json.load(file)
    return readJson


'''
This method will parse though the entire AdJson file and then create the yahooAd files from this.
@:param: adlist - This is a dict to hold all the newly created ad objects
@:param: processedJson - This is the read in and fixed json file that is received from the Yahoo API
'''


def createAdObjects(adlist, processedJson):
    for j in processedJson:
        id = j["id"]
        description = j["description"]
        adGroupId = j["adGroupId"]
        status = j["status"]
        title = j["title"]
        advertiserId = j["advertiserId"]
        landingUrl = j["landingUrl"]
        imageUrl = j["imageUrl"]
        sponsoredBy = j["sponsoredBy"]
        campaignId = j["campaignId"]
        displayUrl = j["displayUrl"]
        imageUrlHQ = j["imageUrlHQ"]
        contentUrl = j["contentUrl"]
        callToActionText = j["callToActionText"]
        videoPrimaryUrl = j["videoPrimaryUrl"]
        adName = j["adName"]

        # Now add the newlly parsed Data into a new object
        adlist.append(yao.YahooAd(id,
                                  description,
                                  adGroupId,
                                  status,
                                  title,
                                  advertiserId,
                                  landingUrl,
                                  imageUrl,
                                  sponsoredBy,
                                  campaignId,
                                  displayUrl,
                                  imageUrlHQ,
                                  contentUrl,
                                  callToActionText,
                                  videoPrimaryUrl,
                                  adName))

'''
This is for testing the this python file 
'''
if __name__ == '__main__':
    # Test parsing file
    jsonFile = "../TestAds/YahooAd.json"

    # Simple Test to print to see if the read in worked
    # DONT NEED IN PRODUCTION
    # for j in readJson:
    #     print(j)
    # testAd = yao.YahooAd(320323, "this is the ad description", 46758,
    #                      "ACTIVE", "this is a test ad", 87292,
    #                      "http://www.yahoo.com", "http://image.jpg", "Sandboxes Inc",
    #                      31369, "http://www.yahoo.com", None, None, None, None, None)

    parsedFile = readinJson(jsonFile)

    yahooAdList = []
    createAdObjects(yahooAdList, parsedFile)

    # Quick check to see if it pulled in the file
    for ad in yahooAdList:
        print(ad.description)

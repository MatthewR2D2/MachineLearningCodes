#!/usr/bin/env python

'''
# Short Description@ The object that defines the yahoo ad object.
# 
# Full Description@ This is the class that will build a python object form the JSON that is recived from the Yahoo
    API. It will use the YahooJsonParser to read in the file and then create the object from what is read in.
    Most of the information here will not be used but added it for future proofing
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

'''
Single ad structure example
{
  "id": 320323,
  "description": "this is the ad description",
  "adGroupId": 46758,
  "status": "ACTIVE",
  "title": "this is a test ad",
  "advertiserId": 87292,
  "landingUrl": "http://www.yahoo.com",
  "imageUrl": "http://image.jpg",
  "sponsoredBy": "Sandboxes Inc",
  "campaignId": 31369,
  "displayUrl": "http://www.yahoo.com",
  "imageUrlHQ": null,
  "contentUrl": null,
  "callToActionText": null,
  "videoPrimaryUrl": null,
  "adName": null,
  "impressionTrackingUrls": {
         "impression": null
      }
}
'''

class YahooAd:
    def __init__(self, id, description, adGroupId, status, title, advertiserId, landingUrl, imageUrl, sponsoredBy,
                 campaignId, displayUrl, imageUrlHQ, contentUrl, callToActionText, videoPrimaryUrl, adName):
        self.id = id
        self.description = description
        self.adGroupId = adGroupId
        self.status = status
        self.title = title
        self.advertiserId = advertiserId
        self.landingUrl = landingUrl
        self.imageUrl = imageUrl
        self.sponsoredBy = sponsoredBy
        self.campaignId = campaignId
        self.displayUrl = displayUrl
        self.imageUrlHQ = imageUrlHQ
        self.contentUrl = contentUrl
        self.callToActionText = callToActionText
        self.videoPrimaryUrl = videoPrimaryUrl
        self.adName = adName







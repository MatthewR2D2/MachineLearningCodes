#!/usr/bin/env python

'''
#This is the AI controller systems that controls the FSM states and changes.
# this is just to control IdeaBit's ads (Google Adwords, YahooAds, FacebookAds)
# This will NOT control their customers ads and manage them.

# This is the main controller for each FSM Ad system. All changes to the FSM will be done through here.
__author__ = "Matthew Millar"
__copyright__ = ""
__credits__ =
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "Matthew Millar"
__email__ = "matthew.millar@igniterlabs.com"
__status__ = "Dev"

'''

import requests

yahooPostURL = "http://ptsv2.com/t/1bgt4-1549605359"


'''
This method will help create each FSM for each Ad services
States available
# START
# ACTIVE
# PAUSED
# ON_HOLD
# REJECTED
# DELETED

FSM flow
START -> ON_HOLD 
                <-> ACTIVE
                            <-> PAUSED
                                        <-> ACTIVE
                                         -> ON_HOLD
                                         -> REJECTED
                                         -> DELETED
                             -> ON_HOLD
                             -> REJECTED
                             -> DELETED
                
                <-> REJECTED
                             -> DELETED
                 -> DELETED
'''

'''
Just need three methods to send to the Yahoo API
Delete the ad
activate the ad
and pause the ad

Rejections will have to be handled manually. 
Oh hold is not accessible and this status is only for reviewing of a AD 
'''

'''
body for adjusting the status
{
  "id": 320323,
  "status": "DELETED"
}
'''

'''
This method is used for deleting the ads by sending the request to the Yahoo API
@:param ad - the ad that will be deleted
'''


def deleteAd(ad):
    print("Sending Cancel Request")
    body = {
        "id": ad.id,
        "status": "DELETED"
    }
    r = requests.post(yahooPostURL, json=body)
    print(r.status_code)
    return r.status_code


'''
This method is used for activate the ads by sending the request to the Yahoo API
@:param ad - the ad that will be activated
'''


def activateAd(ad):
    print("Sending Activate Request")
    body = {
        "id": ad.id,
        "status": "ACTIVE"
    }
    r = requests.post(yahooPostURL, json=body)
    print(r.status_code)
    return r.status_code


'''
This method is used for pausing the ads by sending the request to the Yahoo API
@:param ad - the ad that will be paused
'''


def pauseAd(ad):
    print("Sending Pause Request")
    body = {
        "id": ad.id,
        "status": "PAUSED"
    }
    r = requests.post(yahooPostURL, json=body)
    print(r.status_code)
    return r.status_code


'''
This method is the AI controller when there is a event that occurred
Potential Events
Connot make profit from conversion
Item sold out
Seasonal Items / Season change
@:param: event - this is the event that happened
@:param: currentAds - this is a dictionary of every available ads that are hosted on Yahoo  
'''


def aiControler(event, numberConversions, numberLeads, currentAds):

    messaage = ""
    # Check to see if max conversion is met
    maxLeads = 59 # Total number of conversion b
    if numberLeads >= maxLeads and numberConversions == 0:
        # Pause all the ads and stop them from running
        print("Max Leads met")
        for ads in currentAds:
            ad = ads[1]
            controlFSM(ad, "pause")
            messaage = "Max Leads have been met and Ads have been paused"

    if event == "New Day":
        for ads in currentAds:
            ad = ads[1]
            controlFSM(ad, "activate")
            messaage = "Ads have been activated"
    elif event == "Target Reached":
        for ads in currentAds:
            ad = ads[1]
            controlFSM(ad, "pause")
            messaage = "Target Convergence reached pausing ads"
    elif event == "Stop All Ads":
        for ads in currentAds:
            ad = ads[1]
            controlFSM(ad, "delete")
            messaage = "Stop all ads triggered Deleting all ads"
    elif event == "item sold out":
        for ads in currentAds:
            ad = ads[1]
            controlFSM(ad, "pause")
            messaage = "Item has been sold out, Pausing Ads"
    elif event == "item back in stock":
        for ads in currentAds:
            ad = ads[1]
            controlFSM(ad, 'activate')
            messaage = "Item back in stock, Activating ads"
    elif event == "out of season":
        for ads in currentAds:
            ad = ads[1]
            controlFSM(ad, "delete")
            messaage = "Season ended, deleting ads"

    return messaage


'''
# This is a test controller that takes in a machine and a trigger then set the machine state correctly
@:param ad - this is the ad that is being adjusted
@:param trigger - this is the trigger that or the event that is called
@:return a single message to display on the UI
'''
def controlFSM(ad, trigger):
    resultString = ""
    statusCode = ""

    if trigger == "delete":
        if ad.status == "DELETED":
            resultString = "Ad:{}-ID:{} has already ended and will be removed soon".format(ad.title, ad.id)
        else:
            statusCode = deleteAd(ad)
            resultString = "Ad:{}-ID:{} is being deleted".format(ad.title, ad.id)

    elif trigger == "activate":
        if ad.status == "ACTIVE":
            resultString = "Ad:{}-ID:{} is already Active".format(ad.title, ad.id)
        else:
            if ad.status != "ON_HOLD" and ad.status != "DELETED" and ad.status != "REJECTED":
                statusCode = activateAd(ad)
                resultString = "Ad:{}-ID:{} is being activated".format(ad.title, ad.id)
            else:
                resultString = "Ad:{}-ID:{} is currently {}, and cannot be activated".format(ad.title, ad.id, ad.status)

    elif trigger == "pause":
        if ad.status == "PAUSED":
            resultString = "Ad:{}-ID:{} is already paused".format(ad.title, ad.id)
        else:
            if ad.status != "ON_HOLD" and ad.status != "DELETED" and ad.status != "REJECTED":
                statusCode = pauseAd(ad)
                resultString = "Ad:{}-ID:{} is being paused".format(ad.title, ad.id)
            else:
                resultString = "Ad:{}-ID:{} is currently {}, cannot be paused".format(ad.title, ad.id, ad.status)

    return resultString,  statusCode


'''
# this is an example of how to use the FMS and AI controller together 
'''
if __name__ == '__main__':
    print("Starting Simple Test")

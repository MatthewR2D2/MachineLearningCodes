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

body = {'ids': [12, 14, 50]}


# Open a connection to YahooAPI
# Create Json file to send
# Send this to the endpoint

def deleteAd(ad):
    print("Sending Cancel Request")
    r = requests.post(yahooPostURL, json=body)
    print(r.status_code)


def activateAd(ad):
    print("Sending Activate Request")
    r = requests.post(yahooPostURL, json=body)
    print(r.status_code)


def pauseAd(ad):
    print("Sending Pause Request")
    r = requests.post(yahooPostURL, json=body)
    print(r.status_code)


# This is a test controller that takes in a machine and a trigger then set the machine state correctly
def controlFSM(ad, trigger):
    resultString = ""

    if trigger == "delete":
        if ad.status == "DELETED":
            resultString = "Ad:{}-ID:{} has already ended and will be removed soon".format(ad.title, ad.id)
        else:
            deleteAd(ad)
            resultString = "Ad:{}-ID:{} is being deleted".format(ad.title, ad.id)

    elif trigger == "activate":
        if ad.status == "ACTIVE":
            resultString = "Ad:{}-ID:{} is already Active".format(ad.title, ad.id)
        else:
            activateAd(ad)
            resultString = "Ad:{}-ID:{} is being activated".format(ad.title, ad.id)

    elif trigger == "pause":
        if ad.status == "PAUSED":
            resultString = "Ad:{}-ID:{} is already paused".format(ad.title, ad.id)
        else:
            pauseAd(ad)
            resultString = "Ad:{}-ID:{} is being paused".format(ad.title, ad.id)

    return resultString


'''
# this is an example of how to use the FMS and AI controller together 
'''
if __name__ == '__main__':
    print("Starting Simple Test")

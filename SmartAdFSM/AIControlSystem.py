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


'''
# These methods will interact with the API for Yahoo
deleteAd Will delete the ad from the system and will not be reversible
activateAd will set the status of the ad to Active system
pauseAd will set the status of the ad to Pause in the system
'''
def deleteAd(ad):
    print("Sending Cancel to API for {}".format(ad.id))


def activateAd(ad):
    print("Sending Activate Request to API for {}".format(ad.id))


def pauseAd(ad):
    print("Sending Pause Request to API for {}".format(ad.id))


# This is a test controller that takes in a machine and a trigger then set the machine state correctly
def controlFSM(ad, trigger):

    if trigger == "delete":
        if ad.status == "DELETED":
            print("Ad is all ready ended and will be removed soon")
        else:
            deleteAd(ad)

    elif trigger == "activate":
        if ad.status == "ACTIVE":
            print("Ad is Currently Active")
        else:
            activateAd(ad)

    elif trigger == "pause":
        if ad.status == "PAUSED":
            print("Ad is Currently Paused")
        else:
            pauseAd(ad)






'''
# this is an example of how to use the FMS and AI controller together 
'''
if __name__ == '__main__':
    print("Creating Yahoo ad controler")
    # Create a FSM for yahoo ad and google ad




    activateTrigger = "activate"
    deactivateTrigger = "deactivate"
    endTrigger = "end"
    startTrigger = "Start"

    testYahooAd = ""
    testGoogleAd = ""
    testFaceBookAd = ""

    print("Starting Simple Test")



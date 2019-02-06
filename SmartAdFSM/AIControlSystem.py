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

from SmartAdFSM import YahooFiniteStateMachine as fsm


# This is a test controller that takes in a machine and a trigger then set the machine state correctly
def controlFSM(machine, trigger):
    if trigger == "start":
        if machine.current == "START":
            print('Ad is all ready running')
        else:
            print("You cannot start a ad that has already started")
    elif trigger == "end":
        if machine.current == "DELETED":
            print("Ad is all ready ended")
        else:
            print("Ad is ending")
            machine.end()
    elif trigger == "activate":
        if machine.current == "ACTIVE":
            print("Ad is all ready active")
        else:
            machine.activate()
            print("Ad Activated")
    elif trigger == "deactivate":
        if machine.current == "PAUSED":
            print("Ad is already inactive")
        else:
            machine.deactivate()
            print("Ad is now inactive")


def printStateOfEachMachine(name, machine):
    print('FSM: {} is at state {}'.format(name, machine.current))


'''
# this is an example of how to use the FMS and AI controller together 
'''
if __name__ == '__main__':
    print("Creating Yahoo ad controler")
    # Create a FSM for yahoo ad and google ad
    yahooMachine = fsm.createFSM()
    googleMachine = fsm.createFSM()
    facebookMachine = fsm.createFSM()

    printStateOfEachMachine("Yahoo", yahooMachine)
    printStateOfEachMachine("Google", googleMachine)
    printStateOfEachMachine("Facebook", facebookMachine)

    activateTrigger = "activate"
    deactivateTrigger = "deactivate"
    endTrigger = "end"
    startTrigger = "Start"

    print("Starting Simple Test")
    controlFSM(yahooMachine, startTrigger)
    controlFSM(yahooMachine, activateTrigger)
    controlFSM(yahooMachine, activateTrigger)
    controlFSM(yahooMachine, deactivateTrigger)
    controlFSM(yahooMachine, deactivateTrigger)
    controlFSM(yahooMachine, activateTrigger)
    controlFSM(yahooMachine, startTrigger)
    controlFSM(yahooMachine, activateTrigger)
    print("Simple Test Finished Successfully")

    controlFSM(googleMachine, endTrigger)

    controlFSM(facebookMachine, deactivateTrigger)

    # Create a FSM for yahoo ad
    printStateOfEachMachine("Yahoo", yahooMachine)
    printStateOfEachMachine("Google", googleMachine)
    printStateOfEachMachine("Facebook", facebookMachine)

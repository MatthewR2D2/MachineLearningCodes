#!/usr/bin/env python
'''
#This is the Finite state machine file.

# This will allow you to create multiple FSM for use with each AD for different service providers.
__author__ = "Matthew Millar"
__copyright__ = ""
__credits__ =
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "Matthew Millar"
__email__ = "matthew.millar@igniterlabs.com"
__status__ = "Dev"

'''


"""
This copy right notice is for the use of fysom open source software and not for everything in this file.
This software includes the fysom Library by Maximilien Riehl under the MIT License Agreement
This will handle MIT License agreement.
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
 to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
 and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

'''
This creates all the state machines for each control of the Ad services.
'''

from fysom import *

'''
States that are used
Start Ad: this is the start of the ad when it starts (initialized)
Active Ad: This is when the ad is active and runing on google/yahoo/facebook
Inactive Ad: This is when the ad is stopped for the day. 
End Ad: This is when the ad is closed/cancelled. 

This can be applied to every state machine

This method will help create each FSM for each Ad services
States available
# start
# end
# activate
# deactivate

This method also defines the events that controls the transition between based on outside environment
'''


def createFSM():
    return Fysom({'initial': 'start', 'final': 'endAd',
                  'events':
                      [
                          {'name': 'activate', 'src': ['start', 'inactiveAd'], 'dst': 'activeAd'},
                          {'name': 'deactivate', 'src': ['activeAd', 'start'], 'dst': 'inactiveAd'},
                          {'name': 'end', 'src': ['activeAd', 'start', 'inactiveAd'], 'dst': 'endAd'}]})


'''
# Helper methods for use with testing and working with FSM
'''

'''
This is a recursive FSM testing method
It will allow for you to test changes into each state and will allow for you to 
see if there are any issues
'''


def testStateChange(state):
    print("Starting Testing")
    task = input("What should I do")
    if task == "s":
        if state.current == "start":
            print("Ad is all ready stated, cannot start it again")
            testStateChange(state)
        else:
            print("Invalid Change")
    elif task == "a":
        if state.current == "activeAd":
            print("Ad is all ready active")
            testStateChange(state)
        else:
            state.activate()
            printState(state.current)
            testStateChange(state)
    elif task == "d":
        if state.current == "inactiveAd":
            print("Ad is already inactive")
            testStateChange(state)
        else:
            state.deactivate()
            printState(state.current)
            testStateChange(state)
    elif task == "e":
        state.end()
        printState(state.current)
    else:
        pass


'''
Simple print method to display the current state
'''


def printState(printStatement):
    print("The FMS is: ", printStatement)

def printCurrentState(machine):
    print("The current State is: ", machine.current)

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
# START
# ACTIVE
# PAUSED
# ON_HOLD
# REJECTED
# DELETED

This method also defines the events that controls the transition between based on outside environment
'''


def createFSM():
    return Fysom({'initial': 'START', 'final': 'DELETED',
                  'events':
                      [
                          {'name': 'activate', 'src': ['START', 'PAUSED', 'ON_HOLD'], 'dst': 'ACTIVE'},
                          {'name': 'deactivate', 'src': ['START', 'ACTIVE',  'ON_HOLD'], 'dst': 'PAUSED'},
                          {'name': 'end', 'src': ['START', 'ACTIVE', 'PAUSED', 'ON_HOLD', 'REJECTED'], 'dst': 'DELETED'}]})


'''
# Helper methods for use with testing and working with FSM
'''

'''
This is a recursive FSM testing method
It will allow for you to test changes into each state and will allow for you to 
see if there are any issues
'''


def testStateChange(myFSM):
    print("Starting Testing")
    task = input("What should I do")
    if task == "s":
        if myFSM.current == "START":
            print("Ad is all ready stated, cannot start it again")
            testStateChange(myFSM)
        else:
            print("You cannot restart a running ad")
            testStateChange(myFSM)
    elif task == "a":
        if myFSM.current == "ACTIVE":
            print("Ad is all ready active")
            testStateChange(myFSM)
        else:
            myFSM.activate()
            printState(myFSM.current)
            testStateChange(myFSM)
    elif task == "d":
        if myFSM.current == "PAUSED":
            print("Ad is already inactive")
            testStateChange(myFSM)
        else:
            myFSM.deactivate()
            printState(myFSM.current)
            testStateChange(myFSM)
    elif task == "e":
        myFSM.end()
        printState(myFSM.current)
    else:
        print("Unknow state change retry")
        testStateChange(myFSM)


'''
Simple print method to display the current state
'''


def printState(printStatement):
    print("The FMS is: ", printStatement)

def printCurrentState(machine):
    print("The current State is: ", machine.current)


'''
This is for testing the this python file 
'''
if __name__ == '__main__':
    print("Testing Yahoo FSM Logic")

    myMachine = createFSM()
    printCurrentState(myMachine)
    testStateChange(myMachine)

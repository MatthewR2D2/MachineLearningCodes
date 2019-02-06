#!/usr/bin/env python

'''
# This is the unit test that works with the FSM.

# This file will perform test for changing states from each one to another for the FSM. It will make sure that there is no
issues when there is changes to the system
__author__ = "Matthew Millar"
__copyright__ = ""
__credits__ =
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "Matthew Millar"
__email__ = "matthew.millar@igniterlabs.com"
__status__ = "Dev"

'''

import unittest
from SmartAdFSM import YahooFiniteStateMachine as fsm

class FSMTest(unittest.TestCase):

    def setUp(self):
        self.myMachine = fsm.createFSM()

    # Test the activte function from start active inactive end
    def testSimpleFlow(self):
        # check to see if the current state is start
        self.assertEqual("START", self.myMachine.current)
        # Change state to active
        self.myMachine.activate()
        self.assertEqual("ACTIVE", self.myMachine.current)
        # Change state to inactive
        self.myMachine.deactivate()
        self.assertEqual("PAUSED", self.myMachine.current)
        # Change state to end ad
        self.myMachine.end()
        self.assertEqual("DELETED", self.myMachine.current)

    def testStartToEnd(self):
        # Start with start state then go directly to end state
        self.assertEqual("START", self.myMachine.current)
        # Change state to end ad
        self.myMachine.end()
        self.assertEqual("DELETED", self.myMachine.current)

    def testStartToInactive(self):
        # check to see if the current state is start
        self.assertEqual("START", self.myMachine.current)
        # Change state to inactive
        self.myMachine.deactivate()
        self.assertEqual("PAUSED", self.myMachine.current)

    def testSwitchBetweenActiveInactive(self):
        # check to see if the current state is start
        self.assertEqual("START", self.myMachine.current)
        # Change state to active
        self.myMachine.activate()
        self.assertEqual("ACTIVE", self.myMachine.current)
        # Change state to inactive
        self.myMachine.deactivate()
        self.assertEqual("PAUSED", self.myMachine.current)
        # Change state to active
        self.myMachine.activate()
        self.assertEqual("ACTIVE", self.myMachine.current)
        # Change state to inactive
        self.myMachine.deactivate()
        self.assertEqual("PAUSED", self.myMachine.current)
        # Change state to active
        self.myMachine.activate()
        self.assertEqual("ACTIVE", self.myMachine.current)
        # Change state to inactive
        self.myMachine.deactivate()
        self.assertEqual("PAUSED", self.myMachine.current)




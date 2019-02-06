
'''
# This is the unit test that works with the YahooJsonParser.py.

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
import json
from SmartAdFSM.AdUtility import YahooJsonParser as yjp


class MyTestCase(unittest.TestCase):

    # Checks to see if it can read in a Json file
    def testReadinJson(self):
        jsonFile = "UnitTestData/TestYahooAd.json"
        newFile = yjp.readinJson(jsonFile)
        self.assertIsNotNone(newFile)

    # Test for parsing the read in json file and checking its contents
    def testParseing(self):
        jsonFile = "UnitTestData/TestYahooAd.json"
        newFile = yjp.readinJson(jsonFile)
        adObjectList = []
        yjp.createAdObjects(adObjectList, newFile)
        self.assertIsNotNone(adObjectList)

        for ad in adObjectList:
            self.assertEqual(320324, ad.id)
            self.assertEqual("this is the ad description", ad.description)
            self.assertEqual(46758, ad.adGroupId)
            self.assertEqual("ACTIVE", ad.status)
            self.assertEqual("batch call ad 1", ad.title)
            self.assertEqual(87292, ad.advertiserId)
            self.assertEqual("http://www.yahoo.com", ad.landingUrl)
            self.assertEqual("http://image1.jpg", ad.imageUrl)
            self.assertEqual("Sandboxes Inc", ad.sponsoredBy)
            self.assertEqual(31369, ad.campaignId)
            self.assertEqual("http://www.yahoo.com", ad.displayUrl)
            self.assertEqual(None, ad.imageUrlHQ)
            self.assertEqual(None, ad.contentUrl)
            self.assertEqual(None, ad.callToActionText)
            self.assertEqual(None, ad.videoPrimaryUrl)
            self.assertEqual(None, ad.adName)


if __name__ == '__main__':
    unittest.main()

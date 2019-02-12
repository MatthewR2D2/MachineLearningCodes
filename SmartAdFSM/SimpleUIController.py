from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

# AI devices imports
from SmartAdFSM import AIControlSystem as aic
from SmartAdFSM.AdUtility import AdHelperMethods as ahm
import requests

# Varialbes that are collected from differnt APIs
# TODO:Replace with real ads from Google/Yahoo/Facebook
# TODO: Create method to gather all avalialbe ads from service providers and create
#  1: list of all ads form API, '(Yahoo, Google, Facebook)

# Links to Json Files
jsonFile = "TestAds/YahooAd.json"
yahooGetAPIURL = "https://api.jsonbin.io/b/5c6244031198012fc894e9ca"  # Change this to the one for ads

# Tell this to either read from a file or from a url
readFromFile = True
if readFromFile:
    myJson = jsonFile
else:
    # Request method for getting the Json file from Yahoo API
    r = requests.get(yahooGetAPIURL)
    myJson = r.json()

# List for ads
# They are broken up first by service provider then added into a master list
currentAds = []  # This holds every add from every service provider.
apiYahooAds = []  # This holds every yahoo add

# Call method from AdHelperMethods to create the yahoo ad and add it to the currentAds list
ahm.CreateYahooAdList(readFromFile, myJson, apiYahooAds, currentAds)

# Add ad values into the list for dropdown menu
dropdownAdValues = []  # names of each ad

'''
Button methods that will handle the UI input for button clicks
'''

'''
This is the initial button click event. This works for all buttons
@:param dropdown - this is the dropdownWidget which the input to the function 
@:param event - this is the event that triggers something it may be manual or from another event outside
'''


def handleClick(dropdown, event):
    # this gets the string from the dropdown menu
    targetString = dropdown.get()
    apiHost = targetString.split(":")[0]  # Who is hosting the ad (yahoo/google/facebook)
    target = targetString.split(":")[1]  # The title of the Ad
    stat = targetString.split(":")[2]  # the current status of the ad
    # Preform all task like sending things to the service provider
    eventListener(target, event)
    # Reset the UI by calling the change from the
    ahm.CreateYahooAdList(readFromFile, myJson, apiYahooAds, currentAds)
    # Create the UI values and update the UI
    ahm.UpdateUIValues(dropdownAdValues, currentAds)
    ahm.UpdateUI(dropdown, dropdownAdValues)


'''
This method will be used to handle the event that was triggered
@:param targetAd is a single ad which will will be changed either yahoo/google/facebook
@:param event - this is the event
'''


def eventListener(targetAd, event):
    for ad in currentAds:
        ad = ad[1]
        if targetAd == ad.title:
            msg = aic.controlFSM(ad, event)
            messagebox.showinfo("Alert", msg)


'''
This passes the events and ads to the AI controller
@:param event - which is the event that are the tirggers
@:param allAds - this is all the ads that are available to use. 
'''


def aiHandler(event, allAds):
    aic.aiControler(event, allAds)


'''
This is the simple User interface which can be used to manually interact with the ads online from one single
access point. 
'''

window = Tk()

window.title("SmartAd Manager IgniterLabs")
window.geometry("800x400")

# Widgets

# Labels for UI
mainLabel = Label(window, text="Welcome to SmartAd management Tool", font=("Arial Bold", 12))
activeAdsLabel = Label(window, text="Current Ads Available")
manualButtonLabel = Label(window, text="Manual Override Buttons", font=("Arial Bold", 12))
simulationLabel = Label(window, text="Simulation Buttons for AI Event handler", font=("Arial Bold", 12))

# Combo box to select the Ad
dropdownMenu = Combobox(window, width=40)
# Initial Setup of values
ahm.UpdateUIValues(dropdownAdValues, currentAds)
ahm.UpdateUI(dropdownMenu, dropdownAdValues)

# Manual User override buttons
# Activate button
activateButton = Button(window, text="Activate Ad", command=lambda: handleClick(dropdownMenu, "activate"))
# Deactivate Button
deactivateButton = Button(window, text="Deactivate Ad", command=lambda: handleClick(dropdownMenu, "pause"))
# End Button
endButton = Button(window, text="End Ad", command=lambda: handleClick(dropdownMenu, "delete"))


# Simulation buttons should be removed later on
stopAllAdsButton = Button(window, text="Simulate Stop All Ads", command=lambda: aiHandler("Stop All Ads", currentAds))
targetMetButton = Button(window, text="Simulate Target Met", command=lambda: aiHandler("Target Reached", currentAds))
newDayButton = Button(window, text="Start a New Day", command=lambda: aiHandler("New Day", currentAds))

# Menu Button
# Quit button
quitButton = Button(window, text="Quit", command=quit)

# Set main label position on grid
mainLabel.grid(sticky=W, column=0, row=0, columnspan=3)
quitButton.grid(column=3, row=0)

activeAdsLabel.grid(sticky=W, column=0, row=1)
dropdownMenu.grid(sticky=W, column=1, row=1, columnspan=3)

manualButtonLabel.grid(sticky=W, column=0, row=2)
activateButton.grid(sticky=W + E, column=0, row=3)
deactivateButton.grid(sticky=W + E, column=1, row=3)
endButton.grid(sticky=W + E, column=2, row=3)

simulationLabel.grid(sticky=W, column=0, row=4)
targetMetButton.grid(sticky=W, column=0, row=5)
newDayButton.grid(sticky=W + E, column=1, row=5)
stopAllAdsButton.grid(sticky=W + E, column=2, row=5)

window.mainloop()

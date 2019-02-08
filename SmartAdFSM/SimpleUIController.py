from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
from tkinter import messagebox

# AI devices imports
from SmartAdFSM import AIControlSystem as aic
from SmartAdFSM.AdUtility import YahooJsonParser as yjp
from SmartAdFSM.AdUtility import AdHelperMethods as ahm

# Varialbes that are collected from differnt APIs
# TODO:Replace with real ads from Google/Yahoo/Facebook
# TODO: Create method to gather all avalialbe ads from service providers and create
#  1: list of all ads form API, '(Yahoo, Google, Facebook)
#  2: FSM for all ads


# List for ads
# They are broken up first by service provider then added into a master list
currentAds = []        # This holds every add from every service provider.
apiYahooAds = []  # This holds every yahoo add

# Test Ad simulate call from API
# TODO: Create call to API for Yahoo Ad to get every ad that is available
jsonFile = "TestAds/YahooAd.json"
# read in the file
parsedFile = yjp.readinJson(jsonFile)
# create objects for each ad and add them into the Yahoo Ad list
yjp.createAdObjects(apiYahooAds, parsedFile)

# Ad yahoo ads to current Ads
for ad in apiYahooAds:
    currentAds.append((ad))

# Add ad values into the list for dropdown and fsm
dropdownAdValues = []  # names of each ad



'''
Button methods that will handle the UI input for button clicks
'''

def handleClick(dropdown, event):
    targetString = dropdown.get()
    target= targetString.split(":")[0]
    stat = targetString.split(":")[1]
    eventListener(target, stat, event)

def eventListener(targetAd, stat, event):
    print("Target:{} CurrentStatus: {} event {}".format(targetAd, stat, event))

    for ad in currentAds:
        if targetAd == ad.title:
            aic.controlFSM(ad, event)
            msg = "AD:{}-{} is being {}".format(ad.title,ad.id, event)
            messagebox.showinfo("Alert", msg)


window = Tk()

window.title("SmartAd Manager IgniterLabs")
window.geometry("600x360")

# Widgets

# Labels for UI
mainLabel = Label(window, text="Welcome to SmartAd management Tool", font=("Arial Bold", 12))
activeAdsLabel = Label(window, text="Current Ads Available")
manualButtonLabel = Label(window, text="Manual Override Buttons", font=("Arial Bold", 12))

# Combo box to select the Ad
dropdownMenu = Combobox(window)
ahm.UpdateUIValues(dropdownAdValues, currentAds)
ahm.UpdateUI(dropdownMenu, dropdownAdValues)

# Manual User override buttons
# Activate button
activateButton = Button(window, text="Activate Ad", command=lambda: handleClick(dropdownMenu, "activate"))
# Deactivate Button
deactivateButton = Button(window, text="Deactivate Ad", command=lambda: handleClick(dropdownMenu, "pause"))
# End Button
endButton = Button(window, text="End Ad", command=lambda: handleClick(dropdownMenu, "delete"))

# Menu Button
# Quit button
quitButton = Button(window, text="Quit",command=quit)


# Set main label position on grid
mainLabel.grid(sticky= W, column=0, row=0, columnspan=3)
quitButton.grid(column=2, row=0)

activeAdsLabel.grid(sticky=W, column=0, row=1)
dropdownMenu.grid(sticky=W, column=1, row=1)

manualButtonLabel.grid(sticky=W, column=0, row=2)
activateButton.grid(sticky=W+E, column=0, row=3)
deactivateButton.grid(sticky=W+E,column=1, row=3)
endButton.grid(sticky=W+E,column=2, row=3)



window.mainloop()

from tkinter import *
from tkinter.ttk import *
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

ahm.CreateYahooAdList(jsonFile,apiYahooAds,currentAds)

# Add ad values into the list for dropdown and fsm
dropdownAdValues = []  # names of each ad



'''
Button methods that will handle the UI input for button clicks
'''

def handleClick(dropdown, event):
    targetString = dropdown.get()
    apiHost = targetString.split(":")[0]
    target= targetString.split(":")[1]
    stat = targetString.split(":")[2]
    # Preform all task like sending things to the service provider
    eventListener(target, event)

    ahm.CreateYahooAdList(jsonFile,apiYahooAds,currentAds)
    ahm.UpdateUIValues(dropdownAdValues, currentAds)
    ahm.UpdateUI(dropdown,dropdownAdValues)

def eventListener(targetAd,event):
    for ad in currentAds:
        ad = ad[1]
        if targetAd == ad.title:
            msg = aic.controlFSM(ad, event)
            messagebox.showinfo("Alert", msg)


window = Tk()

window.title("SmartAd Manager IgniterLabs")
window.geometry("800x400")

# Widgets

# Labels for UI
mainLabel = Label(window, text="Welcome to SmartAd management Tool", font=("Arial Bold", 12))
activeAdsLabel = Label(window, text="Current Ads Available")
manualButtonLabel = Label(window, text="Manual Override Buttons", font=("Arial Bold", 12))

# Combo box to select the Ad
dropdownMenu = Combobox(window, width=40)
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
quitButton.grid(column=3, row=0)

activeAdsLabel.grid(sticky=W, column=0, row=1)
dropdownMenu.grid(sticky=W, column=1, row=1, columnspan=3)

manualButtonLabel.grid(sticky=W, column=0, row=2)
activateButton.grid(sticky=W+E, column=0, row=3)
deactivateButton.grid(sticky=W+E,column=1, row=3)
endButton.grid(sticky=W+E,column=2, row=3)



window.mainloop()

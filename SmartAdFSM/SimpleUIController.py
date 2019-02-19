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

# Add ad values into the list for listbox menu
adValues = []  # names of each ad

'''
Button methods that will handle the UI input for button clicks
'''

'''
This is the initial button click event. This works for all buttons
@:param listbox - this is the listbox window which the input to the function 
@:param event - this is the event that triggers something it may be manual or from another event outside
'''


def handleClick(listBox, event):

    listboxTarget = listBox.get(ACTIVE)
    print("List Target", listboxTarget)
    apiHost = listboxTarget.split(":")[0]  # Who is hosting the ad (yahoo/google/facebook)
    target = listboxTarget.split(":")[1]  # The title of the Ad
    stat = listboxTarget.split(":")[2]  # the current status of the ad
    # Preform all task like sending things to the service provider

    # Reset the UI by calling the change from the
    # Look at each host for each API
    if apiHost == "Yahoo":
        # Preform event manager task
        eventListener(target, event)
        # Create each ad for Yahoo vendor
        ahm.CreateYahooAdList(readFromFile, myJson, apiYahooAds, currentAds)
    elif apiHost == "Google":
        print("Google is not supported yet")
        # eventListener(target, event)
    elif apiHost == "Facebook":
        print("Facebook is not supported yet")
        # eventListener(target, event)
    else:
        print("Missing API Host provider")

    # Create the UI values and update the UI
    ahm.UpdateUIValues(adValues, currentAds)
    ahm.UpdateUI(listBox, adValues)


'''
This method will be used to handle the event that was triggered
@:param targetAd is a single ad which will will be changed either yahoo/google/facebook
@:param event - this is the event
'''


def eventListener(targetAd, event):
    for ad in currentAds:
        ad = ad[1]
        if targetAd == ad.title:
            msg, responseCode = aic.controlFSM(ad, event)
            if responseCode == "":
                responseCode = "Not Sent"
            pastMessage = msg + ": Status: " + str(responseCode)
            # Clear textbox
            textBox.delete(1.0, END)
            # Add new message
            textBox.insert(INSERT, pastMessage)
            messagebox.showinfo("Alert", msg)


'''
This passes the events and ads to the AI controller
@:param event - which is the event that are the tirggers
@:param allAds - this is all the ads that are available to use. 
'''


def aiHandler(event, numberConversions, numberLeads,  allAds):
    message = aic.aiControler(event, numberConversions, numberLeads, allAds)
    # Clear textbox
    textBox.delete(1.0, END)
    # Add new message
    textBox.insert(INSERT, message)


'''
This is the simple User interface which can be used to manually interact with the ads online from one single
access point. 
'''

window = Tk()

window.title("SmartAd Manager IgniterLabs")
window.geometry("800x400")

# Widgets

# Labels for UI
mainLabel = Label(window, text="SmartAd 管理ツール", font=("Arial Bold", 12))
activeAdsLabel = Label(window, text="現在利用可能な広告")
manualButtonLabel = Label(window, text="手動オーバーライドボタン", font=("Arial Bold", 12))
simulationLabel = Label(window, text="AIイベントハンドラのシミュレーションボタン", font=("Arial Bold", 12))
messageLabel = Label(window,  text="Output Message", font=("Arial Bold", 12))


# Initial Setup of values
listboxMenu = Listbox(window, width= 30)
ahm.UpdateUIValues(adValues, currentAds)
ahm.UpdateUI(listboxMenu, adValues)

# Manual User override buttons
# Activate button
activateButton = Button(window, text="活性化する AD AA", command=lambda: handleClick(listboxMenu, "activate"))
# Deactivate Button
deactivateButton = Button(window, text="無効にする AD PA", command=lambda: handleClick(listboxMenu, "pause"))
# End Button
endButton = Button(window, text="削除する AD EA", command=lambda: handleClick(listboxMenu, "delete"))


# Simulation buttons should be removed later on
stopAllAdsButton = Button(window, text="すべて削除する AD SAA", command=lambda: aiHandler("Stop All Ads", 5, 10, currentAds))
targetMetButton = Button(window, text="目標を達成 STM", command=lambda: aiHandler("Target Reached", 15, 60, currentAds))
newDayButton = Button(window, text="新しい日 SND", command=lambda: aiHandler("New Day",0, 0, currentAds))

# Menu Button
# Quit button
quitButton = Button(window, text="終了する", command=quit)

# Message text widget
textBox = Text(window, height = 2, width = 30)
textBox.insert(INSERT, "Welcome")


# Set main label position on grid
mainLabel.grid(sticky=W, column=0, row=0, columnspan=4)
quitButton.grid(column=3, row=0)

manualButtonLabel.grid(sticky=W, column=0, row=1, columnspan=3)
activateButton.grid(sticky=W + E, column=0, row=2)
deactivateButton.grid(sticky=W + E, column=1, row=2)
endButton.grid(sticky=W + E, column=2, row=2)

simulationLabel.grid(sticky=W, column=0, row=3, columnspan=4)
targetMetButton.grid(sticky=W, column=0, row=4)
newDayButton.grid(sticky=W + E, column=1, row=4)
stopAllAdsButton.grid(sticky=W + E, column=2, row=4)

activeAdsLabel.grid(sticky=W, column=0, row=5)
listboxMenu.grid(sticky=W + E, column=0, row=6, columnspan=5)
messageLabel.grid(sticky=W + E, column=0, row=7, columnspan=5)
textBox.grid(sticky=W + E, column=0, row=8, columnspan=5)

window.mainloop()

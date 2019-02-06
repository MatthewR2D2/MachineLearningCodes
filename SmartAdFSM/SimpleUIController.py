from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
from tkinter import messagebox

# AI devices imports
from SmartAdFSM import AIControlSystem as aic
from SmartAdFSM.AdUtility import YahooJsonParser as yjp

# Varialbes that are collected from differnt APIs
# TODO:Replace with real ads from Google/Yahoo/Facebook
# TODO: Create method to gather all avalialbe ads from service providers and create
#  1: list of all ads form API, '(Yahoo, Google, Facebook)
#  2: FSM for all ads


# List for ads
# They are broken up first by service provider then added into a master list
myAds = []        # This holds every add from every service provider.
apiYahooAds = []  # This holds every yahoo add

# Test Ad simulate call from API
# TODO: Create call to API for Yahoo Ad to get every ad that is available
jsonFile = "TestAds/YahooAd.json"
# read in the file
parsedFile = yjp.readinJson(jsonFile)
# create objects for each ad and add them into the Yahoo Ad list
yjp.createAdObjects(apiYahooAds, parsedFile)

for ad in apiYahooAds:
    myAds.append((ad))

# print("Test add")
# for ad in myAds:
#     print(ad)
#     print(ad[0].id)
#     print(ad[1].current)



# Add ad values into the list for dropdown and fsm
dropdownAdValues = []  # names of each ad
activeAds = []  # The FSM for each ad
for ad in myAds:
    title = ad.title
    dropdownAdValues.append(title)
    activeAds.append(title + "\n")

'''
Button methods that will handle the UI input for button clicks
'''


def activateClicked():
    target = combo.get()
    msg = "{} Ad is now active".format(target)
    for targetAd in myAds:
        if target == targetAd.title:
            aic.controlFSM(targetAd, "activate")
            messagebox.showinfo('Action', msg)
            break


def deactivateClicked():
    target = combo.get()
    msg = "{} Ad in now inactive".format(target)
    for targetAd in myAds:
        if target == targetAd.title:
            aic.controlFSM(targetAd, "pause")
            messagebox.showinfo('Action', msg)
            break


def endClicked():
    target = combo.get()
    msg = "{} Ad in now ended".format(target)
    for targetAd in myAds:
        if target == targetAd.title:
            aic.controlFSM(targetAd,  "delete")
            messagebox.showinfo('Action', msg)
            # Make sure to remove this from the list
            #myAds.remove(targetAd) # This will remove the ad from the list
            # update all feilds
            break


window = Tk()

window.title("SmartAd Manager IgniterLabs")
window.geometry("600x360")

# Widgets

mainLabel = Label(window, text="Welcome to SmartAd management Tool",
                  font=("Arial Bold", 12))
# Activate button
activateButton = Button(window, text="Activate Ad",
                        command=activateClicked)
# Deactivate Button
deactivateButton = Button(window, text="Deactivate Ad",
                          command=deactivateClicked)

# End Button
endButton = Button(window, text="End Ad",
                   command=endClicked)
# Quit button
quitButton = Button(window, text="Quit",
                    command=quit)

# Combo box to select the Ad
combo = Combobox(window)
# Set the dropdownmenu contents
combo['values'] = dropdownAdValues
# The init value
combo.current(0)

activeAdsLabel = Label(window, text="Current Ads Available")

# Text filed for user
textFeild = scrolledtext.ScrolledText(window, width=40, height=10)
# set the textfeild' contents
for actAds in activeAds:
    textFeild.insert(INSERT, actAds)

# Set main label position on grid
mainLabel.grid(column=0, row=0)
combo.grid(column=0, row=1)
activateButton.grid(column=1, row=1)
deactivateButton.grid(column=2, row=1)
endButton.grid(column=3, row=1)
activeAdsLabel.grid(column=0, row=2)
textFeild.grid(column=0, row=3)
quitButton.grid(column=0, row=4)

window.mainloop()

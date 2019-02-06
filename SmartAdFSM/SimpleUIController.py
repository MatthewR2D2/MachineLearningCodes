from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
from tkinter import messagebox

# AI devices imports
from SmartAdFSM import AIControlSystem as aic
from SmartAdFSM import FiniteStateMachine as fsm

# Varialbes that are collected from differnt APIs
# TODO:Replace with real ads from Google/Yahoo/Facebook
# TODO: Create method to gather all avalialbe ads from service providers and create
#  1: list of all ads,
#  2: FSM for all ads

# This holds the list of all available ads
myAds = []

# Create fake ads for initial input
yahooAd = fsm.createFSM()
googleAd = fsm.createFSM()

myAds.append(("Yahoo", yahooAd))
myAds.append(("Google", googleAd))

# Simple loop through the ads to see what is there
for ads in myAds:
    name = ads[0]
    machine = ads[1]
    aic.printStateOfEachMachine(name, machine)

# Add ad values into the list for dropdown and fsm
dropdownAdValues = []  # names of each ad
activeAds = []  # The FSM for each ad
for ad in myAds:
    dropdownAdValues.append(ad[0])
    activeAds.append(ad[1])

'''
Button methods that will handle the UI input for button clicks
'''


def activateClicked():
    target = combo.get()
    msg = "{} Ad is now active".format(target)
    for targetAd in myAds:
        if target == targetAd[0]:
            aic.controlFSM(targetAd[1], "activate")
            messagebox.showinfo('Action', msg)
            break


def deactivateClicked():
    target = combo.get()
    msg = "{} Ad in now inactive".format(target)
    for targetAd in myAds:
        if target == targetAd[0]:
            aic.controlFSM(targetAd[1], "deactivate")
            messagebox.showinfo('Action', msg)
            break

def endClicked():
    target = combo.get()
    msg = "{} Ad in now ended".format(target)
    for targetAd in myAds:
        if target == targetAd[0]:
            aic.controlFSM(targetAd[1], "end")
            messagebox.showinfo('Action', msg)
            # Make sure to remove this from the list
            myAds.remove(targetAd)
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
textFeild.insert(INSERT, activeAds)

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

from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
from tkinter import messagebox

#AI devices

#Varialbes that are collected from differnt APIs
# TODO:Replace with real ads from Google/Yahoo/Facebook
dropdownAdValues = ('YahooAd', "GoogleAd", "FackbookAd")
activeAds = ("New Prodcut \nSale \nBuy One Get One Free \nBuy two get two for two")

def activateClicked():
    target = combo.get()
    msg = "{} Ad is now active".format(target)
    messagebox.showinfo('Action', msg)

def deactivateClicked():
    target = combo.get()
    msg= "{} Ad in now inactive".format(target)
    messagebox.showinfo('Action', msg)

window = Tk()

window.title("SmartAd Manager IgniterLabs")
window.geometry("600x360")

#Widgets

mainLabel = Label(window, text = "Welcome to SmartAd management Tool",
                  font=("Arial Bold", 12))
# Activate button
activateButton = Button(window, text="Activate Ad",
                        command=activateClicked)
# Deactivate Button
deactivateButton = Button(window, text="Deactivate Ad",
                          command = deactivateClicked)
#Quit button
quitButton = Button(window, text="Quit",
                    command=quit)

# Combo box to select the Ad
combo = Combobox(window)
# Set the dropdownmenu contents
combo['values'] = dropdownAdValues
# The init value
combo.current(0)

activeAdsLabel = Label(window, text="Current Ads Avaliable")

# Text filed for user
textFeild = scrolledtext.ScrolledText(window, width=40, height=10)
# set the textfeild' contents
textFeild.insert(INSERT, activeAds)

#Set main label position on grid
mainLabel.grid(column=0, row=0)
combo.grid(column=0, row=1)
activateButton.grid(column=1, row=1)
deactivateButton.grid(column=2, row=1)
activeAdsLabel.grid(column=0, row=2)
textFeild.grid(column=0, row=3)
quitButton.grid(column=0, row=4)

window.mainloop()
from tkinter import Tk, Button, Label, Frame
from functools import partial
import configparser

SpellTracker = configparser.ConfigParser()
SpellTracker.read('SpellSlots.ini')

# Defaults for Background and fonts
Background = 'LightSteelBlue1'
BoldBaseFont = "Arial Bold"
BaseFont = "Arial"

# Start of Tkinter interface
SpellSlots = Tk()
SpellSlots.title("Spell Slot Counter")
SpellSlots.geometry("464x605")
SpellSlots.iconbitmap('Fireball Icon.ico')
SpellSlots.configure(bg=Background)

TitleFrame = Frame(SpellSlots, bg=Background)
TitleFrame.grid(columnspan=2, pady=(5, 5))


# ini.get Functions
def GetCharacterName():
    return SpellTracker.get('Main', 'CharacterName')


def SpellsKnown(Lvl):
    return int(SpellTracker.get('Level ' + str(Lvl) + ' Spells', 'Spells Known'))


def SpellsLeft(Lvl):
    return int(SpellTracker.get('Level ' + str(Lvl) + ' Spells', 'Spells Left'))


def SpellsPerDay(Lvl):
    return int(SpellTracker.get('Level ' + str(Lvl) + ' Spells', 'Spells Per Day'))


# Use Spell Functions
def WriteToSpellTracker():
    with open('SpellSlots.ini', 'w') as configfile:
        SpellTracker.write(configfile)


Title = Label(TitleFrame, text="Spell Slot Counter", font=(BoldBaseFont, 20), bg=Background).grid(columnspan=2, pady=(5, 5))
CharacterName = Label(TitleFrame, text="for " + str(GetCharacterName()), font=(BoldBaseFont, 20), bg=Background).grid(columnspan=2)

# Spell Level Info and Buttons
SpellInfoList = []
SpellButtonList = []
for x in range(1, 10):
    SpellInfoList.append(Label(SpellSlots))
    SpellButtonList.append(Button(SpellSlots))


def SpellUsedButton(SlotNumber):
    if int(SpellTracker.get('Level ' + str(SlotNumber) + ' Spells', 'Spells Left')) > 1:
        SpellTracker.set('Level ' + str(SlotNumber) + ' Spells', 'Spells Left', str(int(SpellTracker.get('Level ' + str(SlotNumber) + ' Spells', 'Spells Left')) - 1))
        SpellInfoList[SlotNumber - 1].config(text="Level " + str(SlotNumber) + " - " + str(SpellTracker.get('Level ' + str(SlotNumber) + ' Spells', 'Spells Left')) + " Spells left of " + str(SpellTracker.get('Level ' + str(SlotNumber) + ' Spells', 'spells per day')))
        WriteToSpellTracker()
        print('1 Spell Used')
    else:
        SpellTracker.set('Level ' + str(SlotNumber) + ' Spells', 'Spells Left', '0')
        WriteToSpellTracker()
        SpellInfoList[SlotNumber - 1].config(text='Level ' + str(SlotNumber) + ' - No Slots left      ')
        SpellButtonList[SlotNumber - 1].config(state='disabled')
        print('Spell Level Spent')


def ResetSlots():
    for SpellLevel in range(1, 10):
        SpellTracker.set('Level ' + str(SpellLevel) + ' Spells', 'Spells Left', str(SpellTracker.get('Level ' + str(SpellLevel) + ' Spells', 'spells per day')))
        WriteToSpellTracker()
        if int(SpellTracker.get('Level ' + str(SpellLevel) + ' Spells', 'Spells Known')) > 0:
            SpellInfoList[SpellLevel-1].config(text="Level " + str(SpellLevel) + " - " + str(SpellTracker.get('Level ' + str(SpellLevel) + ' Spells', 'Spells Left')) + " Spells left of " + str(SpellTracker.get('Level ' + str(SpellLevel) + ' Spells', 'spells per day')))
            SpellButtonList[SpellLevel-1].config(state='normal')
            print('Level ' + str(SpellLevel) + ' Slot Reset')
        else:
            pass


RowCounter = 0
# Spell Level Tkinter Labels
for lbl in SpellInfoList:
    if SpellsKnown(RowCounter+1) > 0 and SpellsLeft(RowCounter+1) > 0:
        lbl.config(text="Level " + str(RowCounter+1) + " - " + str(SpellTracker.get('Level ' + str(RowCounter+1) + ' Spells', 'Spells Left')) + " Spells left of " + str(SpellTracker.get('Level ' + str(RowCounter+1) + ' Spells', 'spells per day')), font=(BaseFont, 15), bg=Background)
        lbl.grid(column=0, row=RowCounter + 2, padx=(20, 10))
    elif int(SpellTracker.get('Level ' + str(RowCounter+1) + ' Spells', 'Spells Known')) > 0 and int(SpellTracker.get('Level ' + str(RowCounter+1) + ' Spells', 'Spells Left')) < 1:
        lbl.config(text='Level ' + str(RowCounter+1) + ' - No Slots left      ')

    else:
        lbl.config(text="Level " + str(RowCounter+1) + " - No Spells Known", font=(BaseFont, 15), bg=Background)
        lbl.grid(column=0, row=RowCounter + 2, padx=(20, 10))
    RowCounter += 1


RowCounter = 0
# Spell Level Tkinter Buttons for using Spells
for button in SpellButtonList:
    if int(SpellTracker.get('Level ' + str(RowCounter+1) + ' Spells', 'Spells Known')) > 1 and int(SpellTracker.get('Level ' + str(RowCounter+1) + ' Spells', 'Spells Left')) > 0:
        button.config(text="Use Level "+str(RowCounter+1)+" Spell", font=(BaseFont, 15), command=partial(SpellUsedButton, (RowCounter + 1)))
        button.grid(column=1, row=RowCounter + 2, pady=5, padx=(4, 20))
    else:
        button.config(text="Use Level "+str(RowCounter+1)+" Spell", font=(BaseFont, 15), state='disabled', command=partial(SpellUsedButton, (RowCounter + 1)))
        button.grid(column=1, row=RowCounter + 2, pady=5, padx=(4, 20))
    RowCounter += 1

LongRest = Button(SpellSlots, text="Long Rest - Reset Slots", command=ResetSlots, font=(BaseFont, 14))
LongRest.grid(columnspan=2, row=11, pady=10)

SpellSlots.mainloop()

from tkinter import Tk, Button, Label, Frame
from functools import partial
from tkinter import ttk
import shutil
import configparser
import subprocess
import os

CWD = os.getcwd()

# Defaults for Background and fonts
Background = 'LightSteelBlue1'
BoldBaseFont = "Arial Bold"
BaseFont = "Arial"
FontColor = "Black"


def create_window(Save):
    CurrentSave = Save.get()
    SpellTracker = configparser.ConfigParser()
    SpellTracker.read(f'Saves/{Save.get()}')

    # Start of Tkinter interface
    Prompt.destroy()
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
        return int(SpellTracker.get(f'Level {str(Lvl)} Spells', 'Spells Known'))

    def SpellsLeft(Lvl):
        return int(SpellTracker.get(f'Level {str(Lvl)} Spells', 'Spells Left'))

    def SpellsPerDay(Lvl):
        return int(SpellTracker.get(f'Level {str(Lvl)} Spells', 'Spells Per Day'))

    # Use Spell Functions
    def WriteToSpellTracker(WriteToName):
        with open(WriteToName, 'w') as configfile:
            SpellTracker.write(configfile)

    Title = Label(TitleFrame, text=f"Spell Slot Counter\nfor {str(GetCharacterName())}",
                  font=(BoldBaseFont, 20), fg=FontColor, bg=Background)
    Title.grid(column=0, row=0)

    # Spell Level Info and Buttons
    SpellInfoList = []
    SpellButtonList = []
    for x in range(1, 10):
        SpellInfoList.append(Label(SpellSlots))
        SpellButtonList.append(Button(SpellSlots))

    def SpellUsedButton(SlotNumber, SetName):
        if int(SpellsLeft(SlotNumber)) > 1:
            SpellTracker.set('Level ' + str(SlotNumber) + ' Spells', 'Spells Left', str(SpellsLeft(SlotNumber)-1))
            SpellInfoList[SlotNumber - 1].config(text="Level " + str(SlotNumber) + " - " + str(SpellsLeft(SlotNumber))
                                                      + " Spells left of " + str(SpellsPerDay(SlotNumber)))
            WriteToSpellTracker(f'Saves/{SetName}')
            print('1 Spell Used')
        else:
            SpellTracker.set('Level ' + str(SlotNumber) + ' Spells', 'Spells Left', '0')
            WriteToSpellTracker(f'Saves/{SetName}')
            SpellInfoList[SlotNumber - 1].config(text='Level ' + str(SlotNumber) + ' - No Slots left      ')
            SpellButtonList[SlotNumber - 1].config(state='disabled')
            print('Spell Level Spent')

    def ResetSlots(SetSave):
        for SpellLevel in range(1, 10):
            SpellTracker.set('Level ' + str(SpellLevel) + ' Spells', 'Spells Left', str(SpellsPerDay(SpellLevel)))
            WriteToSpellTracker(f'Saves/{SetSave}')
            if int(SpellsKnown(SpellLevel)) > 0:
                SpellInfoList[SpellLevel-1].config(
                    text="Level " + str(SpellLevel) + " - " + str(SpellsLeft(SpellLevel)) + " Spells left of "
                         + str(SpellsPerDay(SpellLevel)))
                SpellButtonList[SpellLevel-1].config(state='normal')
                print('Level ' + str(SpellLevel) + ' Slot Reset')
            else:
                pass

    RowCounter = 0
    # Spell Level Tkinter Labels
    for lbl in SpellInfoList:
        if SpellsKnown(RowCounter+1) > 0 and SpellsLeft(RowCounter+1) > 0:
            lbl.config(text="Level " + str(RowCounter+1) + " - " + str(SpellsLeft(RowCounter+1)) + " Spells left of " +
                            str(SpellsPerDay(RowCounter+1)), font=(BaseFont, 15), bg=Background)
            lbl.grid(column=0, row=RowCounter + 2, padx=(20, 10))
        elif int(SpellsKnown(RowCounter+1)) > 0 and int(SpellsLeft(RowCounter+1)) < 1:
            lbl.config(text='Level ' + str(RowCounter+1) + ' - No Slots left      ')

        else:
            lbl.config(text="Level " + str(RowCounter+1) + " - No Spells Known", font=(BaseFont, 15), bg=Background)
            lbl.grid(column=0, row=RowCounter + 2, padx=(20, 10))
        RowCounter += 1

    RowCounter = 0
    # Spell Level Tkinter Buttons for using Spells
    for button in SpellButtonList:
        if int(SpellsKnown(RowCounter+1)) > 0 and int(SpellsLeft(RowCounter+1)) > 0:
            button.config(text="Use Level "+str(RowCounter+1) +
                               " Spell", font=(BaseFont, 15),
                          command=partial(SpellUsedButton, (RowCounter + 1), CurrentSave))
            button.grid(column=1, row=RowCounter + 2, pady=5, padx=(4, 20))
        else:
            button.config(text="Use Level "+str(RowCounter+1) + " Spell",
                          font=(BaseFont, 15), state='disabled',
                          command=partial(SpellUsedButton, (RowCounter + 1), CurrentSave))
            button.grid(column=1, row=RowCounter + 2, pady=5, padx=(4, 20))
        RowCounter += 1

    LongRest = Button(SpellSlots, text="Long Rest - Reset Slots",
                      command=partial(ResetSlots, CurrentSave), font=(BaseFont, 14))
    LongRest.grid(columnspan=2, row=11, pady=10)
    SpellSlots.mainloop()


def OpenSaveLocation():
    subprocess.Popen(f'explorer "{CWD}\\Saves\\"')


def CreateTemplateSave():
    print('Creating Template Save.')
    TemplateLoc = f'{CWD}\\Save Template.ini\\'
    SaveLoc = f'{CWD}\\Saves'
    try:
        shutil.copyfile(TemplateLoc, SaveLoc)
    except FileNotFoundError and PermissionError:
        print('No Template found.')


def CreateSaveList(var):
    for File in os.listdir(f'{CWD}/Saves'):
        if File.endswith('.ini'):
            print(File)
            if File == 'Save Template.ini':
                pass
            else:
                var.append(File)
    if len(var) == 0:
        var = ['No Saves Found']
        OpenSaveLocation()


SaveList = []
CreateSaveList(SaveList)

Prompt = Tk()
Prompt.title("Spell Slot Counter")
Prompt.iconbitmap('Fireball Icon.ico')

# Todo Update spacing to increase size of combobox.
PromptTitle = Label(text="Spell Slot Counter\nSave Selector",
                    font=(BoldBaseFont, 15)).grid(columnspan=2, pady=(10, 5), padx=90)

SaveSelector = ttk.Combobox(Prompt, values=SaveList)
SaveSelector.grid(column=0, row=1, pady=10, padx=10)
SaveSelector.current(0)


SaveConButton = Button(Prompt, text='Confirm Save', command=partial(create_window, SaveSelector))
SaveConButton.grid(column=1, row=1, pady=10, padx=10)


# Todo Add function to open save file location.
OpenSaveFolder = Button(Prompt, text='Open Save Folder', command=OpenSaveLocation)
OpenSaveFolder.grid(columnspan=2, row=2, pady=10, padx=10)

Prompt.mainloop()

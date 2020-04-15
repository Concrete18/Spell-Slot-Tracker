from tkinter import Tk, Button, Label, Frame, messagebox, OptionMenu, StringVar
from tkinter import ttk
from functools import partial
import configparser
import os


# Defaults for Background and fonts
Background = 'LightSteelBlue1'
BoldBaseFont = "Arial Bold"
BaseFont = "Arial"
FontColor = "Black"

# Start of Tkinter interface
SpellSlots = Tk()
SpellSlots.title("Spell Slot Counter")
SpellSlots.geometry("464x638")
SpellSlots.iconbitmap('Fireball Icon.ico')
SpellSlots.configure(bg=Background)
SpellSlots.resizable()

TitleFrame = Frame(SpellSlots, bg=Background)
TitleFrame.grid(columnspan=2, pady=(5, 5))

SpellTracker = configparser.ConfigParser()

FirstRun = 1
SaveList = []
SetSave = None


# ini.get Functions
def GetCharacterName():
    return SpellTracker.get('Main', 'CharacterName')


def SpellsKnown(Lvl):
    return int(SpellTracker.get(f'Level {str(Lvl)} Spells', 'Spells Known'))


def SpellsLeft(Lvl):
    return int(SpellTracker.get(f'Level {str(Lvl)} Spells', 'Spells Left'))


def SpellsPerDay(Lvl):
    return int(SpellTracker.get(f'Level {str(Lvl)} Spells', 'Spells Per Day'))


class SaveSlot:
    def __init__(self, CharName, FileName, FileLoc):
        self.CharName = CharName
        self.FileName = FileName
        self.FileLoc = FileLoc

    def UpdateInterface(self, Save):
        with open('example.cfg', 'wb') as configfile:
            SpellTracker.read(f'{os.getcwd()}/{File}')
            ScriptTitle.config(text=f"Spell Slot Counter\nfor {str(GetCharacterName())}")


for File in os.listdir(f'{os.getcwd()}/Saves'):
    if File.endswith('.ini'):
        with open('example.cfg', 'wb') as configfile:
            SpellTracker.read(f'{os.getcwd()}/{File}')
            CharName = GetCharacterName()
            FileName = File
            FileLoc = f'{os.getcwd()}/Saves/{File}'
            print(CharName)
            print(FileName)
            print(FileLoc)


# SpellTracker.read(f'{os.getcwd()}/Saves/Spells Slots - Template.ini')


# Use Spell Functions
def WriteToSpellTracker(SaveLocation):
    with open(SaveLocation, 'w') as configfile:
        SpellTracker.write(configfile)


# .ini Selection
def ConfirmSave(var):
    global SetSave
    SetSave = SaveSelector.get()
    SpellTracker.read(f'{os.getcwd()}/Saves/{ConfirmSave(ScriptTitle)}')
    var.config(text=f"Spell Slot Counter\nfor {str(GetCharacterName())}")
    print(SetSave)
    return SetSave


# Save Selector
SelectedSave = StringVar()

SaveSelector = ttk.Combobox(TitleFrame, values=SaveList)
SaveSelector.grid(column=0, row=1)

ScriptTitle = Label(TitleFrame, text=f"Spell Slot Counter\nChoose your Save", font=(BoldBaseFont, 20), fg=FontColor, bg=Background)
ScriptTitle.grid(columnspan=2, row=0)

for File in os.listdir(f'{os.getcwd()}/Saves'):
    if File.endswith('.ini'):
        print(f'{File} found and seen as save file.')
        SaveList.append(File)
print(SaveList)

SaveConButton = Button(TitleFrame, text='Confirm Save', command=partial(ConfirmSave, ScriptTitle))
SaveConButton.grid(column=1, row=1)

# Spell Level Info and Buttons
SpellInfoList = []
SpellButtonList = []
for x in range(1, 10):
    SpellInfoList.append(Label(SpellSlots))
    SpellButtonList.append(Button(SpellSlots))


def SpellUsedButton(SlotNumber):
    if int(SpellsLeft(SlotNumber)) > 1:
        SpellTracker.set(f'Level {str(SlotNumber)} Spells', 'Spells Left', str(SpellsLeft(SlotNumber)-1))
        SpellInfoList[SlotNumber - 1].config(text=f"Level {str(SlotNumber)} - {str(SpellsLeft(SlotNumber))} "
                                                  f"Spells left of {str(SpellsPerDay(SlotNumber))}")
        WriteToSpellTracker(SetSave)
        print('1 Spell Used')
    else:
        SpellTracker.set(f'Level {str(SlotNumber)} Spells', 'Spells Left', '0')
        WriteToSpellTracker(SetSave)
        SpellInfoList[SlotNumber - 1].config(text=f'Level {str(SlotNumber)} - No Slots left       ')
        SpellButtonList[SlotNumber - 1].config(state='disabled')
        print('Spell Level Spent')


def ResetSlots():
    response = messagebox.askyesno(title='Long Rest - Reset Slots', message='Are you sure that you want to reset?')
    if response:
        for SpellLevel in range(1, 10):
            SpellTracker.set(f'Level {str(SpellLevel)} Spells', 'Spells Left', str(SpellsPerDay(SpellLevel)))
            WriteToSpellTracker(SetSave)
            if int(SpellsKnown(SpellLevel)) > 0:
                SpellInfoList[SpellLevel-1].config(text=f"Level {str(SpellLevel)} - {str(SpellsLeft(SpellLevel))} "
                                                        f"Spells left of {str(SpellsPerDay(SpellLevel))}")
                SpellButtonList[SpellLevel-1].config(state='normal')
                print(f'Level {str(SpellLevel)} Slot Reset')
            else:
                pass
    else:
        pass


RowCounter = 0
# Spell Level Tkinter Labels
for lbl in SpellInfoList:
    if SpellsKnown(RowCounter+1) > 0 and SpellsLeft(RowCounter+1) > 0:
        lbl.config(text=f"Level {str(RowCounter+1)} - {str(SpellsLeft(RowCounter+1))} "
                        f"Spells left of {str(SpellsPerDay(RowCounter+1))}", font=(BaseFont, 15), bg=Background)
        lbl.grid(column=0, row=RowCounter + 2, padx=(20, 10))
    elif int(SpellsKnown(RowCounter+1)) > 0 and int(SpellsLeft(RowCounter+1)) < 1:
        lbl.config(text=f'Level {str(RowCounter+1)} - No Slots left      ')

    else:
        lbl.config(text=f"Level {str(RowCounter+1)} - No Spells Known", font=(BaseFont, 15), bg=Background)
        lbl.grid(column=0, row=RowCounter + 2, padx=(20, 10))
    RowCounter += 1


RowCounter = 0
# Spell Level Tkinter Buttons for using Spells
for button in SpellButtonList:
    if int(SpellsKnown(RowCounter+1)) > 1 and int(SpellsLeft(RowCounter+1)) > 0:
        button.config(text=f"Use Level {str(RowCounter+1)} Spell", font=(BaseFont, 15),
                      command=partial(SpellUsedButton, (RowCounter + 1)))
        button.grid(column=1, row=RowCounter + 2, pady=5, padx=(4, 20))
    else:
        button.config(text=f"Use Level {str(RowCounter+1)} Spell",
                      font=(BaseFont, 15), state='disabled', command=partial(SpellUsedButton, (RowCounter + 1)))
        button.grid(column=1, row=RowCounter + 2, pady=5, padx=(4, 20))
    RowCounter += 1

LongRest = Button(SpellSlots, text="Long Rest - Reset Slots", command=ResetSlots, font=(BaseFont, 14))
LongRest.grid(columnspan=2, row=11, pady=10)

SpellSlots.mainloop()

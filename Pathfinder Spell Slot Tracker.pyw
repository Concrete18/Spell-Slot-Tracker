from tkinter import Tk, Button, Label, Frame
from functools import partial
from tkinter import ttk
import logging as lg
import configparser
import subprocess
import sys
import os


class Save:


    def __init__(self):
        self.save = ''


    def open_save_location(self):
        subprocess.Popen(f'explorer "{self.cwd}\\Saves\\"')


    def create_save_list(self, var):
        for File in os.listdir(f'{self.cwd}/Saves'):
            if File.endswith('.ini'):
                print(File)
                if File == 'Save Template.ini':
                    pass
                else:
                    var.append(File)
        if len(var) == 0:
            text = ['No Saves Found']
            print(text)
            self.open_save_location()
            return var
        if len(var) == 1:
            self.create_window()


    def save_select(self):
        SaveList = []
        self.create_save_list(SaveList)

        Prompt = Tk()
        Prompt.title("Spell Slot Counter")
        Prompt.iconbitmap('Fireball Icon.ico')

        # Todo Update spacing to increase size of combobox.
        text = "Spell Slot Counter\nSave Selector"
        PromptTitle = Label(text=text, font=(self.bold_base_font, 15))
        PromptTitle.grid(columnspan=2, pady=(10, 5), padx=90)

        SaveSelector = ttk.Combobox(Prompt, values=SaveList)
        SaveSelector.grid(column=0, row=1, pady=10, padx=10)
        SaveSelector.current(0)

        SaveConButton = Button(Prompt, text='Confirm Save', command=self.create_window)
        SaveConButton.grid(column=1, row=1, pady=10, padx=10)

        # Todo Add function to open save file location.
        OpenSaveFolder = Button(Prompt, text='Open Save Folder', command=self.open_save_location)
        OpenSaveFolder.grid(columnspan=2, row=2, pady=10, padx=10)

        Prompt.mainloop()


class Tracker:


    def __init__(self, save_name):
        self.cwd = os.getcwd()
        format = '%(asctime)-15s %(message)s'
        lg.basicConfig(filename='Spell_Tracker.log', level=lg.INFO, format=format, datefmt='%m/%d/%Y %I:%M:%S %p')
        self.spell_log = lg.getLogger()
        self.SpellTracker = configparser.ConfigParser()
        self.current_save = save_name
        # Defaults for Background and fonts
        self.background = 'LightSteelBlue1'
        self.bold_base_font = "Arial Bold"
        self.base_font = "Arial"
        self.font_color = "Black"


    # ini.get Functions
    def get_character_name(self):
        return self.SpellTracker.get('Main', 'charactername')


    def spells_known(self, level):
        return int(self.SpellTracker.get(f'Level {level} Spells', 'Spells Known'))


    def spells_left(self, level):
        return int(self.SpellTracker.get(f'Level {level} Spells', 'Spells Left'))


    def spells_per_day(self, level):
        return int(self.SpellTracker.get(f'Level {level} Spells', 'Spells Per Day'))


    # Use Spell Functions
    def write_to_spell_tracker(self, file):
        with open(file, 'w') as configfile:
            self.SpellTracker.write(configfile)


    def create_window(self):
        self.SpellTracker.read(f'Saves/{self.current_save}')

        # Start of Tkinter interface
        SpellSlots = Tk()
        SpellSlots.title("Spell Slot Counter")
        SpellSlots.geometry("464x605")
        SpellSlots.iconbitmap('Fireball Icon.ico')
        SpellSlots.configure(bg=self.background)

        TitleFrame = Frame(SpellSlots, bg=self.background)
        TitleFrame.grid(columnspan=2, pady=(5, 5))


        text = f"Spell Slot Counter\nfor {self.get_character_name()}"
        Title = Label(TitleFrame, text=text, font=(self.bold_base_font, 20), fg=self.font_color, bg=self.background)
        Title.grid(column=0, row=0)

        # Spell Level Info and Buttons
        SpellInfoList = []
        SpellButtonList = []
        for x in range(1, 10):
            SpellInfoList.append(Label(SpellSlots))
            SpellButtonList.append(Button(SpellSlots))

        def SpellUsedButton(self, SlotNumber, SetName):
            if self.spells_left(SlotNumber) > 1:
                self.SpellTracker.set('Level ' + str(SlotNumber) + ' Spells', 'Spells Left', str(self.spells_left(SlotNumber)-1))
                text = f"Level {SlotNumber} - {self.spells_left(SlotNumber)} Spells left of {self.spells_per_day(SlotNumber)}"
                SpellInfoList[SlotNumber - 1].config(text=text)
                self.write_to_spell_tracker(f'Saves/{SetName}')
            else:
                self.SpellTracker.set(f'Level {SlotNumber} Spells', 'Spells Left', '0')
                self.write_to_spell_tracker(f'Saves/{SetName}')
                SpellInfoList[SlotNumber - 1].config(text=f'Level {SlotNumber} - No Slots left      ')
                SpellButtonList[SlotNumber - 1].config(state='disabled')
            lg.info(f'Level {SlotNumber} spell used.')

        def ResetSlots(SetSave):
            lg.info(f'Spell slots reset for {SetSave}.')
            for SpellLevel in range(1, 10):
                if self.spells_known(SpellLevel) > 0:
                    lg.info(f'Previous Spells for Level {SpellLevel} - {self.spells_left(SpellLevel)}.')
                self.SpellTracker.set(f'Level {SpellLevel} Spells', 'Spells Left', str(self.spells_per_day(SpellLevel)))
                self.write_to_spell_tracker(f'Saves/{SetSave}')
                if self.spells_known(SpellLevel) > 0:
                    text = f"Level {SpellLevel} - {self.spells_left(SpellLevel)} Spells left of {self.spells_per_day(SpellLevel)}"
                    SpellInfoList[SpellLevel-1].config(text=text)
                    SpellButtonList[SpellLevel-1].config(state='normal')
                    print(f'Level {SpellLevel} Slot Reset')
                else:
                    pass

        RowCounter = 0
        # Spell Level Tkinter Labels
        for lbl in SpellInfoList:
            if self.spells_known(RowCounter+1) > 0 and self.spells_left(RowCounter+1) > 0:
                text = f"Level {RowCounter+1} - {self.spells_left(RowCounter+1)} Spells left of {self.spells_per_day(RowCounter+1)}"
                lbl.config(text=text, font=(self.base_font, 15), bg=self.background)
                lbl.grid(column=0, row=RowCounter + 2, padx=(20, 10))
            elif self.spells_known(RowCounter+1) > 0 and self.spells_left(RowCounter+1) < 1:
                lbl.config(text='Level ' + str(RowCounter+1) + ' - No Slots left      ')
            else:
                lbl.config(text="Level " + str(RowCounter+1) + " - No Spells Known", font=(self.base_font, 15), bg=self.background)
                lbl.grid(column=0, row=RowCounter+2, padx=(20, 10))
            RowCounter += 1

        RowCounter = 0
        # Spell Level Tkinter Buttons for using Spells
        for button in SpellButtonList:
            if self.spells_known(RowCounter+1) > 0 and self.spells_left(RowCounter+1) > 0:
                text = f"Use Level {str(RowCounter+1)} Spell"
                button.config(text=text, font=(self.base_font, 15),
                command=lambda: SpellUsedButton(RowCounter + 1, self.current_save))
                button.grid(column=1, row=RowCounter + 2, pady=5, padx=(4, 20))
            else:
                text = f"Use Level {str(RowCounter+1)} Spell"
                button.config(text=text, font=(self.base_font, 15), state='disabled',
                command=partial(SpellUsedButton, (RowCounter + 1), self.current_save))
                button.grid(column=1, row=RowCounter + 2, pady=5, padx=(4, 20))
            RowCounter += 1

        text = "Long Rest - Reset Slots"
        LongRest = Button(SpellSlots, text=text, command=partial(ResetSlots, self.current_save), font=(self.base_font, 14))
        LongRest.grid(columnspan=2, row=11, pady=10)
        SpellSlots.mainloop()
        sys.exit()


if __name__ == '__main__':
    selection = Save()
    # App = Tracker(selection.save)
    App = Tracker('Dain Olaren.json')
    App.create_window()

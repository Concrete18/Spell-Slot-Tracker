from tkinter import Tk, ttk, Button, Label, Frame
import logging as lg
import subprocess
import json
import os


class Startup:


    def __init__(self):
        self.cwd = os.getcwd()
        self.save = ''


    def open_save_location(self):
        subprocess.Popen(f'explorer "{self.cwd}\\Saves\\"')


    def create_save_list(self):
        save_list = []
        for file in os.scandir(f'{self.cwd}/Saves'):
            if file.name.endswith('.json'):
                if file != 'Save Template.json':
                    save_list.append(file)
        if len(save_list) == 0:
            print('No Saves Found')
            self.open_save_location()
        elif len(save_list) == 1:
            return save_list[0]
        else:
            return save_list


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
        # Logging setup
        format = '%(asctime)-15s %(message)s'
        lg.basicConfig(filename='Spell_Tracker.log', level=lg.INFO, format=format, datefmt='%m/%d/%Y %I:%M:%S %p')
        self.spell_log = lg.getLogger()
        # Save system
        self.current_save = save_name
        with open(self.current_save) as json_file:
            self.data = json.load(json_file)
        # Defaults for Background and fonts
        self.background = 'white'
        # self.background = 'LightSteelBlue1'
        self.bold_base_font = "Arial Bold"
        self.base_font = "Arial"
        self.font_color = "Black"


    # ini.get Functions
    def get_character_name(self):
        '''
        Returns Character Name.
        '''
        return self.data['settings']['character_name']

    def spells_known(self):
        '''
        Returns highest spell level known.
        '''
        return self.data['settings']['spell_level_range']

    def spells_left(self, level):
        '''
        Returns spells left for spell level entered as argument.

        Argument:

        level -- spell level
        '''
        return self.data['spells'][f'level_{level}']['spells_left']


    def spells_per_day(self, level):
        '''
        Returns spells per day for spell level entered as argument.

        Argument:

        level -- spell level
        '''
        return self.data['spells'][f'level_{level}']['spells_per_day']


    # Use Spell Functions
    def write_to_json(self):
        '''
        Writes updated json data into save file.
        '''
        json_object = json.dumps(self.data, indent = 4)  # Serializing json
        with open(self.current_save, "w") as outfile:  # Writing to sample.json
            outfile.write(json_object)


    def spell_button_used(self, spell_level):
        print(spell_level)
        spells_left = self.spells_left(spell_level)
        if spells_left > 1:
            self.data['spells'][f'level_{spell_level}']['spells_left'] = spells_left - 1
            text = f"Level {spell_level} - {self.spells_left(spell_level)} Spells left of {self.spells_per_day(spell_level)}"
            self.spell_info_list[spell_level-1].config(text=text)
            self.write_to_json()
        else:
            self.data['spells'][f'level_{spell_level}']['spells_left'] = 0
            self.spell_info_list[spell_level-1].config(text=f'Level {spell_level} - No Slots left      ')
            self.spell_button_list[spell_level-1].config(state='disabled')
            self.write_to_json()
        lg.info(f'Level {spell_level} spell used.')


    def reset_slots(self):
        lg.info(f'Spell slots reset for {self.current_save}.')
        for spell_level in range(1, self.spells_known()):
            spells_per_day = self.spells_per_day(spell_level)
            lg.info(f'Previous Spells for Level {spell_level} - {self.spells_left(spell_level)}.')
            self.data['spells'][f'level_{spell_level}']['spells_left'] = spells_per_day
            self.write_to_json()
            text = f"Level {spell_level} - {spells_per_day} Spells left of {spells_per_day}"
            self.spell_info_list[spell_level-1].config(text=text)
            self.spell_button_list[spell_level-1].config(state='normal')
            print(f'Level {spell_level} Slot Reset')


    def create_window(self):
        '''
        Start of Tkinter interface
        '''
        SpellSlots = Tk()
        SpellSlots.title("Spell Slot Counter")
        # SpellSlots.geometry("464x605")
        SpellSlots.iconbitmap('Fireball Icon.ico')
        SpellSlots.configure(bg=self.background)

        TitleFrame = Frame(SpellSlots, bg=self.background)
        TitleFrame.grid(columnspan=2, pady=(5, 5))

        text = f"Spell Slot Counter\nfor {self.get_character_name()}"
        Title = Label(TitleFrame, text=text, font=(self.bold_base_font, 20), fg=self.font_color, bg=self.background)
        Title.grid(column=0, row=0)

        # Spell Level Info and Buttons
        self.spell_info_list = []
        self.spell_button_list = []
        for _ in range(1, self.data['settings']['spell_level_range']):
            self.spell_info_list.append(Label(SpellSlots))
            self.spell_button_list.append(ttk.Button(SpellSlots))

        # Spell Level Tkinter Labels
        for num in range(1, self.spells_known()):
            spells_left = self.spells_left(num)
            if self.spells_left(num) > 0:
                text = f"Level {num} - {spells_left} spells left of {self.spells_per_day(num)}"
                self.spell_info_list[num-1].config(text=text,
                    font=(self.base_font, 15), bg=self.background)
            elif self.spells_left(num) < 1:
                self.spell_info_list[num-1].config(text=' Level ' + str(num) + ' - no spell slots left',
                    font=(self.base_font, 15), bg=self.background)
            self.spell_info_list[num-1].grid(column=0, row=num + 1, padx=(20, 10))

        # Spell Level Tkinter Buttons for using Spells
        for num in range(1, self.spells_known()):
            text = f"Use Level {num} Spell"
            if self.spells_left(num) > 0:
                self.spell_button_list[num-1].config(text=text,
                    command=lambda: self.spell_button_used(num))
                self.spell_button_list[num-1].grid(column=1, row=num+1, pady=5, padx=(4, 20))
            else:
                self.spell_button_list[num-1].config(text=text, state='disabled',
                    command=lambda: self.spell_button_used(num))
                self.spell_button_list[num-1].grid(column=1, row=num+1, pady=5, padx=(4, 20))

        LongRest = ttk.Button(SpellSlots, text="Long Rest - Reset Slots", command=self.reset_slots)
        LongRest.grid(columnspan=2, row=11, pady=10)
        SpellSlots.mainloop()

if __name__ == '__main__':
    selection = Startup()
    # App = Tracker(selection.save)
    App = Tracker('Saves/Dain Olaren.json')
    App.create_window()

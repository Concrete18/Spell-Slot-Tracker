from tkinter import Tk, ttk, Button, Label, LabelFrame
import logging as lg
import subprocess
import json
import os
from functools import partial

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
        PromptTitle = Label(text=text)
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
        self.character_name = self.data['settings']['character_name']


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


    def write_to_json(self):
        '''
        Writes updated json data into save file.
        '''
        json_object = json.dumps(self.data, indent = 4)  # Serializing json
        with open(self.current_save, "w") as outfile:  # Writing to sample.json
            outfile.write(json_object)


    def spell_button_used(self, spell_level):
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


    def spell_like_button_used(self, index, spell_like):
        uses_left = int(self.data['spell_like'][spell_like]['uses_left'])
        uses_per_day = int(self.data['spell_like'][spell_like]['per_day'])
        if uses_left > 1:
            self.data['spell_like'][spell_like]['uses_left'] = uses_left - 1
            text = f"{spell_like} - {uses_left-1} uses left of {uses_per_day}"
            self.spell_like_info_list[index].config(text=text)
            self.write_to_json()
        else:
            self.data['spell_like'][spell_like]['uses_left'] = 0
            text = f"{spell_like} - No uses left    "
            self.spell_like_info_list[index].config(text=text)
            self.spell_like_button_list[index].config(state='disabled')
            self.write_to_json()
        lg.info(f'{spell_like} used.')


    def reset_slots(self):
        '''
        Resers slots for all known spell levels to the current spells per day for each level.
        '''
        lg.info(f'Spell slots reset for {self.current_save}.')
        for spell_level in range(1, self.spells_known()+1):
            spells_per_day = self.spells_per_day(spell_level)
            lg.info(f'Previous Spells for Level {spell_level} - {self.spells_left(spell_level)}.')
            self.data['spells'][f'level_{spell_level}']['spells_left'] = spells_per_day
            text = f"Level {spell_level} - {spells_per_day} Spells left of {spells_per_day}"
            self.spell_info_list[spell_level-1].config(text=text)
            self.spell_button_list[spell_level-1].config(state='normal')
        index=0
        for spell_like in self.data['spell_like']:
            uses_per_day = self.data['spell_like'][spell_like]['per_day']
            self.data['spell_like'][spell_like]['uses_left'] = uses_per_day
            text = f"{spell_like} - {uses_per_day} uses left of {uses_per_day}"
            self.spell_like_info_list[index].config(text=text)
            self.spell_like_button_list[index].config(state='normal')
            index += 1
        self.write_to_json()
        lg.info('Long Rest Completed')


    def create_window(self):
        '''
        Creates Tkinter interface.
        '''
        SpellSlots = Tk()
        SpellSlots.title("Spell Slot Counter")
        window_width = 370
        window_height = 215
        width = int((SpellSlots.winfo_screenwidth()-window_width)/2)
        height = int((SpellSlots.winfo_screenheight()-window_height)/2)
        SpellSlots.geometry(f'+{width}+{height}')
        SpellSlots.iconbitmap('Fireball Icon.ico')
        SpellSlots.resizable(width=False, height=False)

        text = f"Spell Slot Counter\n{self.character_name}"
        Title = Label(SpellSlots, text=text, font=('Arial Bold', 18))
        Title.grid(column=0, row=0)

        SpellFrame = LabelFrame(SpellSlots, text='Spells', font=('Arial Bold', 14))
        SpellFrame.grid(column=0, row=1, padx=10, pady=(10, 5))

        # Spell Level Info and Buttons
        self.spell_info_list = []
        self.spell_button_list = []
        for _ in range(1, self.data['settings']['spell_level_range']+1):
            self.spell_info_list.append(Label(SpellFrame))
            self.spell_button_list.append(ttk.Button(SpellFrame))

        # Spell Level Tkinter Labels
        for num in range(1, self.spells_known()+1):
            spells_left = self.spells_left(num)
            if self.spells_left(num) > 0:
                text = f"Level {num} - {spells_left} spells left of {self.spells_per_day(num)}"
                self.spell_info_list[num-1].config(text=text, font=('Arial', 13))
            else:
                self.spell_info_list[num-1].config(text=' Level ' + str(num) + ' - no spell slots left')
            self.spell_info_list[num-1].grid(column=0, row=num+1, padx=(20, 10))

        # Spell Level Tkinter Buttons for using Spells
        for num in range(1, self.spells_known()+1):
            text = f"Use Level {num} Spell"
            button_width = 18
            if self.spells_left(num) > 0:
                self.spell_button_list[num-1].config(text=text, width=button_width,
                    command=partial(self.spell_button_used, num))
                self.spell_button_list[num-1].grid(column=1, row=num+1, pady=5, padx=(4, 20))
            else:
                self.spell_button_list[num-1].config(text=text, width=button_width, state='disabled',
                    command=partial(self.spell_button_used, num))
                self.spell_button_list[num-1].grid(column=1, row=num+1, pady=5, padx=(4, 20))

        SpellLikeFrame = LabelFrame(SpellSlots, text='Spell Like Abilities', font=('Arial Bold', 14))
        SpellLikeFrame.grid(column=0, row=2, padx=10, pady=10)

        # Spell Level Info and Buttons
        spell_likes = self.data['spell_like']
        self.spell_like_info_list = []
        self.spell_like_button_list = []
        for _ in spell_likes:
            self.spell_like_info_list.append(Label(SpellLikeFrame))
            self.spell_like_button_list.append(ttk.Button(SpellLikeFrame))

        # Spell-like Tkinter Labels
        index=0
        for spell_like in spell_likes:
            uses_left = int(self.data['spell_like'][spell_like]['uses_left'])
            uses_per_day = int(self.data['spell_like'][spell_like]['per_day'])
            if uses_left > 0:
                text = f"{spell_like} - {uses_left} uses left of {uses_per_day}"
                self.spell_like_info_list[index].config(text=text, font=('Arial', 13))
            else:
                self.spell_like_info_list[index].config(text=f'{spell_like} - no uses left', font=('Arial', 13))
            self.spell_like_info_list[index].grid(column=0, row=index, padx=(20, 10))
            index += 1

        # Spell-like Tkinter Buttons for using Spell like abilties
        index=0
        for spell_like in spell_likes:
            uses_left = int(self.data['spell_like'][spell_like]['uses_left'])
            uses_per_day = int(self.data['spell_like'][spell_like]['per_day'])
            text = f"Use {spell_like}"
            button_width = 18
            if uses_left > 0:
                self.spell_like_button_list[index].config(text=text, width=button_width,
                    command=partial(self.spell_like_button_used, index, spell_like))
            else:
                self.spell_like_button_list[index].config(text=text, width=button_width, state='disabled',
                    command=partial(self.spell_like_button_used, index, spell_like))
            self.spell_like_button_list[index].grid(column=1, row=index, pady=5, padx=(4, 20))
            index += 1

        LongRest = ttk.Button(SpellSlots, text="Long Rest - Reset Slots", width=24, command=self.reset_slots)
        LongRest.grid(columnspan=2, row=3, pady=10)

        SpellSlots.mainloop()


if __name__ == '__main__':
    Selection = Startup()
    # App = Tracker(selection.save)
    App = Tracker('Saves/Dain Olaren.json')
    App.create_window()

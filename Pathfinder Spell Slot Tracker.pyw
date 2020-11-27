from tkinter import Tk, ttk, Label, LabelFrame, Listbox, END
from functools import partial
import logging as lg
import subprocess
import json
import sys
import os

class Startup:


    def __init__(self):
        self.cwd = os.getcwd()
        self.profile = ''


    def open_profile_location(self):
        subprocess.Popen(f'explorer "{self.cwd}\\profiles\\"')


    def create_profile_list(self):
        '''
        Creates a list of the .json files in the profile folder.
        '''
        profile_list = []
        for file in os.scandir(f'{self.cwd}/Profiles'):
            if file.name.endswith('.json'):
                profile_list.append(file.name)
        if len(profile_list) == 0:
            print('No profiles found')
            self.open_profile_location()
        else:
            return profile_list


    def set_profile(self):
        '''
        Sets the profile based on the listbox selection.
        '''
        self.profile = self.profilelist.get(self.profilelist.curselection())
        App = Tracker(Selection.profile)
        self.Prompt.destroy()
        App.create_window()


    def new_profile(self):
        '''
        Creates a new profile.
        '''
        pass


    def profile_select(self):
        profileList = self.create_profile_list()
        print()
        if len(profileList) == 1:
            App = Tracker(profileList[0])
            App.create_window()
            return
        self.Prompt = Tk()
        self.Prompt.title("Spell Slot Counter")
        self.Prompt.iconbitmap('Fireball Icon.ico')
        window_width = 369
        window_height = 194
        width = int((self.Prompt.winfo_screenwidth()-window_width)/2)
        height = int((self.Prompt.winfo_screenheight()-window_height)/2)
        self.Prompt.geometry(f'+{width}+{height}')

        # Bindings for interface.
        self.Prompt.bind(f"<Escape>", sys.exit)

        # Todo Update spacing to increase size of combobox.
        text = "Profile Selector"
        PromptTitle = Label(text=text, font=('Arial Bold', 14))
        PromptTitle.grid(columnspan=2, row=0, pady=(10, 5), padx=50)

        self.profilelist = Listbox(self.Prompt, exportselection=False)
        self.profilelist.grid(rowspan=2, column=0, pady=(5,10), padx=(15, 0))

        for item in profileList:
            self.profilelist.insert(END, item)

        button_width = 15
        padx_spacing = 15

        Load_Profile = ttk.Button(self.Prompt, text='Load Profile', width=button_width, command=self.set_profile)
        Load_Profile.grid(column=1, row=1, padx=padx_spacing)

        New_Profile = ttk.Button(self.Prompt, text='New Profile', width=button_width, command=self.new_profile)
        New_Profile.grid(column=1, row=1, padx=padx_spacing)

        # Todo Add function to open profile location.
        Open_Folder = ttk.Button(self.Prompt, text='Open Folder', width=button_width, command=self.open_profile_location)
        Open_Folder.grid(column=1, row=2, padx=padx_spacing)

        self.Prompt.mainloop()


class Tracker:


    def __init__(self, profile_name):
        # Logging setup
        format = '%(asctime)-15s %(message)s'
        lg.basicConfig(filename='Spell_Tracker.log', level=lg.INFO, format=format, datefmt='%m/%d/%Y %I:%M:%S %p')
        self.spell_log = lg.getLogger()
        # Profile system
        self.current_profile = f'Profile/{profile_name}'
        with open(self.current_profile) as json_file:
            self.data = json.load(json_file)
        self.character_name = self.data['settings']['character_name']
        self.character_class = self.data['settings']['character_class']
        self.spells_known = self.data['settings']['spell_level_range']
        if self.spells_known > 9:
            self.spells_known = 9
        # defaul label text
        self.spells_left_info = 'spells left of'
        self.no_spells_left_info = '0 spells left of'
        self.spell_like_left_info = 'uses left of'
        self.no_spell_like_left_info = '0 uses left of'


    def write_to_json(self, profile):
        '''
        Writes updated json data into profile.
        '''
        json_object = json.dumps(self.data, indent = 4)  # Serializing json
        with open(profile, "w") as outfile:  # Writing to sample.json
            outfile.write(json_object)


    def spell_button_used(self, spell_level):
        spells_left = self.data['spells'][f'level_{spell_level}']['spells_left']
        spells_per_day = self.data['spells'][f'level_{spell_level}']['spells_per_day']
        if spells_left > 1:
            self.data['spells'][f'level_{spell_level}']['spells_left'] = spells_left - 1
            text = f"Level {spell_level} - {spells_left-1} {self.spells_left_info} {spells_per_day}"
            self.spell_info_list[spell_level-1].config(text=text)
            self.write_to_json(self.current_profile)
        else:
            self.data['spells'][f'level_{spell_level}']['spells_left'] = 0
            text = f'Level {spell_level} - {self.no_spells_left_info} {spells_per_day}'
            self.spell_info_list[spell_level-1].config(text=text)
            self.spell_button_list[spell_level-1].config(state='disabled')
            self.write_to_json(self.current_profile)
        lg.info(f'Level {spell_level} spell used.')


    def spell_like_button_used(self, index, spell_like):
        uses_left = int(self.data['spell_like'][spell_like]['uses_left'])
        uses_per_day = int(self.data['spell_like'][spell_like]['per_day'])
        if uses_left > 1:
            self.data['spell_like'][spell_like]['uses_left'] = uses_left - 1
            text = f"{spell_like} - {uses_left-1} {self.spell_like_left_info} {uses_per_day}"
            self.spell_like_info_list[index].config(text=text)
            self.write_to_json(self.current_profile)
        else:
            self.data['spell_like'][spell_like]['uses_left'] = 0
            text = f"{spell_like} - {self.no_spell_like_left_info} {uses_per_day}"
            self.spell_like_info_list[index].config(text=text)
            self.spell_like_button_list[index].config(state='disabled')
            self.write_to_json(self.current_profile)
        lg.info(f'{spell_like} used.')


    def reset_slots(self):
        '''
        Resers slots for all known spell levels to the current spells per day for each level.
        '''
        lg.info(f'Spell slots reset for {self.current_profile}.')
        # Spells
        for spell_level in range(1, self.spells_known+1):
            spells_left = self.data['spells'][f'level_{spell_level}']['spells_left']
            spells_per_day = self.data['spells'][f'level_{spell_level}']['spells_per_day']
            lg.info(f'Previous Spells for Level {spell_level} - {spells_left}.')
            self.data['spells'][f'level_{spell_level}']['spells_left'] = spells_per_day
            text = f"Level {spell_level} - {spells_per_day} {self.spells_left_info} {spells_per_day}"
            self.spell_info_list[spell_level-1].config(text=text)
            self.spell_button_list[spell_level-1].config(state='normal')
        index=0
        # Spell Like Abilities
        for spell_like in self.data['spell_like']:
            uses_per_day = self.data['spell_like'][spell_like]['per_day']
            self.data['spell_like'][spell_like]['uses_left'] = uses_per_day
            text = f"{spell_like} - {uses_per_day} {self.spell_like_left_info} {uses_per_day}"
            self.spell_like_info_list[index].config(text=text)
            self.spell_like_button_list[index].config(state='normal')
            index += 1
        self.write_to_json(self.current_profile)
        lg.info('Long Rest Completed')


    def create_window(self):
        '''
        Creates Tkinter interface.
        '''
        SpellSlots = Tk()
        SpellSlots.title("Spell Slot Counter")
        window_width = 370
        window_height = 500
        width = int((SpellSlots.winfo_screenwidth()-window_width)/2)
        height = int((SpellSlots.winfo_screenheight()-window_height)/2)
        SpellSlots.geometry(f'+{width}+{height}')
        SpellSlots.iconbitmap('Fireball Icon.ico')
        SpellSlots.resizable(width=False, height=False)

        # Bindings for interface.
        SpellSlots.bind(f"<Escape>", sys.exit)

        text = f'{self.character_name}\n{self.character_class}'
        Title = Label(SpellSlots, text=text, font=('Arial Bold', 18))
        Title.grid(column=0, row=0, pady=5)

        SpellFrame = LabelFrame(SpellSlots, text='Spells', font=('Arial Bold', 14))
        SpellFrame.grid(column=0, row=1, padx=40, pady=5)

        # Spell Level Info and Buttons
        self.spell_info_list = []
        self.spell_button_list = []
        for _ in range(1, self.data['settings']['spell_level_range']+1):
            self.spell_info_list.append(Label(SpellFrame))
            self.spell_button_list.append(ttk.Button(SpellFrame))

        # Spell Level Tkinter Labels
        for num in range(1, self.spells_known+1):
            self.data['spells'][f'level_{num}']['spells_per_day']
            spells_left = self.data['spells'][f'level_{num}']['spells_left']
            spells_per_day = self.data['spells'][f'level_{num}']['spells_per_day']
            if spells_left > 0:
                text = f"Level {num} - {spells_left} {self.spells_left_info} {spells_per_day}"
                self.spell_info_list[num-1].config(text=text, font=('Arial', 13))
            else:
                text = f'Level {num} - {self.no_spells_left_info} {spells_per_day}'
                self.spell_info_list[num-1].config(text=text, font=('Arial', 13))
            self.spell_info_list[num-1].grid(column=0, row=num+1, padx=(20, 10))

        # Spell Level Tkinter Buttons for using Spells
        for num in range(1, self.spells_known+1):
            spells_left = self.data['spells'][f'level_{num}']['spells_left']
            text = f"Use Level {num} Spell"
            button_width = 18
            if spells_left > 0:
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
                text = f"{spell_like} - {uses_left} {self.spell_like_left_info} {uses_per_day}"
                self.spell_like_info_list[index].config(text=text, font=('Arial', 13))
            else:
                text = f'{spell_like} - {self.no_spell_like_left_info} {uses_per_day}'
                self.spell_like_info_list[index].config(text=text, font=('Arial', 13))
            self.spell_like_info_list[index].grid(column=0, row=index, padx=(20, 10))
            index += 1

        # Spell-like Tkinter Buttons for using Spell like abilties
        index=0
        for spell_like in spell_likes:
            uses_left = int(self.data['spell_like'][spell_like]['uses_left'])
            uses_per_day = int(self.data['spell_like'][spell_like]['per_day'])
            text = f"Use Ability"
            button_width = 12
            if uses_left > 0:
                self.spell_like_button_list[index].config(text=text, width=button_width,
                    command=partial(self.spell_like_button_used, index, spell_like))
            else:
                self.spell_like_button_list[index].config(text=text, width=button_width, state='disabled',
                    command=partial(self.spell_like_button_used, index, spell_like))
            self.spell_like_button_list[index].grid(column=1, row=index, pady=5, padx=(4, 20))
            index += 1

        LongRest = ttk.Button(SpellSlots, text="Long Rest - Reset Slots", width=24, command=self.reset_slots)
        LongRest.grid(columnspan=2, row=3, pady=(5, 15))

        SpellSlots.mainloop()


if __name__ == '__main__':
    Selection = Startup()
    Selection.profile_select()

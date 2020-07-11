# Spell Slot Tracker
My Pathfinder Spell Slot Tracker for Spontaneous Casters.

![Image of Spell Counter](https://i.imgur.com/P8XSlzF.png)

## Why?
I created this to learn Tkinter and configparser.
I actually have a use for it with my pathfinder Roll20 games as well. It saves to the .ini after every update which should not be often.

# Features
* Full Spell Slot Tracking from all levels known.
* Save Selector that will auto choose the single save if no others are there except the Saves\Save Template.ini.

## Save Method
This saves per action to a .ini which stores info such as character name, spells per day, spells left for the day and spells known. All that info is used to properly display all information in an interactable way.

## How to use it?

Install Python (I have only used Version 3.8 and 2 or lower is not going to work)

Make sure all the files are in the same main folder otherwise it will not work. That includes the .ico, .ini and .py files.

Next fill out the .ini with your character information to its current state in order to make the interface set perfectly for you.
These are located in Saves folder. You can have multiple characters in that folder. A Save picker opens first that allows you to pick which you load.

```.ini
[Main]
charactername = Dain Olaren

[Level 1 Spells]
spells_per_day = 8
spells_left = 4
spells_known = 6
```

Once the .ini is filled out, proceed to click the Use Spell buttons for the spell level you just used and click the Rest - Reset when you want everything to reset to your configured Spells per day per spell level as if after a rest.

### Thanks to [RobinHorn](https://github.com/rellissc) for the help with some of the methods used.

# Spell Slot Tracker
My Pathfinder Spell Slot Tracker for Spontaneous Casters.

## Why?
I created this to learn Tkinter and configparser.
I actually have a use for it with my pathfinder Roll20 games as well. It saves to the .ini after every update which should not be often.

## Save Method
This saves per action to a .ini which stores info such as character name, spells per day, spells left for the day and spells known. All that info is used to properly display all information ineractable way.

## How to use it?
Once the .ini is filled out, proceed to click the Use Spell buttons for the spell level you just used and click the Rest - Reset when you want everything to reset to your configured Spells per day per spell level.

```
[Main]
charactername = Dain Olaren

[Level 1 Spells]
spells per day = 8
spells left = 4
spells known = 6
```

### Thanks to [RobinHorn](https://github.com/rellissc) for the help with some of the methods used.

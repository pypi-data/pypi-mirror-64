# `gh0st`

```
       _      ____      _
      | |    / __ \    | |
  __ _| |__ | | /  |___| |_
 / _` | '_ \| |//| / __| __|
| (_| | | | |  /_| \__ \ |_
 \__, |_| |_|\____/|___/\__|
 /\_/ |
 \___/
```

A top-down stealth and hacking game implemented in python curses  
Playable in 256-color terminal emulators to monochrome tty and everything in between

## Files

```bash
.
├── gh0st/
│   ├── __init__.py
│   ├── __main__.py
│   └── packages/
│       ├── aart/ ------------------------ # ascii art wrapper
│       │   ├── aart.py
│       │   ├── aart.txt
│       │   ├── cursed.py
│       │   └── __init__.py
│       ├── __init__.py
│       ├── keymap/ ---------------------- # keymap class for input
│       │   ├── __init__.py
│       │   └── keymap.py
│       └── menu/ ------------------------ # menu classes for curses
│           ├── __init__.py
│           ├── menu.py
│           ├── OLD/ --------------------- # may incorporate these as base classes
│           └── option.py
├── icons/ ------------------------------- # various icons for game
├── LICENSE
├── README.md
├── setup.py
└── tests/ ------------------------------- # tests of various future features 
```

## Download and Play

```bash
$ pip install gh0st
$ gh0st
```

## TODO

### Key
[**+**] feature to be added  
[**x**] change in code  
[**-**] bug to be removed  
[**?**] uncertain how to proceed  

### Tasks

[**+**] add badges to gitlab <3  
[**+**] upload to PyPI  
`├──`   write working demo  
`└──`   tag first release  
[**+**] SE logic needs to be fuzzy, contradictable, and maybe not all revealed, but able to reveal by prodding/getting skill/familiarity?  
`└──`   SE demo?  
[**+**] Need to keep better track of window size to prevent errors from making and using windows that are larger  
[**+**] match window size on create&resize  
[**+**] use old option&menu as base class?  
[**x**] keymap needs to accept any and all curses chars  
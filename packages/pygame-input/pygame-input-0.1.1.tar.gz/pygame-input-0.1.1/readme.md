pygame-input
========
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

`pygame-input` will simplify your input handling with pygame
by providing a simple way to assign callbacks to given key press
or joystick events.

Look how easy it is to use:

```python
import pygame
from pygame_input import Inputs, Button, JoyButton

inputs = Inputs()
inputs["fire"] = Button(pygame.K_SPACE, JoyButton(1))
inputs["fire"].on_press_repeated(player.fire, delay=0.1)
```

This will call your `player.fire()` function every 0.1 seconds while 
any button, whether it is the space bar or the button one on your
joystick is pressed.
    
Features
--------

- Joystick
- Boolean input values (ie. *is key pressed ?*) 
    and scalar input values (ie. *how much is the stick on the left ?*)
- Register callbacks on:
    - press,
    - release,
    - double-press 
    - or all the time
    
    
What `pygame-input` is not (yet ?):
 - handling key modifiers
 - handling mouse input
 - recognising mouse gestures
 - doing gamepad configuration 
    (ie. you need to know which id is the "A" button)
    
Though the first two will probably be implemented quite
soon, depending on when I need them.

Installation
------------

Install `pygame-input` by running::

    pip install pygame-input

Alternativelly you can just copy `pygame_input.py` into your
game folder as the whole code is just one file. Feel free to
modify it as much as you need.

Usage
-----

See the [examples](examples).


Contribute
----------

- Issue Tracker: gitlab.com/ddorn/pygame-input/issues
- Source Code: gitlab.com/ddorn/pygame-input

Support
-------

If you are having issues, please let me know.
You can open an issue or send me a mail, 
my email address is on my gitlab profile.

License
-------

The project is licensed under the MIT license.
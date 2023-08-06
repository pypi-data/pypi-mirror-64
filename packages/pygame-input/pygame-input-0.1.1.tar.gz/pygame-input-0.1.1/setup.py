# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pygame_input']
install_requires = \
['pygame>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'pygame-input',
    'version': '0.1.1',
    'description': 'pygame-input is a tool to simplify input handling with pygame',
    'long_description': 'pygame-input\n========\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n`pygame-input` will simplify your input handling with pygame\nby providing a simple way to assign callbacks to given key press\nor joystick events.\n\nLook how easy it is to use:\n\n```python\nimport pygame\nfrom pygame_input import Inputs, Button, JoyButton\n\ninputs = Inputs()\ninputs["fire"] = Button(pygame.K_SPACE, JoyButton(1))\ninputs["fire"].on_press_repeated(player.fire, delay=0.1)\n```\n\nThis will call your `player.fire()` function every 0.1 seconds while \nany button, whether it is the space bar or the button one on your\njoystick is pressed.\n    \nFeatures\n--------\n\n- Joystick\n- Boolean input values (ie. *is key pressed ?*) \n    and scalar input values (ie. *how much is the stick on the left ?*)\n- Register callbacks on:\n    - press,\n    - release,\n    - double-press \n    - or all the time\n    \n    \nWhat `pygame-input` is not (yet ?):\n - handling key modifiers\n - handling mouse input\n - recognising mouse gestures\n - doing gamepad configuration \n    (ie. you need to know which id is the "A" button)\n    \nThough the first two will probably be implemented quite\nsoon, depending on when I need them.\n\nInstallation\n------------\n\nInstall `pygame-input` by running::\n\n    pip install pygame-input\n\nAlternativelly you can just copy `pygame_input.py` into your\ngame folder as the whole code is just one file. Feel free to\nmodify it as much as you need.\n\nUsage\n-----\n\nSee the [examples](examples).\n\n\nContribute\n----------\n\n- Issue Tracker: gitlab.com/ddorn/pygame-input/issues\n- Source Code: gitlab.com/ddorn/pygame-input\n\nSupport\n-------\n\nIf you are having issues, please let me know.\nYou can open an issue or send me a mail, \nmy email address is on my gitlab profile.\n\nLicense\n-------\n\nThe project is licensed under the MIT license.',
    'author': 'Diego Dorn',
    'author_email': 'pygame-input@lama-corp.space',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/ddorn/pygame-input',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

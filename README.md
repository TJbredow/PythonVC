# PythonVC
Basic voice activated system to control raspberry Pi's

There are three configurable files to this program, the receipes CSV which can be configured with up to twelve different commands. You can assign multiple different keywords, but there can only be values one through twelve.

*wakewords.py* changes how the device initially responds to you.
*recipes.csv* is which keywords are assigned to which command.
*pinoutcommands.py* is how the commands interface with the pi's GPIO pins. It is set by default to pulse a HIGH signal for .5s in the following order:

- one: GPIO17
- two: GPIO27
- three: GPIO22
- four: GPIO10
- five: GPIO9
- six: GPIO11
- seven: GPIO5
- eight: GPIO13
- nine: GPIO19
- ten: GPIO26
- eleven: GPIO16
- twelve: GPIO20

*setup.sh* includes a script for all dependencies. This is an assumption that you are setting this up on a raspberry pi running Raspbian. It is recommended to run a desktop environment and put a desktop en

*runthis.desktop* is a file that you can put in /home/pi/autostart/ to start the program at startup. You can change the path to the file. By default it is /home/pi/Desktop/PythonVC 

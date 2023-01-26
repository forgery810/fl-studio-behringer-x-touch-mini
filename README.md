# fl-studio-behringer-x-touch-mini

A MIDI script to provide functionality for the Behringer X-Touch Mini with FL Studio. This script is currently in development and may have bugs. The layout may change over time.  
You can email forgery810@gmail.com with requests for functionality, although I may not be able to accomodate everything. Given how early this is in development, do not email with bug reports as I am likely aware of them.

# Instructions

This script currently uses the Standard mode with the stock layout. Install the script by unzipping the folder to Documents/Image-Line/Settings/Hardware.

Select behringer-xtouch-mini from the options under midi settings. Make sure both input and output MIDI are set to the same port.  
  
The Fader is set to control currently selected track, channel, or playlist track depending on what is currently focused. 

Pressing Knob 8 will set the controller to Transport mode for Start, Stop etc. 

Pressing Knob 7 enters step editor mode. The buttons will set/remove steps. Pressing knob 7 again will rotate between A (steps 1-6) and B (17-32). Knob 7 leds will all light when B is active. The button leds should reflect the current status of the pattern steps. 

Pressing Knob 6 will enter keyboard mode. Pressing top left or right unlit buttons will shift the octave lower and higher, respectively.


Knobs 1 and 2 will control volume and panning of the currently selected channel/track dependent on the currently focused window.

When in Transport Mode



Current Transport layout:

top row A:

left    up     right    copy    paste	 overdub  tap tempo    undo

bottom row A:

enter  down   prev-pat   next-pat   loop-rec   stop    play    rec



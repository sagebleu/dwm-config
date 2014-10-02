#!/bin/sh

compton --config ~/.config/compton.conf &
feh --bg-fill ~/images/nil.png 
xset -b
./bar/bar.py &
exec ~/dwm/dwm

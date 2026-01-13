import screen_brightness_control as sbc

# get the brightness
brightness = sbc.get_brightness()
# get the brightness for the primary monitor
primary = sbc.get_brightness(display=0)

# set the brightness to 100% for the primary monitor
sbc.set_brightness(0, display=0)
sbc.set_brightness(0, display=1)

sbc.set_brightness(100, display=0)
sbc.set_brightness(77, display=1)

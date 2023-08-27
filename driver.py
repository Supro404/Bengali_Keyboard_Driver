import keyboard
import codecs

shift = False
capsLock = False
ctrl = False
numLock = False

shiftMap = {}
unShiftMap = {}

def remap_keyboard(src):
    def handler(event):
        global ctrl,numLock,capsLock,shift
        if(ctrl or (numLock and event.scan_code in [71,72,73,75,76,77,79,80,81,82])):
            keyboard.send(event.scan_code)
        elif((event.scan_code not in [53]) and ((event.scan_code not in [72,80,75,77]) or (event.scan_code in [53,72,80,75,77] and event.is_keypad))):
            if (event.event_type == keyboard.KEY_DOWN):
                if(not capsLock):
                    if(shift and (src in shiftMap)):
                        keyboard.write(shiftMap[src])
                        shift = True
                    elif(src in unShiftMap):
                        keyboard.write(unShiftMap[src])
                    else:
                        keyboard.write(src)
                else:
                    if(shift and (src in unShiftMap)):
                        keyboard.write(unShiftMap[src])
                        shift = True
                    elif(src in shiftMap):
                        keyboard.write(shiftMap[src])
                    else:
                        keyboard.write(src)

            else:
                keyboard.release(src)
        else:
            keyboard.send(event.scan_code)
    keyboard.on_press_key(src, handler, suppress=True)

def capsLockHandler(e):
    global capsLock
    capsLock = not capsLock

def numLockHandler(e):
    global numLock
    numLock = not numLock


def shiftPressHandler(e):
    global shift
    shift = True


def shiftReleaseHandler(e):
    global shift
    shift = False


def ctrlPressHandler(e):
    global ctrl
    ctrl = True


def ctrlReleaseHandler(e):
    global ctrl
    ctrl = False


keyboard.on_press_key('shift', shiftPressHandler)
keyboard.on_release_key('shift', shiftReleaseHandler)
keyboard.on_press_key('ctrl', ctrlPressHandler)
keyboard.on_release_key('ctrl', ctrlReleaseHandler)
keyboard.on_press_key('caps lock', capsLockHandler)
keyboard.on_press_key('num lock', numLockHandler)

f = codecs.open("shift.csv", mode="r", encoding="utf-8")
for x in f:
    x = x.strip().split("\n")[0].split(",")
    remap_keyboard(x[0].lower())
    shiftMap[x[0].lower()] = x[1]

f = codecs.open("unshift.csv", mode="r", encoding="utf-8")
for x in f:
    x = x.strip().split("\n")[0].split(",")
    remap_keyboard(x[0].lower())
    unShiftMap[x[0].lower()] = x[1]

shiftMap[","] = '\u0998'
remap_keyboard(",")
keyboard.wait('esc')
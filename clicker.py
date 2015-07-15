import sys
import time
from Quartz.CoreGraphics import *

def mouseEvent(type, posx, posy):
    theEvent = CGEventCreateMouseEvent(None, type, (posx,posy), kCGMouseButtonLeft)
    CGEventPost(kCGHIDEventTap, theEvent)
def mousemove(posx, posy):
    mouseEvent(kCGEventMouseMoved, posx,posy);
def mouseclick(posx, posy):
    mouseEvent(kCGEventLeftMouseDown, posx,posy);
    mouseEvent(kCGEventLeftMouseUp, posx,posy);
def position():
    return CGEventGetLocation(CGEventCreate(None))

def listener():
    keyUpEventTap = CGEventTapCreate(kCGHIDEventTap, kCGHeadInsertEventTap,kCGEventTapOptionListenOnly, CGEventMaskBit(kCGEventKeyUp), None, None)
    keyUpRunLoopSourceRef = CFMachPortCreateRunLoopSource(None, keyUpEventTap, 0)
    CFRelease(keyUpEventTap)

    CFRunLoopAddSource(CFRunLoopGetCurrent(), keyUpRunLoopSourceRef, kCFRunLoopDefaultMode)
    CFRelease(keyUpRunLoopSourceRef)


pos = position()
for x in range(15):
    time.sleep(.5)
    print pos
    mouseclick(*pos)


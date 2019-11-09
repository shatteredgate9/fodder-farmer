import mouse
import win32gui
from window import getWindowSizes
import cv2 as cv
import numpy as np
import pyautogui
import sys

windows = getWindowSizes()
nox = None

for win in windows:
    if win32gui.GetWindowText(win) == 'NoxPlayer':
        nox = win 

dimensions = win32gui.GetWindowRect(nox)
width = dimensions[2] - dimensions[0]
height = dimensions[3] - dimensions[1]
left = dimensions[0]
top = dimensions[1]
print(dimensions)

if height != 524 and width != 924:
    print(width, height)
    print('Error: Set NoxPlayer dimensions to (width: 920, height: 520)')
    sys.exit()

#cv.namedWindow('noxPlayer')

#m = mouse.Mouse()
#m.initMouseTracking('noxPlayer')

confirm = cv.imread('confirm.png', 0)
print(confirm)
screen = pyautogui.screenshot(region=(left, top, width, height))
screen = cv.cvtColor(np.array(screen), cv.COLOR_RGB2GRAY)

coord = pyautogui.locateOnScreen('confirm.png', region=(left, top, width, height))

print(coord)
found = pyautogui.screenshot(region=(coord.left, coord.top, coord.width, coord.height))

cv.imshow('found', np.array(found))

space = (coord.width * coord.height) / 2;
right_half_x_range = (coord.left + (coord.width / 2), coord.left + coord.width)
right_half_y_range = (coord.top, coord.top + coord.height)
print(right_half_x_range)
print(right_half_y_range)
print(right_half_x_range[0])
half = pyautogui.screenshot(region=(right_half_x_range[0], right_half_y_range[0], right_half_x_range[1] - right_half_x_range[0], right_half_y_range[1] - right_half_y_range[0]))

cv.imshow('half', np.array(half))
if cv.waitKey() == 27:
    cv.destroyAllWindows()
#while True:
#    image = pyautogui.screenshot(region=(left, top, width, height))
#    image = cv.cvtColor(np.array(image), cv.COLOR_RGB2BGR)
#    cv.imshow('noxPlayer', image)
#    
#    if cv.waitKey(1) == 27:
#        cv.destroyAllWindows()
#        break
#    
    



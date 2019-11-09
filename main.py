import sys
import math
import cv2 as cv
import time
import random
import pyautogui
import numpy as np
import win32gui
from utils.window import isRealWindow
import sms


def waitKey(key=27):
    if cv.waitKey() == key:
        cv.destroyAllWindows()


class Finder:
    def __init__(self, context):
        self.context = context

    def find(self, img, confidence=0.9):
        #screen = pyautogui.screenshot(region=self.context)

        #screen = cv.cvtColor(np.array(screen), cv.COLOR_BGR2GRAY)
        #screen_array = np.array(screen.convert('RGB'))
        #screen_cv = screen_array[:, :, ::-1].copy()
        #cv.imshow('hay', screen_cv)

        #needleImg = cv.imread(img, cv.IMREAD_COLOR)
        #needleImg = cv.cvtColor(np.array(needleImg), cv.COLOR_RGB2BGR)
        #cv.imshow('needle', needleImg)

        # waitKey()
        try:
            coords = pyautogui.locateOnScreen(
                img, region=self.context, confidence=0.9)
        except:
            raise

        return coords

    def show(self, coords):
        img = pyautogui.screenshot(region=coords)
        img = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
        cv.imshow('show', img)
        if cv.waitKey() == 27:
            cv.destroyAllWindows()


class Mouse:
    def __init__(self, context):
        self.context = context

    def click(self, x, y, clicks=1):
        print('Num of clicks', clicks)
        if clicks > 1:
            interval = random.uniform(0.50, 1)
            print(interval)
            pyautogui.click(x, y, clicks=clicks, interval=interval)
        else:
            pyautogui.click(x, y)

    def randomClick(self, coords, clicks=1):
        left, top, width, height = coords

        x_range = (left, left + width)
        y_range = (top, top + height)

        x_half_len = int(width / 2)

        pers = np.arange(x_range[0], x_range[1], 1)
        prob = [1.0] * (len(pers) - x_half_len) + [5.0] * x_half_len
        prob /= np.sum(prob)

        x = np.random.choice(pers, p=prob)

        y = random.uniform(y_range[0], y_range[1])

        # if clicks == 1:
        #clicks = random.randint(1, 2)

        self.click(x, y, clicks)

    def clickCenter(self):
        left, top, width, height = self.context

        x = random.uniform(left, left + width - 40)
        y = random.uniform(top + 40, top + height - 2)

        pyautogui.click(x, y)


def cb(hWnd, windows):
    if not isRealWindow(hWnd):
        return
    name = win32gui.GetWindowText(hWnd)
    rect = win32gui.GetWindowRect(hWnd)
    if name == 'LDPlayer':
        windows.append(hWnd)


windows = []
win32gui.EnumWindows(cb, windows)
ld = windows[0]

dimensions = win32gui.GetWindowRect(ld)
width = dimensions[2] - dimensions[0]
height = dimensions[3] - dimensions[1]
left = dimensions[0]
top = dimensions[1]

context = (left, top, width, height)
print('context', context)
mouse = Mouse(context)
finder = Finder(context)


def picture(region):
    pic = pyautogui.screenshot(region=region)
    pic = cv.cvtColor(np.array(pic), cv.COLOR_RGB2BGR)
    cv.imshow('pic', pic)

    waitKey()


def clickStart():
    time.sleep(random.uniform(3.5, 5))
    fixed_region = (context[0] + 700, context[1] + 510, 238, 40)
    mouse.randomClick(fixed_region, 2)

    time.sleep(random.uniform(1, 3))


def checkArrangeInventoryPrompt():
    failed = 0
    allowedAttempts = random.randrange(2, 3)

    while True:
        print('Checking for arrange invnetory prompt. . .')
        coords = finder.find('arrange.png')

        if coords:
            return True
        else:
            failed += 1

        if failed > allowedAttempts:
            return False

        time.sleep(random.uniform(1, 3))


def checkForStageFinish():
    print('Fighting still in progress.')
    while True:
        cleared_coords = finder.find('stage_cleared.png')

        if cleared_coords:
            print('Stage cleared.')
            return True

        failed_coords = finder.find('stage_failed.png')

        if failed_coords:
            print('Stage failed.')
            return False

        time.sleep(random.uniform(2, 6))


def clickConfirm():
    while True:
        coords = finder.find('confirm_green.png')

        if coords:
            x, y = pyautogui.center(coords)
            mouse.randomClick(coords)
            break
        else:
            print('Locating confirm button. . .')

        time.sleep(random.uniform(1, 3))


def clickTryAgain():
    time.sleep(random.uniform(3.5, 5))

    fixed_region = (context[0] + 740, context[1] + 510, 200, 45)
    mouse.randomClick(fixed_region, 1)

    time.sleep(random.uniform(1, 3))


def isEnergyNotEnough():
    failed = 0
    allowedAttempts = random.randrange(2, 4)

    while True:
        print('Checking if not enough energy . . .')
        coords = finder.find('no_energy.png')

        if coords:
            return True
        else:
            failed += 1

        if failed > allowedAttempts:
            return False

        time.sleep(random.uniform(1, 2))


def buyEnergy():
    print('Buying energy')
    while True:
        coords = finder.find('buy.png')

        if coords:
            mouse.randomClick(coords)
            break
        else:
            print('Locating buy again button . . .')

        time.sleep(random.uniform(1, 2))


def showShot(coords):
    shot = pyautogui.screenshot(region=coords)
    shot = cv.cvtColor(np.array(shot), cv.COLOR_RGB2BGR)
    cv.imshow('debugger', shot)
    if cv.waitKey() == 27:
        sys.exit()


mode = sys.argv[1]
print(mode, 'mode')


def Epic7Script():
    if mode == 'adv':
        print('Adventure mode. . . clicking again.')
        clickStart()
    clickStart()

    if checkArrangeInventoryPrompt():
        print('Inventory full, terminating. . .')
        sys.exit()

    if isEnergyNotEnough():
        print('Buying energy. . .')
        buyEnergy()
        print('Clicking start again. . .')
        clickStart()

    cleared = checkForStageFinish()

    mouse.clickCenter()

    if cleared:
        clickConfirm()

    clickTryAgain()


global_loop = 0
looped = 0
loop_range = (40, 55)
#looped_limit = random.randrange(loop_range[0], loop_range[1])
looped_limit = 10000

break_range = (3600, 5500)
break_time = random.uniform(break_range[0], break_range[1])

print('First break will last ', break_time / 60, ' minutes long.')
print('And will occur after ', looped_limit, ' loops.')


def getTime():
    return math.floor(time.time())


phone_number = ""
with open('.env', 'r') as env:
    lines = env.readlines()
    phone_number = lines[0].strip()

service = sms.init()


def notifyUser():
    msg = sms.CreateMessage('Epic7Bot', phone_number,
                            'Script Stalled', time.asctime())
    sms.SendMessage(service, 'me', msg)


while True:
    t = Timer(210, notifyUser)
    t.start()

    if looped > looped_limit:
        print('Reached loop limit of: ', looped_limit)
        global_loop += looped
        looped = 0
        looped_limit = random.uniform(loop_range[0], loop_range[1])
        print('New Loop limit: ', looped_limit)

        print('Taking a break for: ', break_time / 60, ' minutes long')
        time.sleep(break_time)
        break_time = random.uniform(break_range[0], break_range[1])
        print('Next break will be ', break_time / 60, ' minutes long.')

    Epic7Script()

    looped += 1
    t.cancel()

'''
    - All mouse commands must click on to a random portion of target.
    - All routines must be executed within a random timeframe from each other.

    1. Hit Start
        - If Insufficient Inventory
        - If Insufficient Energy
            - Add more crystals
            - If not enough crystals, go to 5.
        - Go to 5.
    2. Fight Started:
        - Check every 2:30 - 3:00 minutes for Stage Clear or Stage Failed
        - If Stage Cleared go to 3. 
        - Else go to 
    3. Stage Cleared:
        - Click Screen in random area. Mostly right half side of screen.
        - Hit Confirm
        - Hit Try Again
            - Check if not enough energy, add more from crystals.
        - Go To 1.
    4. Stage Failed:
        - Hit Try again
        - Go to 1.
    5. Stop Script.

    
    Confirm
'''

# Possible Obstacles
# 1. Stage Failed
# 2. Stage Cleared
# 3. Extra Quest Popup
# 4. Sent back to Lobby
# 5. Inventory full
# 6. Hero Inventory Full
# 7. Not enough Energy
# 8. dispatch missions - auto confirm
# 9. friend - auto cancej
# 10. your cp is below the recommended
# Modules


# Flow
# Find the nox player window, retrieve its dimensions
# Check that dimensions are 1280 x 720, if not, terminate script
# Go to adventure mode
# Find Click on 4-9
# Check team does not have any max levl units

# Script 1: Unit Checker
# CHeck if there is at least 1 white phantasma
# Check if there are no max level units
# Mark which unit is max level

# Script 2: Hero Inventory Full

# Script 3: Equipment Inventory Full

# Script 4: Handle random lobby screen

# Script 5: Battle Cleared

# Script 6: Battle Failed

# Generic Modules

# Window
# - Click
# -
#
#
#
#
#

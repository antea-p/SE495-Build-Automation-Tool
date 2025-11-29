import os
from dataclasses import astuple
from datetime import datetime

import pyautogui

from custom_types import HOTKEYS, REGION_BOX

RESOLUTION = pyautogui.size()


class Chitubox:

    def __init__(self, path: str = r"C:\Program Files\CBD\CHITUBOX_Basic\CHITUBOX_Basic.exe"):
        # TODO: start Chitubox and set focus
        # self.PATH = path
        # os.system('start "" "' + self.PATH + '"')  # https://stackoverflow.com/a/58589129
        pyautogui.PAUSE = 1.5

    @staticmethod
    def click(filename: str, confidence: float = 0.7, region_box=None):
        # https://medium.com/@khushalkathad2512/python-pyautogui-easy-to-automate-013e064c1451
        try:
            # https://github.com/asweigart/pyscreeze/issues/110#issuecomment-2333233194
            image_location = pyautogui.locateOnScreen(filename, confidence=confidence,
                                                      region=region_box if region_box else None)
            if image_location:
                x, y, width, height = image_location
                pyautogui.click(x + width / 2, y + height / 2)
        except pyautogui.PyAutoGUIException as e:
            if os.path.exists(filename):
                print(f"App found {filename}")
            print(f"Couldn't click {filename}. Exception details: {e}")  # TODO: logging
            pyautogui.screenshot(f'screenshot_{datetime.now().strftime("%d-%m-%Y")}.png')

    def open_file(self, filename: str):
        pyautogui.hotkey(*HOTKEYS['OPEN'])
        pyautogui.write(filename, interval=0.1)
        pyautogui.press(HOTKEYS['ENTER'])

    def slice(self):
        pyautogui.hotkey(*HOTKEYS['SLICE'])

    def save(self):
        self.click("Slice_v2.png", region_box=astuple(REGION_BOX['SLICE']))
        pyautogui.sleep(5)

        pyautogui.hotkey(*HOTKEYS['SAVE'])
        pyautogui.press('enter')
        pyautogui.hotkey(*HOTKEYS['CANCEL_PROMPT'])

    def back_to_model_prepare(self):
        self.click("BackToModelPrepare.png", region_box=astuple(REGION_BOX['BACK_TO_MODEL_PREPARE']))
        pyautogui.hotkey(*HOTKEYS['CANCEL_PROMPT'])
        pyautogui.hotkey(*HOTKEYS['NEW_PROJECT'])

        pyautogui.hotkey(*HOTKEYS['CANCEL_PROMPT'])
        pyautogui.hotkey(*HOTKEYS['NEW_PROJECT'])

        self.click("No.png", region_box=astuple(REGION_BOX['NO']))


if __name__ == '__main__':
    chitubox = Chitubox()
    pyautogui.sleep(10)
    # TODO: check if there's 'restore project files prompt', or if there's report bug prompt
    for file in os.scandir():
        if file.name.endswith(".stl"):
            chitubox.open_file(file.name)
            pyautogui.sleep(2)
            chitubox.slice()
            chitubox.save()
            chitubox.back_to_model_prepare()

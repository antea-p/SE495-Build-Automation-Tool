import os
from dataclasses import astuple
from datetime import datetime
from pathlib import Path

import pyautogui

from custom_types import HOTKEYS, REGION_BOX

RESOLUTION = pyautogui.size()


class Chitubox:

    def __init__(self, path: str = r"C:\Program Files\CBD\CHITUBOX_Basic\CHITUBOX_Basic.exe"):
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
        self.click("SliceAndSave.png", region_box=astuple(REGION_BOX['SLICE']))
        pyautogui.sleep(5)

        completed = False
        while not completed:
            # https://stackoverflow.com/a/52237162
            result = pyautogui.getWindowsWithTitle("Save slice file")
            if result:
                completed = True
                pyautogui.press('enter')
                print("Slicing finished")
                pyautogui.sleep(2)

                pyautogui.hotkey(*HOTKEYS['CANCEL_PROMPT'])
                self.back_to_model_prepare()
                pyautogui.hotkey(*HOTKEYS['NEW_PROJECT'])

    def back_to_model_prepare(self):
        self.click("BackToModelPrepare.png", region_box=astuple(REGION_BOX['BACK_TO_MODEL_PREPARE']))
        pyautogui.hotkey(*HOTKEYS['CANCEL_PROMPT'])
        pyautogui.hotkey(*HOTKEYS['NEW_PROJECT'])

        pyautogui.hotkey(*HOTKEYS['CANCEL_PROMPT'])
        pyautogui.hotkey(*HOTKEYS['NEW_PROJECT'])

        self.click("No.png", region_box=astuple(REGION_BOX['NO']))

    def perform_automation(self, file: Path):
        self.open_file(file.name)
        pyautogui.sleep(2)
        # size_mb = file.stat().st_size / 1000000
        # print(f"Size of {file.name}: {size_mb} MB")
        # if size_mb > 100:
        #     pyautogui.PAUSE = 15
        self.slice()
        self.save()
        pyautogui.PAUSE = 1.5

        # self.back_to_model_prepare()

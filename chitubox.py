import os
from dataclasses import astuple
from pathlib import Path

import pyautogui

from custom_types import HOTKEYS, REGION_BOX

RESOLUTION = pyautogui.size()


class Chitubox:

    def __init__(self, path: str = r"C:\Program Files\CHITUBOX\CHITUBOX.exe"):
        pyautogui.PAUSE = 1.5
        self._start(path)

    def _start(self, path):
        # https://stackoverflow.com/a/58589129
        os.system('start "" "' + path + '"')
        pyautogui.sleep(10)  # in case of slow computer
        self.click("X.png", region_box=astuple(REGION_BOX['X_CLOSE']))
        self.click("OpenFile.png", region_box=astuple(REGION_BOX['OPEN_FILE']))

    @staticmethod
    def click(filename: str, confidence: float = 0.7, region_box=None):
        # https://medium.com/@khushalkathad2512/python-pyautogui-easy-to-automate-013e064c1451
        full_path = Path('./ui_elements').joinpath(filename)
        try:
            # https://github.com/asweigart/pyscreeze/issues/110#issuecomment-2333233194
            image_location = pyautogui.locateOnScreen(str(full_path), confidence=confidence,
                                                      region=region_box if region_box else None)
            if image_location:
                x, y, width, height = image_location
                pyautogui.click(x + width / 2, y + height / 2)
        except pyautogui.PyAutoGUIException as e:
            if full_path.exists():
                print(f"App found {full_path}")
            print(f"Couldn't click {full_path}. Exception details: {e}")

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
            pyautogui.sleep(2)
            result = pyautogui.getWindowsWithTitle("Save slice file")
            if result:
                completed = True
                result[0].activate()  # makes sure Save dialog is focused
                pyautogui.sleep(2)
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
        self.slice()
        self.save()

    def show_message(self, message: str):
        pyautogui.alert(text=message, title="Info", button="OK")

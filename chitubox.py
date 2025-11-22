import os
import time
from datetime import datetime

import pyautogui

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
        # self.click("Open.png", region_box=(0, 0, 300, 400))
        pyautogui.hotkey('ctrl', 'o')
        pyautogui.write(filename, interval=0.1)
        pyautogui.press("enter")

    def slice(self):
        # self.click("Slice.png", region_box=(int(RESOLUTION.width * 0.8), int(RESOLUTION.height * 0.7), RESOLUTION.width,
        #                                     RESOLUTION.height))
        pyautogui.hotkey('s', 'l')

    def save(self):
        pyautogui.screenshot("slice.png", region=(int(RESOLUTION.width * 0.7), int(RESOLUTION.height * 0.8),
                                                  int(RESOLUTION.width * 0.4), int(RESOLUTION.height)))
        self.click("Slice_v2.png", region_box=(int(RESOLUTION.width * 0.7), int(RESOLUTION.height * 0.8),
                                               int(RESOLUTION.width * 0.4), int(RESOLUTION.height)))
        pyautogui.sleep(5)
        pyautogui.screenshot("save.png", region=(int(RESOLUTION.width * 0.5), int(RESOLUTION.height * 0.04),
                                                 int(RESOLUTION.width * 0.55), int(RESOLUTION.height * 0.05)))

        pyautogui.hotkey('ctrl', 'shift', 's', logScreenshot=True)
        pyautogui.sleep(1)
        pyautogui.press('enter')
        pyautogui.sleep(5)
        pyautogui.screenshot("save_success_preview.png",
                             region=(int(RESOLUTION.width * 0.3), int(RESOLUTION.height * 0.3),
                                     int(RESOLUTION.width * 0.4), int(RESOLUTION.height * 0.35)))
        pyautogui.hotkey('alt', 'f4', logScreenshot=True)
        pyautogui.sleep(2)
        pyautogui.screenshot("model_prepare.png", region=(int(RESOLUTION.width * 0.45), 0,
                                                          int(RESOLUTION.width * 0.5), int(RESOLUTION.height * 0.05)))
        self.click("BackToModelPrepare.png", region_box=(int(RESOLUTION.width * 0.45), 0,
                                                         int(RESOLUTION.width * 0.5), int(RESOLUTION.height * 0.05)))
        pyautogui.sleep(1)
        pyautogui.hotkey('alt', 'f4', logScreenshot=True)
        pyautogui.sleep(1)
        pyautogui.hotkey('ctrl', 'n', logScreenshot=True)

        pyautogui.screenshot("prompt.png")
        pyautogui.hotkey('alt', 'f4', logScreenshot=True)
        pyautogui.hotkey('ctrl', 'n', logScreenshot=True)

        self.click("No.png", region_box=(int(RESOLUTION.width * 0.5), int(RESOLUTION.height * 0.5),
                                         int(RESOLUTION.width * 0.6), int(RESOLUTION.height * 0.55)))


def close_bug_report(self):
    # TODO: refine
    try:
        timeout = time.time() + 5
        pyautogui.screenshot("bug_report.png", region=(int(RESOLUTION.width * 0.3), int(RESOLUTION.height * 0.1),
                                                       int(RESOLUTION.width * 0.4), int(RESOLUTION.height * 0.2)))
        while time.time() <= timeout:
            for pos in pyautogui.locateAllOnScreen("BugReport.png", grayscale=True,
                                                   region=(int(RESOLUTION.width * 0.3),
                                                           int(RESOLUTION.height * 0.1),
                                                           int(RESOLUTION.width * 0.4),
                                                           int(RESOLUTION.height * 0.2))):
                if pos:
                    pyautogui.hotkey('alt', 'f4', logScreenshot=True)
                    break
    except pyautogui.PyAutoGUIException:
        pass


if __name__ == '__main__':
    chitubox = Chitubox()
    pyautogui.sleep(10)
    # chitubox.close_bug_report()
    # TODO: check if there's 'restore project files prompt', or if there's report bug prompt
    for file in os.scandir():
        if file.name.endswith(".stl"):
            chitubox.open_file(file.name)
            pyautogui.sleep(2)
            chitubox.slice()
            chitubox.save()
            # for file in os.scandir():
            #     if file.name.endswith(".stl"):
            #         chitubox.open_file(file.name)
            #         pyautogui.sleep(2)
            #         chitubox.slice()
            #         chitubox.save()

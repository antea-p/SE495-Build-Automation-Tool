# SE495-Build-Automation-Tool

## Instructions

1. Prerequisite tools:
    - Python 3.11.7+ (make sure it's included in PATH environment variable)
    - CHITUBOX Basic
      3.1.0 - Sep 25, 2025 (https://www.chitubox.com/en/download/previous/chitubox-free)
    - Visual Studio Build Tools 2022 - install Desktop development with C++
2. Clone the repository to a Windows machine.
3. Install the dependencies with `pip install -r requirements.txt`
4. Open CHITUBOX and skip wizard. For printer,
   select AnyCubic, then Photon Mono X 6K. You can then accept default printer settings, or you can customise them.
5. Click the CHITUBOX logo (top left of the screen), then from dropdown menu select **Settings**.
6. Navigate to **File**. Change **_Default Save Directory_** to folder you want the script to save .pwmb files. Also
   change **_Default Open Directory_**, to folder where you have .stl files. Otherwise the script might not work as
   expected.
7. Next, go to **Function**, and disable **Apply auto-layout to imported models**.
8. Click **_Save_**, then **_Confirm_** to close the **Settings** modal.
9. Close and re-open CHITUBOX. Click X in the top right to skip login modal, if you wish to skip login. Make sure that
   you select **Ignore the current version upgrade** and then Cancel the update prompt.
10. Run `python main.py`. Don't use the computer while the script is running, so that the GUI automatisation doesn't get
    messed up. If you need to stop the automation, drag the mouse to any of the screen edges, e.g. top left (0, 0),
    which will activate pyautogui failsafe mechanism.

**Note**: The project wasn't tested on Unix.
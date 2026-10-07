# SE495-Build-Automation-Tool

3D build automation - it slices! It dices! Just (half) kidding. It downloads order part files, lays them out in CHITUBOX's print bed and slices them so they can be sent to printer without breaking a sweat. Note: this version is made to work with mock API to avoid leaking proprietary code. 

## Motivation
The project idea came up while I was looking for a real life problem to solve for bachelor's thesis. I didn't want to waste it by playing it safe and I was very eager to tackle something that is just outside of my comfort zone. The idea transpired during internship at 3DC Ltd when my mentor told me about how the employees spend 2 hours every work day just on daily tasks of preparing printers, slicing the order files, and sending them to printer. 

## Quick Start

### Usage
Note: company behind CHITUBOX sometimes permanently disables downloading of old version and basically forces you to download newer ones. This happened to me once and while all hotkeys worked fine, I had to replace 1 or 2 UI element screenshots. 

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


## Contributing
This project is not really intended for further contribution. You can clone the project and integrate it with API that provides access to builds and the respective files. Note that 


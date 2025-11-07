# SE495-Build-Automation-Tool

## Instructions

1. Prerequisite tools:
    - Python 3.11.7+ (make sure it's included in PATH environment variable)
    - CHITUBOX Basic
      2.3.1 (https://sac.chitubox.com/software/download.do?installerUrl=https%3A%2F%2Fdownload.chitubox.com%2F17839%2Fv2.3.1%2FCHITUBOX_Basic_WIN64_Installer_V2.3.1.exe&softwareId=17839&softwareVersionId=v2.3.1)
    - CMake
2. Clone the repository to a Windows machine.
3. Install the dependencies with `pip install -r requirements.txt`
4. Open CHITUBOX and skip wizard. For printer, select Photon Mono X 6k. You can then accept default printer settings, or
   customise them.
5. Run `python main.py`.

**Note**: The project wasn't tested on Linux and its compatibility most likely depends on CHITUBOX compatibility with
WINE.
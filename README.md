# Geforce-Hybrid-Capture
Statue: Alpha

### Description
So, while using Geforce Experience on Hybrid Radeon setup on Windows 8.1, there is an issue with Experience not loading, even when you disable the AMD hardware and reboot, while free alternatives are not able to record compitently, this is put down to that the build-in screen recording is using optimized process taking adavantage of key hardware features, this is what this program needs to to, is use the existing dlls etc, to trigger compitent screen recording.

### Structure
The plan for the file structure...
```
.\Geforce-Hybrid-Capture.bat
.\installer.py   (install libraries in `.venv`)
.\launcher.py    (run main program)
.\scripts\***.py (other scripts for program).
.\data\temporary.json
```

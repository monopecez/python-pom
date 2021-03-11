@echo off
set arg1=%1
adb shell screencap /sdcard/screencap.png
adb pull -p -a /sdcard/screencap.png
adb shell rm /sdcard/screencap.png

IF [%arg1%] == [] (GOTO GETDATE) ELSE (GOTO DONE)

:GETDATE
For /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
For /f "tokens=1-3 delims=/:" %%a in ("%TIME%") do (set mytime=%%a%%b%%c)
set arg1=%mydate%_%mytime%.png
GOTO DONE

:DONE
echo trying to delete %arg1%
del %arg1%
echo saving screenshot to %arg1%
ren screencap.png %arg1%
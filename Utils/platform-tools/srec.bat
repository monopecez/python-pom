@echo off
set arg1=%1
start /wait cmd /c adb shell screenrecord /sdcard/screen.mp4
adb pull -p -a /sdcard/screen.mp4
adb shell rm /sdcard/screen.mp4

IF [%arg1%] == [] (GOTO GETDATE) ELSE (GOTO DONE)

:GETDATE
For /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
For /f "tokens=1-3 delims=/:" %%a in ("%TIME%") do (set mytime=%%a%%b%%c)
set arg1=%mydate%_%mytime%.mp4
GOTO DONE

:DONE
echo %arg1%
ren screen.mp4 %arg1%
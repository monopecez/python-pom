@echo off
SET ARGUMENTS=%*

if "%ARGUMENTS%" == "" (
    GOTO EOF
)

SET "ARGUMENTS=%ARGUMENTS:""="%"

SETLOCAL ENABLEDELAYEDEXPANSION 
:: INSTALL ON ALL ATTACHED DEVICES ::
FOR /F "tokens=1,2 skip=1" %%A IN ('adb devices') DO (
    SET IS_DEV=%%B
	if "!IS_DEV!" == "device" (
	    SET SERIAL=%%A
	    echo "adb -s !SERIAL! %ARGUMENTS%"
	    call adb -s !SERIAL! %ARGUMENTS%
	)
)
ENDLOCAL

:EOF
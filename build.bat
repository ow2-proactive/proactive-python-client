@echo off
setlocal

echo Received argument: %1

set PYTHON=python

if "%1"=="CLEAN" goto CLEAN
if "%1"=="SETUP" goto SETUP
if "%1"=="SETUP_VENV" goto SETUP_VENV
if "%1"=="VIRTUAL_ENV" goto VIRTUAL_ENV
if "%1"=="BUILD" goto BUILD
if "%1"=="HELP" goto HELP
echo Invalid command. Use "build.bat HELP" for a list of available commands.
goto :EOF

:CLEAN
echo Cleaning up project...
call gradlew -q clean
echo Project clean complete.
goto :EOF

:SETUP
echo Setting up project...
call gradlew -q setup
echo Project setup complete.
goto :EOF

:SETUP_VENV
echo Setting up virtual environment...
%PYTHON% -m venv env
call env\Scripts\activate.bat && %PYTHON% -m pip install --upgrade pip setuptools twine
call env\Scripts\activate.bat && %PYTHON% -m pip install -r requirements.txt
call env\Scripts\activate.bat && %PYTHON% -m pip -V
echo Virtual environment is ready.
goto :EOF

:VIRTUAL_ENV
if exist "env\" (
    echo Virtual environment already exists.
    set /p answer="Do you want to delete it and create a new one? [y/N] "
    if /I "%answer%"=="y" (
        echo Deleting and recreating the virtual environment...
        rmdir /s /q env
        call :SETUP_VENV
    ) else (
        echo Using the existing virtual environment.
    )
) else (
    call :SETUP_VENV
)
goto :EOF

:BUILD
echo Building package...
rmdir /s /q dist
call env\Scripts\activate.bat && %PYTHON% build.py sdist --formats=zip
echo Package built.
goto :EOF

:HELP
echo Usage: build.bat [command]
echo Available commands: CLEAN SETUP SETUP_VENV VIRTUAL_ENV BUILD
goto :EOF

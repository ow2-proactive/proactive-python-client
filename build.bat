@echo off
setlocal

echo Received argument: %1

set PYTHON=python

if "%1"=="CLEAN" goto CLEAN
if "%1"=="SETUP" goto SETUP
if "%1"=="SETUP_VENV" goto SETUP_VENV
if "%1"=="VIRTUAL_ENV" goto VIRTUAL_ENV
if "%1"=="BUILD" goto BUILD
if "%1"=="CLEAN_BUILD" goto CLEAN_BUILD
if "%1"=="UNINSTALL" goto UNINSTALL
if "%1"=="INSTALL" goto INSTALL
if "%1"=="TEST" goto TEST
if "%1"=="PUBLISH_TEST" goto PUBLISH_TEST
if "%1"=="PUBLISH_TEST_USING_SECRETS" goto PUBLISH_TEST_USING_SECRETS
if "%1"=="PUBLISH_PROD" goto PUBLISH_PROD
if "%1"=="PUBLISH_PROD_USING_SECRETS" goto PUBLISH_PROD_USING_SECRETS
if "%1"=="PRINT_VERSION" goto PRINT_VERSION
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

:CLEAN_BUILD
call :SETUP
call :VIRTUAL_ENV
call :BUILD
goto :EOF

:UNINSTALL
echo Uninstalling package...
call env\Scripts\activate.bat && %PYTHON% -m pip uninstall -y proactive
echo Package uninstalled.
goto :EOF

:INSTALL
call :UNINSTALL
echo Installing package from dist...
for %%f in (dist\*.zip) do (
    call env\Scripts\activate.bat && %PYTHON% -m pip install "%%f"
)
echo Package installed.
goto :EOF

:TEST
echo Running tests...
call env\Scripts\activate.bat && set PROACTIVE_URL=<URL> && set PROACTIVE_USERNAME=<USERNAME> && set PROACTIVE_PASSWORD=<PASSWORD> && %PYTHON% -m pytest --metadata proactive_url %PROACTIVE_URL% --metadata username %PROACTIVE_USERNAME% --metadata password %PROACTIVE_PASSWORD% --junit-xml=build\reports\TEST-report.xml
echo Tests completed.
goto :EOF

:PUBLISH_TEST
echo Publishing to TestPyPI...
call env\Scripts\activate.bat && twine upload --repository-url https://test.pypi.org/legacy/ dist/* --config-file .pypirc
echo Publishing completed.
goto :EOF

:PUBLISH_TEST_USING_SECRETS
echo Publishing to TestPyPI using secrets...
call env\Scripts\activate.bat && twine upload --repository-url https://test.pypi.org/legacy/ dist/*
echo Publishing completed.
goto :EOF

:PUBLISH_PROD
echo Publishing to PyPI...
call env\Scripts\activate.bat && twine upload dist/* --config-file .pypirc
echo Publishing completed.
goto :EOF

:PUBLISH_PROD_USING_SECRETS
echo Publishing to PyPI using secrets...
call env\Scripts\activate.bat && twine upload dist/*
echo Publishing completed.
goto :EOF

:PRINT_VERSION
call env\Scripts\activate.bat && %PYTHON% -m pip show proactive
call env\Scripts\activate.bat && %PYTHON% -c "import proactive; print(proactive.__version__)"
goto :EOF

:HELP
echo Usage: build.bat [command]
echo Available commands: CLEAN SETUP SETUP_VENV VIRTUAL_ENV BUILD CLEAN_BUILD UNINSTALL INSTALL TEST PUBLISH_TEST PUBLISH_TEST_USING_SECRETS PUBLISH_PROD PUBLISH_PROD_USING_SECRETS PRINT_VERSION
goto :EOF

:: This batch file handles running the server in a python virtual environment
@echo off
echo Loading virtual environment
if NOT exist venv\pyvenv.cfg (
	echo Virtual environment not found
	echo Please run install.bat to configure the virtual environment
	echo Press enter to continue
	pause
	exit /b
)
echo Starting server
cmd /c venv\scripts\activate.bat ^
& python -m arma_api
pause

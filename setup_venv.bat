echo Creating virtual environment
if exist venv\pyenv.cfg (
	echo Virtual Environment Exists. Skipping...
) else (
	python -m venv ./venv/
	echo Virtual Environment Created
)
echo Installing dependencies
cmd /c venv\scripts\activate.bat ^
& python -m pip install --upgrade pip ^
& python -m pip install -r requirements.txt
echo Done

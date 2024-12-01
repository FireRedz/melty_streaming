echo off
clear

echo Checking for Overlay
If not Exist "www/dist/index.html" (
    echo Overlay hasn't been built yet, building!
    cd www
    npm i
    npm run build
    cd ..
) Else (
    echo Seems fine, continuing!
)

echo Checking for Python Enviroment!
If Not Exist ".venv/Scripts/activate.bat" (
    echo Not found, creating one!
    python -m venv .venv
    echo Done!

    Call ".venv/Scripts/activate.bat"

    echo Installing requirements!
    python -m pip install -r requirements.txt
) Else (
    echo Seems fine, continuing!
)


If Not Exist ".venv/Scripts/activate.bat" Exit /B 1

echo Activating venv!
Call ".venv/Scripts/activate.bat"

python main.py
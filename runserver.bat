@echo off
set VENV_PATH=.\myvenv
set PYTHON_EXECUTABLE=%VENV_PATH%\Scripts\python.exe

if exist %PYTHON_EXECUTABLE% (
    call %VENV_PATH%\Scripts\activate
    %PYTHON_EXECUTABLE% .\manage.py runserver
) else (
    echo Error: Virtual environment not found or Python executable missing.
)

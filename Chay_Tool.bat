@echo off
title Khoi dong Tool Tao Excel Fanpage Reels v2.0
cd /d "%~dp0"

:: Kiem tra va tu dong cai dat thu vien neu thieu
python -c "import openpyxl" 2>nul
if errorlevel 1 (
    echo Dang tu dong cai dat thu vien openpyxl...
    python -m pip install openpyxl
)

python main.py
if errorlevel 1 pause



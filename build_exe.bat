@echo off
title Build Tool Tao Excel Fanpage v2
cd /d "D:\Tool_Tao_Excel_Fanpage_v2"
echo Dang dong goi thanh file EXE...
pyinstaller --noconsole --onefile --clean --name "Tool_Tao_Excel_Fanpage_v2" main.py
echo.
echo ==============================================
echo DA DONG GOI HOAN TAT!
echo File EXE nam tai thu muc: D:\Tool_Tao_Excel_Fanpage_v2\dist
echo ==============================================
pause

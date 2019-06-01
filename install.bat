@echo off
where python.exe > tempFile
set /p pythonpath=<tempFile
set folderPath=%0
set handlerFilename=BFU_Install_ContextMenu.py
set requirementsFilename=requirements.txt
call set installHandlerPath=%%folderPath:install.bat=%handlerFilename%%%
call set installRequirementsPath=%%folderPath:install.bat=%requirementsFilename%%%
echo Installing requirements...
echo Requirements path: %installRequirementsPath%
echo.
pip install -r %installRequirementsPath%
echo.
echo Installation complete.
echo.
echo.
echo Installing Registry keys...
echo Python path: %pythonpath%
echo Install registry path: %installHandlerPath%
echo.
%pythonpath% %installHandlerPath%
echo.
echo Installation complete.
pause

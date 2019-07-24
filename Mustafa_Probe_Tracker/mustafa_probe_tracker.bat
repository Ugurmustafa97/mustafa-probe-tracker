@echo off

REM Then start a PlusServerLauncher for Slicer to use to start/stop PlusServers
start /MIN "" "C:\Users\Mustafa Ugur\PlusApp-2.8.0.20190617-Win64\bin\PlusServerLauncher.exe" 

REM Then start Slicer 
start /wait "" "C:\Program Files\Slicer 4.10.2\Slicer.exe" 

REM After we close out of Slicer, lets close the PlusServerLauncher
taskkill /F /IM PlusServerLauncher.exe
taskkill /F /IM PlusServer.exe

EXIT
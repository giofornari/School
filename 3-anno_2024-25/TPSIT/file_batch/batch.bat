@echo off
rem ***********************************************
rem  Giordano's Batch Script to simplify gcc
rem  Script Batch per compilare un programma in gcc
rem ***********************************************

echo Compilatore gcc
echo Version 1.0
echo.

rem Impostiamo la variabile SYSTEM: in Windows il valore sarà "windows"
set "SYSTEM=windows"

rem ================================
rem 1. NOME DEL FILE SORGENTE
rem ================================
:input_source
set "FILENAME="
set /p FILENAME="Source code name: "
if not "%FILENAME:~-2%"==".c" (
    echo File is not a .c source code!
    goto input_source
)
if not exist "%FILENAME%" (
    echo File not found!
    echo Available .c files:
    dir /b *.c
    goto input_source
)

rem ================================
rem 2. NOME OUTPUT
rem ================================
:input_output
set "OUTPUT="
set /p OUTPUT="Output name: "

rem ================================
rem 3. COMPILAZIONE
rem ================================
:input_method
set "METHOD="
set /p METHOD="Metodo di compilazione (1. Diretto, 2. Passo passo): " 
if not "%METHOD%"=="1" if not "%METHOD%"=="2" (
    echo Metodo non valido!
    goto input_method
)

rem ================================
rem 4. WARNING
rem ================================
:input_warnings
set "SHOW_WARNINGS_FLAG="
set /p SHOW_WARNINGS_FLAG="Show warnings (y/n): "
if not "%SHOW_WARNINGS_FLAG%"=="y" if not "%SHOW_WARNINGS_FLAG%"=="n" (
    echo Please answer y or n.
    goto input_warnings
)

rem ================================
rem 6. OTTIMIZZAZIONE
rem ================================
:input_optimization
set "OPTIMIZATION="
echo Scegli ottimizzazione:
echo 1. Base, 2. Media, 3. Avanzata, 4. Compressione, 5. Massima, 6. Nessuna
set /p OPTIMIZATION="(1-6)    > "
if not "%OPTIMIZATION%"=="1" if not "%OPTIMIZATION%"=="2" if not "%OPTIMIZATION%"=="3" if not "%OPTIMIZATION%"=="4" if not "%OPTIMIZATION%"=="5" if not "%OPTIMIZATION%"=="6" (
    echo Opzione non valida
    goto input_optimization
)

rem Define main compilation and execution
set "BASE_CMD=gcc %FILENAME%"

if "%METHOD%"=="1" (
    call :run "%OUTPUT%" ""
) else if "%METHOD%"=="2" (
    call :run "%OUTPUT%.i" "-E"
    if errorlevel 1 goto end
    call :run "%OUTPUT%.s" "-S"
    if errorlevel 1 goto end
    call :run "%OUTPUT%.o" "-c"
    if errorlevel 1 goto end
    call :run "%OUTPUT%" ""
    if errorlevel 1 goto end
)
goto end

:run
setlocal enabledelayedexpansion
set "CMD=%BASE_CMD%"
if not "%~2"=="" (
    set "CMD=!CMD! %~2"
)
set "CMD=!CMD! -o %~1"
if /i "%SHOW_WARNINGS_FLAG%"=="y" (
    set "CMD=!CMD! -Wall -Wextra"
)

if "%OPTIMIZATION%"=="1" (
    set "CMD=!CMD! -O1"
) else if "%OPTIMIZATION%"=="2" (
    set "CMD=!CMD! -O2"
) else if "%OPTIMIZATION%"=="3" (
    set "CMD=!CMD! -O3"
) else if "%OPTIMIZATION%"=="4" (
    set "CMD=!CMD! -Os"
) else if "%OPTIMIZATION%"=="5" (
    set "CMD=!CMD! -Ofast"
)

echo.
echo Esecuzione comando: !CMD!
echo.
!CMD!
if errorlevel 1 (
    echo Errore durante la compilazione.
    endlocal
    exit /b 1
)
endlocal
exit /b 0

:end
echo.
echo Compilazione completata.
pause
exit /b 0
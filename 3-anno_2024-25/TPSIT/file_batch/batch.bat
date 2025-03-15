@echo off
rem ***********************************************
rem  Giordano's Batch Script to simplify gcc
rem  Script Batch per compilare un programma in gcc
rem ***********************************************

echo Giordano's C Compiler
echo Version 1.0
echo.

rem Impostiamo la variabile SYSTEM: in Windows il valore sarà "windows"
set "SYSTEM=windows"

rem ================================
rem 1. CHIEDI IL NOME DEL FILE SORGENTE
rem ================================
:input_source
set "FILENAME="
set /p FILENAME=Source code name: 
call :endswith "%FILENAME%" ".c"
if errorlevel 1 (
    echo File is not .c source code!
    goto input_source
)
if not exist "%FILENAME%" (
    echo File not found!
    echo Available .c files:
    dir /b *.c
    goto input_source
)

rem ================================
rem 2. CHIEDI IL NOME DELL'OUTPUT
rem ================================
:input_output
set "OUTPUT="
set /p OUTPUT=Output name: 
rem Verifica che il nome contenga solo lettere, numeri, underscore o dash
echo %OUTPUT% | findstr /r "^[a-zA-Z0-9_-][a-zA-Z0-9_-]*$" >nul
if errorlevel 1 (
    echo Output name is not valid!
    goto input_output
)

rem ================================
rem 3. METODO DI COMPILAZIONE
rem ================================
:input_method
set "METHOD="
set /p METHOD=Compilation method (1. Direct, 2. Step by step) [choose 1 or 2]: 
if not "%METHOD%"=="1" if not "%METHOD%"=="2" (
    echo Method not found!
    goto input_method
)

rem ================================
rem 4. MOSTRARE I WARNING?
rem ================================
:input_warnings
set "SHOW_WARNINGS_FLAG="
set /p SHOW_WARNINGS_FLAG=Show warnings (y/n): 
if /i not "%SHOW_WARNINGS_FLAG%"=="y" if /i not "%SHOW_WARNINGS_FLAG%"=="n" (
    echo Please answer y or n.
    goto input_warnings
)

rem ================================
rem 5. COMPATIBILITA' ANSI (MinGW ANSI Studio)
rem ================================
:input_ansi
set "ANSI_FLAG="
set /p ANSI_FLAG=Use MinGW ANSI Studio compatibility (y/n): 
if /i not "%ANSI_FLAG%"=="y" if /i not "%ANSI_FLAG%"=="n" (
    echo Please answer y or n.
    goto input_ansi
)

rem ================================
rem 6. OTTIMIZZAZIONE
rem ================================
:input_optimization
set "OPTIMIZATION="
echo Optimization options:
echo   1. Basic
echo   2. Medium
echo   3. Advanced
echo   4. Compression
echo   5. Maximum optimization (use with caution)
echo   6. No optimization
set /p OPTIMIZATION=Choose option (1-6): 
if not "%OPTIMIZATION%"=="1" if not "%OPTIMIZATION%"=="2" if not "%OPTIMIZATION%"=="3" if not "%OPTIMIZATION%"=="4" if not "%OPTIMIZATION%"=="5" if not "%OPTIMIZATION%"=="6" (
    echo Option not valid!
    goto input_optimization
)

rem ================================
rem 7. COMPILAZIONE PER DEBUGGING
rem ================================
:input_debug
set "DEBUG_FLAG="
set /p DEBUG_FLAG=Compile for debugging (y/n): 
if /i not "%DEBUG_FLAG%"=="y" if /i not "%DEBUG_FLAG%"=="n" (
    echo Please answer y or n.
    goto input_debug
)

rem Imposta il comando di base
set "BASE_CMD=gcc %FILENAME%"

rem ------------------------------
rem Definizione della subroutine :run
rem Parametri:
rem    %1 = nome del file output
rem    %2 = eventuali flag aggiuntivi (es. -E, -S, -c)
rem ------------------------------
:run
setlocal enabledelayedexpansion
set "CMD=%BASE_CMD% -o %1 %2"
if /i "%SHOW_WARNINGS_FLAG%"=="y" (
    set "CMD=!CMD! -Wall -Wextra"
)
if /i "%ANSI_FLAG%"=="y" (
    if /i "%SYSTEM%"=="windows" (
        set "CMD=!CMD! -D_USE_MINGW_ANSI_STUDIO"
    )
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
if /i "%DEBUG_FLAG%"=="y" (
    set "CMD=!CMD! -g"
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
goto :eof

rem ------------------------------
rem Subroutine :endswith
rem Controlla se la stringa (%1) termina con il suffisso (%2)
rem Restituisce 0 se vero, 1 se falso
rem ------------------------------
:endswith
setlocal enabledelayedexpansion
set "str=%~1"
set "suf=%~2"
call :strlen str len_str
call :strlen suf len_suf
if %len_str% LSS %len_suf% (
    endlocal & exit /b 1
)
set /a start=len_str-len_suf
set "sub=!str:~%start%!"
if /i "!sub!"=="%suf%" (
    endlocal & exit /b 0
) else (
    endlocal & exit /b 1
)

rem ------------------------------
rem Subroutine :strlen
rem Calcola la lunghezza della stringa contenuta nella variabile %1
rem Il risultato viene memorizzato nella variabile il cui nome è passato in %2
rem ------------------------------
:strlen
setlocal enabledelayedexpansion
set "s=!%~1!"
set /a len=0
:strlen_loop
if defined s (
    set "s=!s:~1!"
    set /a len+=1
    goto strlen_loop
)
endlocal & set "%~2=%len%"
goto :eof

rem ================================
rem Esecuzione della compilazione
rem ================================
if "%METHOD%"=="1" (
    call :run "%OUTPUT%"
) else if "%METHOD%"=="2" (
    call :run "%OUTPUT%.i" "-E"
    call :run "%OUTPUT%.s" "-S"
    call :run "%OUTPUT%.o" "-c"
    call :run "%OUTPUT%"
)

rem Se non sei su Windows (SYSTEM diverso da windows), chiedi se compilare per Windows x86_64
if /i not "%SYSTEM%"=="windows" (
    set "WINDOWS_FLAG="
    set /p WINDOWS_FLAG=Do you want to compile for Windows x86_64? (y/n): 
    if /i "%WINDOWS_FLAG%"=="y" (
        set "BASE_CMD=x86_64-w64-mingw32-gcc %FILENAME%"
        call :run "%OUTPUT%.exe"
    )
)

pause
exit /b 0
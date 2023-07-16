@echo off
setlocal EnableExtensions DisableDelayedExpansion


set "base=%USERPROFILE%\.pronav"
set "projects=%base%\.projects"
set "top=%USERPROFILE%\Documents"
set /A depth=5

IF NOT EXISTS "%base%" MD "%base%"
IF NOT EXISTS "%projects%" ECHO "" > "%projects%"

if %1 == "-u" CALL :find-projects %depth%


:find-projects
    set /A counter=%depth%
    for /D %%f IN ("%top%\*") do (
		if "%%~nxA" == ".git" echo %%f > %projects%
		%counter% -= 1
		if %counter% == 0 GOTO END
    )

:END

cat %projects%

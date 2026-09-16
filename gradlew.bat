@echo off
setlocal
set "APP_HOME=%~dp0"
set "GRADLE_VERSION=8.7"
set "GRADLE_USER_HOME=%GRADLE_USER_HOME%"
if "%GRADLE_USER_HOME%"=="" set "GRADLE_USER_HOME=%USERPROFILE%\.gradle"
set "DIST=%GRADLE_USER_HOME%\wrapper\dists\gradle-%GRADLE_VERSION%-bin\manual"
set "ZIP=%DIST%\gradle-%GRADLE_VERSION%-bin.zip"
set "BIN=%DIST%\gradle-%GRADLE_VERSION%\bin\gradle.bat"
if exist "%BIN%" goto run
if not exist "%DIST%" mkdir "%DIST%"
if not exist "%ZIP%" (
  echo Gradle %GRADLE_VERSION% not found; downloading it...
  powershell -NoProfile -ExecutionPolicy Bypass -Command "Invoke-WebRequest -UseBasicParsing -Uri 'https://services.gradle.org/distributions/gradle-%GRADLE_VERSION%-bin.zip' -OutFile '%ZIP%'"
  if errorlevel 1 exit /b 1
)
powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -Force '%ZIP%' '%DIST%'"
if errorlevel 1 exit /b 1
:run
call "%BIN%" %*
endlocal

@echo off
echo Audio Normalizer
echo ================
echo.

echo Building Docker container...
docker-compose build

echo.
echo Processing audio files...
docker-compose up

echo.
echo Done! Check the output folder for results.
pause
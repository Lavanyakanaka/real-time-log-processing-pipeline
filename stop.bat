@echo off
REM stop.bat - Stop and cleanup the Real-time Log Processing Pipeline (Windows)

echo.
echo ==========================================
echo Stopping Real-time Log Processing Pipeline
echo ==========================================
echo.

REM Check if Docker Compose is installed
where docker-compose >nul 2>nul
if errorlevel 1 (
    echo Error: Docker Compose is not installed.
    exit /b 1
)

REM Check if docker-compose.yml exists
if not exist "docker-compose.yml" (
    echo Error: docker-compose.yml not found in current directory
    exit /b 1
)

echo Stopping all services gracefully...
docker-compose stop

echo All services stopped
echo.

set /p cleanup="Do you want to remove containers and volumes? (y/n) "
if /i "%cleanup%"=="y" (
    echo Removing containers and volumes...
    docker-compose down -v
    echo Cleanup complete
) else (
    echo Containers remain available. Run 'docker-compose down' to remove them completely.
)

echo.
echo Goodbye!
pause

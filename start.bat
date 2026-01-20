@echo off
REM start.bat - Start the Real-time Log Processing Pipeline (Windows)

echo.
echo ==========================================
echo Real-time Log Processing Pipeline
echo ==========================================
echo.

REM Check if Docker and Docker Compose are installed
where docker >nul 2>nul
if errorlevel 1 (
    echo Error: Docker is not installed. Please install Docker first.
    exit /b 1
)

where docker-compose >nul 2>nul
if errorlevel 1 (
    echo Error: Docker Compose is not installed. Please install Docker Compose first.
    exit /b 1
)

echo Docker and Docker Compose are installed
echo.

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    if exist ".env.example" (
        copy .env.example .env
        echo .env file created
    ) else (
        echo Warning: .env.example not found, using defaults
    )
) else (
    echo .env file exists
)

echo.
echo Starting services...
echo.

REM Build and start services
docker-compose up --build

echo.
echo All services started successfully!
echo.
echo Next steps:
echo   1. Wait for services to be healthy
echo   2. In another terminal, run: docker-compose logs -f
echo   3. To view processed logs: docker-compose exec consumer tail -f /data/processed_errors_warnings.jsonl
echo   4. To stop services: docker-compose down
echo.
pause

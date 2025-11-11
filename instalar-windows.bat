@echo off
title Instalador de dependencias LexnetReady (Windows)
color 0A

echo ===========================================================
echo        LexnetReady - Instalador de dependencias
echo ===========================================================
echo.
echo Este script instalará todos los programas y librerías necesarias
echo para que LexnetReady funcione correctamente en Windows.
echo ANTES DE CONTINUAR, DEBE TENER INSTALADO AUTOFIRMA Y SU CERTIFICADO
echo ACA EN MOZILLA FIREFOX.
echo.
echo Version: 2025.11
echo Desarrollado por: José Carlos Rueda Álvarez (Bandua Legal)
echo ===========================================================
echo.

:: ------------------------------------------------------------
:: Comprobación de privilegios
:: ------------------------------------------------------------
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [X] Debe ejecutar este instalador como Administrador.
    pause
    exit /b
)

:: ------------------------------------------------------------
:: Comprobación de Winget
:: ------------------------------------------------------------
where winget >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Winget no está disponible. 
    echo     Actualice Windows (requiere Windows 10/11) o instale la Microsoft Store App Installer.
    pause
    exit /b
)

:: ------------------------------------------------------------
:: Instalar dependencias principales mediante Winget
:: ------------------------------------------------------------
echo.
echo [1/8] Instalando LibreOffice...
winget install --id LibreOffice.LibreOffice -e --accept-source-agreements --accept-package-agreements -h
echo.

echo [2/8] Instalando Java (Temurin 17)...
winget install --id EclipseAdoptium.Temurin17.JRE -e --accept-source-agreements --accept-package-agreements -h
echo.

echo [3/8] Instalando Tesseract OCR...
winget install --id UB-Mannheim.TesseractOCR -e --accept-source-agreements --accept-package-agreements -h
echo.

echo [4/8] Instalando Ghostscript...
winget install --id ArtifexSoftware.Ghostscript -e --accept-source-agreements --accept-package-agreements -h
echo.

echo [5/8] Instalando Poppler...
winget install --id Poppler.Poppler -e --accept-source-agreements --accept-package-agreements -h
echo.

echo [6/8] Instalando QPDF...
winget install --id qpdf.qpdf -e --accept-source-agreements --accept-package-agreements -h
echo.

:: ------------------------------------------------------------
:: Instalar dependencias Python
:: ------------------------------------------------------------
echo [8/8] Instalando dependencias Python (reportlab, ocrmypdf)...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python no encontrado. Instalando Python 3.12...
    winget install --id Python.Python.3.12 -e --accept-source-agreements --accept-package-agreements -h
)
echo.
python -m pip install --upgrade pip
python -m pip install reportlab ocrmypdf
echo.

:: ------------------------------------------------------------
:: Finalización
:: ------------------------------------------------------------
echo ===========================================================
echo [✔] Instalación completada. 
echo ===========================================================
echo.
pause
exit /b






#!/usr/bin/env bash
# Instalador de dependencias LexnetReady (Linux)
# © 2025 José Carlos Rueda Álvarez — Bandua Legal

set -e
clear

echo "==========================================================="
echo "        LexnetReady - Instalador de dependencias"
echo "==========================================================="
echo
echo "Este script instalará todos los programas y librerías necesarias"
echo "para que LexnetReady funcione correctamente en Linux."
echo "ANTES DE CONTINUAR, DEBE TENER INSTALADO AUTOFIRMA Y SU CERTIFICADO"
echo "ACA IMPORTADO EN MOZILLA FIREFOX."
echo
echo "Versión: 2025.11"
echo "Desarrollado por: José Carlos Rueda Álvarez (Bandua Legal)"
echo "==========================================================="
echo

# ------------------------------------------------------------
# Comprobación de privilegios
# ------------------------------------------------------------
if [ "$EUID" -ne 0 ]; then
  echo "[X] Este instalador debe ejecutarse como superusuario (sudo)."
  echo
  echo "Ejecute:"
  echo "    sudo ./instalar_lexnetready_linux.sh"
  echo
  exit 1
fi

# ------------------------------------------------------------
# Instalación con apt
# ------------------------------------------------------------
echo "[1/8] Actualizando lista de paquetes..."
apt update -y
echo

echo "[2/8] Instalando LibreOffice..."
apt install -y libreoffice
echo

echo "[3/8] Instalando Java (JRE)..."
apt install -y default-jre
echo

echo "[4/8] Instalando Tesseract OCR..."
apt install -y tesseract-ocr
echo

echo "[5/8] Instalando Ghostscript..."
apt install -y ghostscript
echo

echo "[6/8] Instalando Poppler y QPDF..."
apt install -y poppler-utils qpdf
echo

echo "[7/8] Instalando OCRmyPDF..."
apt install -y ocrmypdf
echo

echo "[8/8] Instalando dependencias Python..."
apt install -y python3-pip
python3 -m pip install --upgrade pip
python3 -m pip install reportlab ocrmypdf
echo

# ------------------------------------------------------------
# AutoFirma (nota)
# ------------------------------------------------------------
echo "-----------------------------------------------------------"
echo "[!] AutoFirma debe instalarse manualmente desde el portal oficial:"
echo "    https://firmaelectronica.gob.es/Home/Descargas.html"
echo "-----------------------------------------------------------"
echo

# ------------------------------------------------------------
# Comprobación final
# ------------------------------------------------------------
echo "Verificando componentes instalados..."
for cmd in java libreoffice tesseract ocrmypdf pdfsig qpdf; do
  if command -v "$cmd" >/dev/null 2>&1; then
    echo "  ✓ $cmd encontrado en $(command -v "$cmd")"
  else
    echo "  × $cmd no encontrado"
  fi
done
echo

echo "==========================================================="
echo " [✔] Instalación completada correctamente." 
echo "==========================================================="

# LexnetReady — Requisitos e Instalación

**LexnetReady** automatiza la preparación de documentos para su presentación en la plataforma LexNET (PDF/A, OCR, índice y firma digital con AutoFirma) en cumplimiento de toda la normativa establecida a tal efecto. Está creado por José Carlos Rueda, abogado de Bandua Legal. 

LexnetReady supera los requisitos mínimos establecidos por ley para la preparación de escritos a presentar en Lexnet. Le permite crear una carpeta con la demanda, documentos (en CUALQUIER formato, pues él se encargará de pasarlos a PDF) y convertirla lista para presentar. Además de todo lo anterior, genera un archivo de índice interactivo ("documento 0") también exigido por la normativa y que pocos abogados/procuradores cumplen. 

CONVERSIÓN PDF --> PDF/A --> OCR --> FIRMA --> VERIFICACIÓN --> ÍNDICE

---

## ✅ Qué hace concretamente LexnetReady

* Permite **seleccionar múltiples documentos** en un solo gesto.
* Convierte automáticamente los archivos que **no están en PDF** (por ejemplo: Word, imágenes, escaneos) a formato PDF usando LibreOffice en modo headless (conversión sin intervención).  
* Aplica a cada archivo PDF el proceso de **OCR** y conversión al estándar **PDF/A**, para cumplir con los requisitos documentales del sistema (formato de preservación + texto seleccionable). 
* Genera un **índice documental** (“DOC 0 – Indice.pdf”) con listado de los archivos finales.
* Integra el uso de AutoFirma para firmar digitalmente los PDF, incluyendo solo los que se hayan marcado para firma mediante checkbox (y dejando los demás para solo conversión).  
* Verifica automáticamente la firma digital y extrae información clave para confirmar.  
* Proporciona una interfaz gráfica con log en tiempo real, barra de progreso, selección de firma, generación de índice opcional y detección multiplataforma (Windows / Linux / macOS).

---

## 🕒 Beneficio real en despachos

> Un envío típico de 10 documentos (mezcla de Word, imágenes, PDF sin OCR) manual podría implicar: preparar cada archivo, exportar a PDF/A, revisar OCR, generar índice, firmar cada documento, verificar y borrar intermedios → entre **45 y 90 minutos**.  
> Con LexnetReady, ese mismo envío puede realizarse en **menos de 5 minutos**, incluyendo generación de índice, firma selectiva y verificación automática. Esto se traduce en **decenas de horas al año** por abogado/libro, tiempo que se puede dedicar al asesoramiento jurídico.  
Además, reduce el coste oculto del riesgo de rechazo o de tener que rehacer un envío por fallo técnico.

---

## 🚀 Principales bondades

* **Ahorro de tiempo significativo**: en lugar de convertir manualmente, revisar si es PDF/A + OCR, generar índice, firmar y verificar uno por uno, todo se realiza en un solo flujo. Un proceso que antes podía llevar **30-60 minutos por envío** (dependiendo del número de documentos) ahora puede realizarse en **menos de 5 minutos**, liberando al abogado para tareas de mayor valor.  
* **Reducción de errores y rechazos**: puesto que el sistema automatiza los formatos obligatorios (PDF/A + OCR + firma), minimiza los riesgos de que el envío sea rechazado por no cumplir requisitos técnicos. 
* **Versatilidad multiplataforma**: Windows, Linux y macOS son soportados gracias a detección automática de rutas y comandos, lo que permite desplegar en distintos entornos sin reescribir el flujo.  
* **Selección flexible de firma**: no todos los anexos requieren firma digital; con LexnetReady usted decide qué documentos firmas y cuáles solo pasan por conversión, manteniendo control y simplificando los anexos que no requieren firma.  
* **Gestión de documentos optimizada**: la carpeta de envío única (“LEXNET_READY”) contiene solo los archivos finales listos para presentación, lo que reduce desorden, elimina intermedios y facilita el envío al buzón LexNET.

---

## 🔧 Público objetivo

LexnetReady está orientado a despachos de abogados o procuradores que:
- Presentan con regularidad escritos y documentos en LexNET.  
- Quieren reducir tiempos operativos y dedicar menos personal a tareas técnicas.  
- Necesitan asegurar que sus envíos cumplen los requisitos legales y técnicos (PDF/A + OCR + firma).  
- Buscan centralizar y sistematizar su flujo documental en un solo botón.


---

## 📋 Cómo empezar

1. Verifique que AutoFirma esté instalada con certificado ACA y que Firefox reconoce ese certificado.  
2. Instale las dependencias (puede usar los scripts `instalar-windows.bat` o `instalar-linux.sh` que se incluyen).  
3. Inicie LexnetReady, arrastre los documentos, marque los que quiere firmar, pulse “Iniciar proceso”.  
4. Verifique en la carpeta creada `LEXNET_READY` que solo estén los archivos finales listos para presentación.  
5. Suba al buzón LexNET.

ATENCIÓN: LEXNETREADY NO GENERA FIRMA VISIBLE. Esto quiere decir que sus documentos estarán firmados digitalmente pero no mostrará ningún estampado, pero será comprobable en cualquier visor de PDF. La normativa no exige este estampado.

---

## Requisitos adicionales (dependencias)

LexnetReady es muy eficaz, pero depende de diversos programas externos.  
Para facilitar su uso, existen instaladores preparados para Windows y Linux.

### Windows  
- Haga clic derecho en `instalar-windows.bat` y seleccione **“Ejecutar como administrador”**.  
  Este script se encargará de instalar automáticamente todas las dependencias marcadas.

### Linux (Debian/Ubuntu)  
- En consola, navegue al directorio del instalador y ejecute:
  ```bash
  chmod +x instalar-linux.sh
  sudo ./instalar-linux.sh
  ```

El script instalará las dependencias necesarias automáticamente.

## Si no lo consigue...

Si por algún motivo los scripts NO consiguen instalar las dependencias, LexnetReady no funcionará correctamente, por lo que deberá instalar manualmente los siguientes componentes:

* Java Runtime Environment (JRE)
* LibreOffice (versión con soporte de línea de comandos / modo “headless”)
* OCRmyPDF
* Tesseract OCR
* Ghostscript
* QPDF
* Poppler-utils (comando pdfsig)
* Python 3
* Tkinter para Python
* Reportlab para Python

Sé que parece mucho… pero instalar estas dependencias sólo ha de hacerse una vez, y le ahorrará muchas horas de trabajo manual en el futuro.


## Tras instalar las dependencias...

¡Ya está listo para ejecutar! Ejecute `python3 lexnetready.py` en la carpeta de la aplicación. 

Para usuarios en Windows, puede ejecutar el archivo (doble click) en "LexnetReadyWindows.bat". 

Si tiene dudas, abra una `issue` en este repositorio de github y estaré encantado de ayudar.

#!/usr/bin/env python3
# LexnetReady.py — versión multiplataforma (Windows, Linux, macOS) con verificación de dependencias

import os
import sys
import platform
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import threading
import re

# --- DETECCIÓN DE PLATAFORMA ---
SO = platform.system().lower()

if SO == "windows":
    AUTO_FIRMA_JAR = r"C:\Program Files\AutoFirma\AutoFirma.jar"
    LIBREOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"
    PDFSIG = "pdfsig.exe"
    STORE_TYPE = "auto"
elif SO == "darwin":
    AUTO_FIRMA_JAR = "/Applications/AutoFirma.app/Contents/Java/AutoFirma.jar"
    LIBREOFFICE = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    PDFSIG = "pdfsig"
    STORE_TYPE = "auto"
else:  # Linux
    AUTO_FIRMA_JAR = "/usr/lib/Autofirma/autofirma.jar"
    LIBREOFFICE = "libreoffice"
    PDFSIG = "pdfsig"
    STORE_TYPE = "mozilla"

# --- CHEQUEO DE DEPENDENCIAS ---
def comprobar_dependencias():
    faltantes = []

    def existe_comando(cmd):
        return shutil.which(cmd) is not None

    # 1. Python libs
    try:
        import reportlab, ocrmypdf
    except ImportError:
        faltantes.append("Python: reportlab u ocrmypdf")

    # 2. LibreOffice
    if not os.path.exists(LIBREOFFICE) and not existe_comando("libreoffice"):
        faltantes.append("LibreOffice (no encontrado)")

    # 3. AutoFirma
    if not os.path.exists(AUTO_FIRMA_JAR):
        faltantes.append(f"AutoFirma.jar no encontrado en {AUTO_FIRMA_JAR}")

    # 4. pdfsig (Poppler)
    if not existe_comando(PDFSIG):
        faltantes.append("pdfsig (Poppler-utils) no encontrado en PATH")

    if faltantes:
        mensaje = "No se encontraron las siguientes dependencias:\n\n" + "\n".join(faltantes) + \
                  "\n\nInstálelas y vuelva a ejecutar LexnetReady."
        messagebox.showerror("Dependencias faltantes", mensaje)
        sys.exit(1)

# Llamamos al chequeo antes de todo
comprobar_dependencias()


# --- LOG ---
def log(texto):
    log_box.config(state='normal')
    log_box.insert(tk.END, texto + "\n")
    log_box.see(tk.END)
    log_box.config(state='disabled')


def bloquear_interfaz():
    btn_add.config(state="disabled")
    btn_start.config(state="disabled")
    chk_indice.config(state="disabled")
    tree.unbind("<Button-1>")


# --- PIPELINE PRINCIPAL ---
def procesar_documentos(carpeta_base, barra):
    iids = tree.get_children()
    if not iids:
        messagebox.showwarning("Aviso", "No hay documentos en la lista.")
        return

    carpeta_salida = os.path.join(carpeta_base, "LEXNET_READY")
    os.makedirs(carpeta_salida, exist_ok=True)

    total = len(iids)
    for idx, iid in enumerate(iids, start=1):
        ruta = iid
        base = os.path.basename(ruta)
        destino = os.path.join(carpeta_salida, os.path.splitext(base)[0] + ".pdf")

        log(f"[{idx}/{total}] Procesando {base}")
        barra["value"] = (idx - 1) / total * 100
        barra.update_idletasks()

        src_for_ocr = ruta
        if not ruta.lower().endswith(".pdf"):
            try:
                subprocess.run([
                    LIBREOFFICE, "--headless", "--convert-to", "pdf",
                    "--outdir", carpeta_salida, ruta
                ], check=True)
                src_for_ocr = os.path.join(carpeta_salida, os.path.splitext(base)[0] + ".pdf")
                log("  → Convertido a PDF.")
            except subprocess.CalledProcessError:
                log(f"  × Error al convertir {base} a PDF.")
                continue

        try:
            subprocess.run([
                "ocrmypdf", "--force-ocr", "--output-type", "pdfa",
                src_for_ocr, destino
            ], check=True)
            log("  → PDF/A con OCR generado.")
        except subprocess.CalledProcessError:
            log(f"  × Error al aplicar OCR en {base}.")
            continue

        barra["value"] = (idx / total) * 100
        barra.update_idletasks()

    firmar_seleccionados(carpeta_salida, iids)
    limpiar_originales_con_firmado(carpeta_salida)

    if var_indice.get():
        generar_indice_final(carpeta_salida)
        log("Índice documental 'DOC 0 - Indice.pdf' creado sobre el estado final.")
        firmar_y_limpia_doc0(carpeta_salida)

    bloquear_interfaz()
    barra["value"] = 100
    log("Proceso completado. Archivos listos en LEXNET_READY.")
    messagebox.showinfo(
        "Proceso completado",
        "Dentro de la carpeta donde estaban sus archivos originales se ha creado la carpeta "
        "LEXNET_READY con los archivos listos para su presentación."
    )


# --- FUNCIONES AUXILIARES ---
def firmar_seleccionados(carpeta_salida, todos):
    for ruta in todos:
        base = os.path.basename(ruta)
        nombre_base = os.path.splitext(base)[0]
        destino = os.path.join(carpeta_salida, f"{nombre_base}.pdf")
        if not os.path.exists(destino):
            continue
        if checks[ruta].get():
            salida = os.path.join(carpeta_salida, f"{nombre_base}_firmado.pdf")
            log(f"Firmando {os.path.basename(destino)}...")
            try:
                subprocess.run([
                    "java", "-jar", AUTO_FIRMA_JAR, "sign",
                    "-i", destino,
                    "-o", salida,
                    "-store", STORE_TYPE,
                    "-certgui",
                    "-format", "pades"
                ], check=True)
                verificar_firma(salida)
            except subprocess.CalledProcessError as e:
                log(f"  × Error firmando {os.path.basename(destino)}: {e}")
        else:
            log(f"{os.path.basename(destino)} — no marcado para firma (solo convertido).")


def verificar_firma(pdf_firmado_path):
    try:
        out = subprocess.run([PDFSIG, pdf_firmado_path], capture_output=True, text=True, check=True).stdout
        cn = re.search(r"Signer Certificate Common Name:\s*(.+)", out)
        fecha = re.search(r"Signing Time:\s*([^\n]+)", out)
        cn_text = cn.group(1).strip() if cn else "CN no detectado"
        fecha_text = fecha.group(1).strip() if fecha else "Fecha no detectada"
        log(f"  ✓ Verificado: {os.path.basename(pdf_firmado_path)} — CN: {cn_text} — Fecha: {fecha_text}")
    except subprocess.CalledProcessError as e:
        log(f"  × Error verificando {os.path.basename(pdf_firmado_path)}: {e}")


def limpiar_originales_con_firmado(carpeta_salida):
    archivos = [f for f in os.listdir(carpeta_salida) if f.lower().endswith(".pdf")]
    bases_firmadas = {f[:-12].lower() for f in archivos if f.lower().endswith("_firmado.pdf")}
    for f in archivos:
        if f.lower().endswith("_firmado.pdf"):
            continue
        nombre_base = os.path.splitext(f)[0].lower()
        if nombre_base in bases_firmadas:
            try:
                os.remove(os.path.join(carpeta_salida, f))
                log(f"  → Eliminado original {f}")
            except Exception as e:
                log(f"  × No se pudo eliminar {f}: {e}")


def generar_indice_final(ruta_destino):
    indice = os.path.join(ruta_destino, "DOC 0 - Indice.pdf")
    doc = SimpleDocTemplate(indice)
    styles = getSampleStyleSheet()
    copyright_style = ParagraphStyle(name='CopyrightStyle', parent=styles['Normal'], textColor=colors.lightgrey)
    flow = [Paragraph("<h1>ÍNDICE DOCUMENTAL</h1>", styles['Title']), Spacer(1, 12)]
    lista = [f for f in os.listdir(ruta_destino) if f.lower().endswith(".pdf") and not f.lower().startswith("doc 0")]
    for f in sorted(lista, key=str.lower):
        nombre = os.path.splitext(f)[0].upper()
        flow.append(Paragraph(f"<a href='{f}'>{nombre}</a>", styles['Normal']))
        flow.append(Spacer(1, 6))
    flow.append(Spacer(1, 24))
    flow.append(Paragraph("<para align=center>Índice generaado por LexnetReady - MIT-TAL license. 2025, José Carlos Rueda (jcrueda.com).</para>", copyright_style))
    doc.build(flow)


def firmar_y_limpia_doc0(carpeta_salida):
    doc0 = os.path.join(carpeta_salida, "DOC 0 - Indice.pdf")
    if not os.path.exists(doc0):
        log("× DOC 0 - Indice.pdf no encontrado para firma.")
        return
    salida_doc0 = os.path.join(carpeta_salida, "DOC 0 - Indice_firmado.pdf")
    log("Firmando DOC 0 - Indice.pdf...")
    try:
        subprocess.run([
            "java", "-jar", AUTO_FIRMA_JAR, "sign",
            "-i", doc0,
            "-o", salida_doc0,
            "-store", STORE_TYPE,
            "-certgui",
            "-format", "pades"
        ], check=True)
        verificar_firma(salida_doc0)
        try:
            os.remove(doc0)
        except Exception:
            pass
    except subprocess.CalledProcessError as e:
        log(f"  × Error firmando DOC 0 - Indice.pdf: {e}")


# --- GUI ---
def añadir_documentos():
    rutas = filedialog.askopenfilenames(title="Seleccionar documentos", filetypes=[("Archivos", "*.*")])
    if not rutas:
        return
    if tree.get_children():
        ref = os.path.dirname(list(tree.get_children())[0])
        for r in rutas:
            if os.path.dirname(r) != ref:
                messagebox.showerror("Error", "Todos los archivos deben estar en la misma carpeta.")
                return
    for r in rutas:
        if r in checks:
            continue
        checks[r] = tk.BooleanVar(value=True)
        tree.insert("", "end", iid=r, values=("☑", os.path.basename(r)))
    log(f"{len(rutas)} documentos añadidos.")


def iniciar_proceso():
    if not tree.get_children():
        messagebox.showwarning("Aviso", "No hay documentos cargados.")
        return
    carpeta_base = os.path.dirname(list(tree.get_children())[0])
    threading.Thread(target=procesar_documentos, args=(carpeta_base, barra_progreso), daemon=True).start()


def on_tree_click(event):
    region = tree.identify("region", event.x, event.y)
    if region != "cell":
        return
    col = tree.identify_column(event.x)
    if col != "#1":
        return
    iid = tree.identify_row(event.y)
    if not iid:
        return
    val = checks[iid].get()
    checks[iid].set(not val)
    tree.set(iid, "Firmar?", "☑" if checks[iid].get() else "☐")


# --- MAIN GUI ---
root = tk.Tk()
root.title("LexnetReady — Conversión + PDF/A + OCR + Firma + Índice")
root.geometry("850x640")

lbl_copy = tk.Label(
    root,
    text=f"© 2025 José Carlos Rueda — Bandua Legal | LexnetReady v4.0 ({SO.upper()})",
    fg="gray40",
    font=("Segoe UI", 9)
)
lbl_copy.pack(pady=3)

frame_table = ttk.Frame(root)
frame_table.pack(padx=10, pady=8, fill="x")

cols = ("Firmar?", "Archivo")
tree = ttk.Treeview(frame_table, columns=cols, show="headings", height=10)
tree.heading("Firmar?", text="¿Firmar?")
tree.column("Firmar?", width=80, anchor="center")
tree.heading("Archivo", text="Archivo")
tree.column("Archivo", width=660, anchor="w")
tree.pack(side="left", fill="x", expand=True)
tree.bind("<Button-1>", on_tree_click)

scroll_table = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
tree.configure(yscroll=scroll_table.set)
scroll_table.pack(side="right", fill="y")

checks = {}

frame_buttons = ttk.Frame(root)
frame_buttons.pack(padx=10, pady=6, fill="x")
btn_add = ttk.Button(frame_buttons, text="Añadir documentos", command=añadir_documentos)
btn_add.pack(side="left", padx=5)
btn_start = ttk.Button(frame_buttons, text="Iniciar proceso", command=iniciar_proceso)
btn_start.pack(side="left", padx=5)

var_indice = tk.BooleanVar(value=True)
chk_indice = ttk.Checkbutton(frame_buttons, text="Generar índice", variable=var_indice)
chk_indice.pack(side="left", padx=15)

barra_progreso = ttk.Progressbar(root, orient="horizontal", length=800, mode="determinate")
barra_progreso.pack(padx=10, pady=6, fill="x")

frame_log = ttk.Frame(root)
frame_log.pack(padx=10, pady=6, fill="both", expand=True)
log_box = tk.Text(frame_log, height=18, width=100, wrap="word", state="disabled", bg="#f7f7f7")
scroll_log = ttk.Scrollbar(frame_log, orient="vertical", command=log_box.yview)
log_box.configure(yscroll=scroll_log.set)
log_box.pack(side="left", fill="both", expand=True)
scroll_log.pack(side="right", fill="y")

root.mainloop()

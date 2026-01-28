import sys
import os
import subprocess
import shutil
import threading
import zipfile
import tarfile
import pandas as pd
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QProgressBar, 
                             QComboBox, QFileDialog, QFrame)
from PySide6.QtCore import Qt, QThread, Signal, QSize
from PySide6.QtGui import QColor, QFont, QPalette, QDragEnterEvent, QDropEvent
from PIL import Image
import pypandoc

# =================================================================
# REGISTRE DES FORMATS (60+ EXTENSIONS)
# =================================================================
FORMATS = {
    "🎬 VIDÉO": ["mp4", "mkv", "avi", "mov", "webm", "flv", "wmv", "m4v", "3gp", "mpg", "mpeg", "ts", "vob", "m2ts", "ogv"],
    "🎧 AUDIO": ["mp3", "wav", "flac", "aac", "ogg", "opus", "m4a", "wma", "aiff", "mid", "ac3", "amr", "mka", "ra"],
    "🖼️ IMAGE": ["png", "jpg", "jpeg", "webp", "gif", "bmp", "tiff", "svg", "ico", "heic", "tga", "psd", "eps", "ppm"],
    "📄 DOCUMENT": ["pdf", "docx", "doc", "txt", "rtf", "odt", "html", "md", "epub", "tex", "mobi", "azw3"],
    "📊 DONNÉES": ["xlsx", "xls", "csv", "json", "xml", "yaml", "sql", "parquet", "pickle"],
    "🗜️ ARCHIVE": ["zip", "tar", "gz", "bz2", "xz"]
}

# =================================================================
# MOTEUR DE CONVERSION UNIVERSEL
# =================================================================
class ConversionEngine:
    @staticmethod
    def convert(input_path, output_path, target_ext):
        source_ext = input_path.split('.')[-1].lower()
        target_ext = target_ext.lower()

        # --- LOGIQUE MÉDIA (FFmpeg) ---
        if target_ext in FORMATS["🎬 VIDÉO"] or target_ext in FORMATS["🎧 AUDIO"]:
            cmd = ['ffmpeg', '-y', '-i', input_path, '-preset', 'fast', output_path]
            subprocess.run(cmd, capture_output=True, check=True)

        # --- LOGIQUE IMAGE (Pillow) ---
        elif target_ext in FORMATS["🖼️ IMAGE"]:
            with Image.open(input_path) as img:
                if target_ext in ["jpg", "jpeg"] and img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                img.save(output_path, optimize=True)

        # --- LOGIQUE DOCUMENT (Pandoc) ---
        elif target_ext in FORMATS["📄 DOCUMENT"]:
            # Note: PDF nécessite wkhtmltopdf ou pdflatex installé pour Pandoc
            pypandoc.convert_file(input_path, target_ext, outputfile=output_path)

        # --- LOGIQUE DONNÉES (Pandas) ---
        elif target_ext in FORMATS["📊 DONNÉES"]:
            # Lecture
            if source_ext == 'csv': df = pd.read_csv(input_path)
            elif source_ext in ['xls', 'xlsx']: df = pd.read_excel(input_path)
            elif source_ext == 'json': df = pd.read_json(input_path)
            elif source_ext == 'parquet': df = pd.read_parquet(input_path)
            else: df = pd.DataFrame() # Fallback

            # Écriture
            if target_ext == 'csv': df.to_csv(output_path, index=False)
            elif target_ext in ['xls', 'xlsx']: df.to_excel(output_path, index=False)
            elif target_ext == 'json': df.to_json(output_path, indent=4)
            elif target_ext == 'xml': df.to_xml(output_path)
            elif target_ext == 'parquet': df.to_parquet(output_path)

        # --- LOGIQUE ARCHIVE (Standard Lib) ---
        elif target_ext == 'zip':
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as f:
                f.write(input_path, os.path.basename(input_path))
        elif target_ext in ['tar', 'gz', 'bz2', 'xz']:
            mode = f"w:{target_ext}" if target_ext != 'tar' else "w"
            with tarfile.open(output_path, mode) as f:
                f.add(input_path, arcname=os.path.basename(input_path))

# =================================================================
# WORKER THREAD
# =================================================================
class Worker(QThread):
    row_update = Signal(int, str, int) # index, status, progress

    def __init__(self, index, input_path, target_ext):
        super().__init__()
        self.index = index
        self.input_path = input_path
        self.target_ext = target_ext

    def run(self):
        try:
            self.row_update.emit(self.index, "Initialisation...", 10)
            
            out_dir = os.path.join(os.path.dirname(self.input_path), "Nexus_Output")
            os.makedirs(out_dir, exist_ok=True)
            
            base_name = os.path.basename(self.input_path).rsplit('.', 1)[0]
            out_path = os.path.join(out_dir, f"{base_name}.{self.target_ext}")
            
            self.row_update.emit(self.index, "Conversion en cours...", 40)
            ConversionEngine.convert(self.input_path, out_path, self.target_ext)
            
            self.row_update.emit(self.index, "Terminé", 100)
        except Exception as e:
            print(f"Erreur: {e}")
            self.row_update.emit(self.index, "Échec", 0)

# =================================================================
# UI PRINCIPALE
# =================================================================
class NexusOmniApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NexusConvert Pro Omni-Edition")
        self.resize(1200, 800)
        self.files = []
        self.setup_ui()
        self.setup_styling()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(30, 30, 30, 30)

        # Titre
        title = QLabel("NEXUS CONVERT PRO")
        title.setStyleSheet("font-size: 35px; font-weight: 900; color: white; letter-spacing: 5px;")
        layout.addWidget(title, alignment=Qt.AlignCenter)

        # Zone Drop
        self.drop_zone = QFrame()
        self.drop_zone.setAcceptDrops(True)
        self.drop_zone.setMinimumHeight(150)
        self.drop_zone.setObjectName("dropZone")
        dz_layout = QVBoxLayout(self.drop_zone)
        dz_label = QLabel("GLISSEZ-DÉPOSEZ VOS FICHIERS ICI\n(Supporte Vidéo, Audio, Image, Doc, Data, Archive)")
        dz_label.setAlignment(Qt.AlignCenter)
        dz_label.setStyleSheet("color: #666; font-size: 14px; font-weight: bold;")
        dz_layout.addWidget(dz_label)
        layout.addWidget(self.drop_zone)

        # Table des fichiers
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["NOM", "TYPE ACTUEL", "TYPE CIBLE", "STATUT", "PROGRESSION"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        # Barre d'actions
        actions = QHBoxLayout()
        
        self.target_combo = QComboBox()
        self.target_combo.setMinimumWidth(250)
        for cat, exts in FORMATS.items():
            self.target_combo.addItem(f"--- {cat} ---")
            for e in sorted(exts):
                self.target_combo.addItem(e.upper())
        
        btn_start = QPushButton("LANCER LA CONVERSION")
        btn_start.setObjectName("btnStart")
        btn_start.clicked.connect(self.run_all)
        
        btn_clear = QPushButton("EFFACER TOUT")
        btn_clear.clicked.connect(self.clear_table)

        actions.addWidget(QLabel("Convertir vers :"))
        actions.addWidget(self.target_combo)
        actions.addStretch()
        actions.addWidget(btn_clear)
        actions.addWidget(btn_start)
        layout.addLayout(actions)

    def setup_styling(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #0A0A0A; }
            QWidget { font-family: 'Segoe UI'; color: #DDD; }
            #dropZone { 
                border: 2px dashed #333; border-radius: 15px; background: #111; 
            }
            #dropZone:hover { border-color: #00A2FF; background: #151515; }
            QTableWidget { 
                background: #111; border: 1px solid #222; border-radius: 10px; 
            }
            QHeaderView::section { background: #1A1A1A; border: none; padding: 10px; font-weight: bold; }
            QPushButton { 
                background: #222; border: 1px solid #333; padding: 10px 20px; border-radius: 5px; font-weight: bold;
            }
            QPushButton:hover { background: #333; }
            #btnStart { background: #0078D4; border: none; color: white; }
            #btnStart:hover { background: #1086E0; }
            QProgressBar { border: none; background: #222; height: 8px; border-radius: 4px; text-align: center; }
            QProgressBar::chunk { background: #0078D4; border-radius: 4px; }
            QComboBox { background: #1A1A1A; border: 1px solid #333; padding: 8px; }
        """)

    # --- LOGIQUE ---
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls(): e.accept()
        else: e.ignore()

    def dropEvent(self, e):
        for url in e.mimeData().urls():
            path = url.toLocalFile()
            self.add_to_table(path)

    def add_to_table(self, path):
        row = self.table.rowCount()
        self.table.insertRow(row)
        ext = path.split('.')[-1].upper()
        
        self.table.setItem(row, 0, QTableWidgetItem(os.path.basename(path)))
        self.table.setItem(row, 1, QTableWidgetItem(ext))
        self.table.setItem(row, 2, QTableWidgetItem(self.target_combo.currentText()))
        self.table.setItem(row, 3, QTableWidgetItem("Prêt"))
        
        pbar = QProgressBar()
        self.table.setCellWidget(row, 4, pbar)
        self.files.append({'path': path, 'row': row})

    def clear_table(self):
        self.table.setRowCount(0)
        self.files = []

    def run_all(self):
        target = self.target_combo.currentText()
        if "---" in target: return # Ignorer les headers de catégorie
        
        for f in self.files:
            worker = Worker(f['row'], f['path'], target.lower())
            worker.row_update.connect(self.on_update)
            worker.start()

    def on_update(self, row, status, val):
        self.table.setItem(row, 3, QTableWidgetItem(status))
        self.table.cellWidget(row, 4).setValue(val)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = NexusOmniApp()
    win.show()
    sys.exit(app.exec())
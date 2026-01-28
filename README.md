# NexusConvert Pro - Convertisseur Universel de Fichiers

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**NexusConvert Pro Omni-Edition** est un convertisseur de fichiers universel avec interface graphique moderne, supportant plus de 60 formats de fichiers différents répartis en 6 catégories principales.

## 🎯 Fonctionnalités

- ✨ **Interface Graphique Moderne** : Interface utilisateur élégante avec thème sombre
- 🎬 **Conversion Vidéo** : MP4, MKV, AVI, MOV, WebM, FLV, WMV, et plus
- 🎧 **Conversion Audio** : MP3, WAV, FLAC, AAC, OGG, OPUS, et plus
- 🖼️ **Conversion Image** : PNG, JPG, WebP, GIF, BMP, TIFF, SVG, et plus
- 📄 **Conversion Document** : PDF, DOCX, TXT, HTML, Markdown, EPUB, et plus
- 📊 **Conversion Données** : XLSX, CSV, JSON, XML, YAML, Parquet, et plus
- 🗜️ **Compression Archive** : ZIP, TAR, GZ, BZ2, XZ
- 🎯 **Glisser-Déposer** : Ajoutez facilement des fichiers par glisser-déposer
- ⚡ **Traitement par Lots** : Convertissez plusieurs fichiers simultanément
- 📊 **Suivi en Temps Réel** : Barre de progression pour chaque conversion

## 📦 Formats Supportés

### 🎬 Vidéo (15 formats)
`mp4`, `mkv`, `avi`, `mov`, `webm`, `flv`, `wmv`, `m4v`, `3gp`, `mpg`, `mpeg`, `ts`, `vob`, `m2ts`, `ogv`

### 🎧 Audio (14 formats)
`mp3`, `wav`, `flac`, `aac`, `ogg`, `opus`, `m4a`, `wma`, `aiff`, `mid`, `ac3`, `amr`, `mka`, `ra`

### 🖼️ Image (15 formats)
`png`, `jpg`, `jpeg`, `webp`, `gif`, `bmp`, `tiff`, `svg`, `ico`, `heic`, `tga`, `psd`, `eps`, `ppm`

### 📄 Document (12 formats)
`pdf`, `docx`, `doc`, `txt`, `rtf`, `odt`, `html`, `md`, `epub`, `tex`, `mobi`, `azw3`

### 📊 Données (9 formats)
`xlsx`, `xls`, `csv`, `json`, `xml`, `yaml`, `sql`, `parquet`, `pickle`

### 🗜️ Archive (5 formats)
`zip`, `tar`, `gz`, `bz2`, `xz`

## 🔧 Prérequis

### Dépendances Système

1. **FFmpeg** (pour conversion vidéo/audio)
   ```bash
   # Ubuntu/Debian
   sudo apt-get install ffmpeg
   
   # macOS
   brew install ffmpeg
   
   # Windows
   # Télécharger depuis https://ffmpeg.org/download.html
   ```

2. **Pandoc** (pour conversion de documents)
   ```bash
   # Ubuntu/Debian
   sudo apt-get install pandoc
   
   # macOS
   brew install pandoc
   
   # Windows
   # Télécharger depuis https://pandoc.org/installing.html
   ```

3. **wkhtmltopdf** (optionnel, pour conversion PDF avec Pandoc)
   ```bash
   # Ubuntu/Debian
   sudo apt-get install wkhtmltopdf
   
   # macOS
   brew install wkhtmltopdf
   
   # Windows
   # Télécharger depuis https://wkhtmltopdf.org/downloads.html
   ```

### Dépendances Python

Python 3.8 ou supérieur est requis.

## 📥 Installation

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/rafael12g/convertisseur.git
   cd convertisseur
   ```

2. **Installer les dépendances Python**
   ```bash
   pip install PySide6 Pillow pypandoc pandas openpyxl
   ```

   Ou avec un fichier requirements.txt (si créé) :
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Utilisation

1. **Lancer l'application**
   ```bash
   python convert.py
   ```

2. **Convertir des fichiers**
   - Glissez-déposez vos fichiers dans la zone prévue à cet effet
   - Sélectionnez le format de sortie désiré dans le menu déroulant
   - Cliquez sur "LANCER LA CONVERSION"
   - Les fichiers convertis seront sauvegardés dans le dossier `Nexus_Output` à côté de vos fichiers source

3. **Effacer la liste**
   - Cliquez sur "EFFACER TOUT" pour vider la liste des fichiers

## 📂 Structure du Projet

```
convertisseur/
├── convert.py          # Application principale
└── README.md          # Ce fichier
```

Les fichiers convertis sont automatiquement sauvegardés dans :
```
<dossier_source>/Nexus_Output/<nom_fichier>.<extension_cible>
```

## 🎨 Interface

L'application propose une interface moderne avec :
- Thème sombre élégant
- Zone de glisser-déposer intuitive
- Tableau de suivi des conversions
- Barres de progression individuelles
- Statuts en temps réel

## ⚠️ Notes Importantes

- **Conversions Vidéo/Audio** : Utilise FFmpeg avec preset "fast" pour un équilibre performance/qualité
- **Conversions Image** : Optimisation automatique, conversion RGB pour JPEG si nécessaire
- **Conversions Document** : Certaines conversions PDF peuvent nécessiter LaTeX ou wkhtmltopdf
- **Conversions Données** : Support limité selon les formats source/destination
- **Archives** : Crée une archive contenant le fichier source

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Améliorer la documentation
- Soumettre des pull requests

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 🐛 Dépannage

### Erreur FFmpeg
- Vérifiez que FFmpeg est installé : `ffmpeg -version`
- Assurez-vous que FFmpeg est dans votre PATH

### Erreur Pandoc
- Vérifiez que Pandoc est installé : `pandoc --version`
- Pour les conversions PDF, installez wkhtmltopdf ou LaTeX

### Erreur de dépendances Python
- Assurez-vous d'utiliser Python 3.8+
- Réinstallez les dépendances : `pip install --upgrade PySide6 Pillow pypandoc pandas openpyxl`

## 📧 Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue sur GitHub.

---

**Développé avec ❤️ par rafael12g**

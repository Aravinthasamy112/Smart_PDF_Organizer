# Smart PDF Organizer

> A Python-based desktop application for scanning, organizing, and managing PDF files with metadata extraction, duplicate detection, and automated report generation.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-009688)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite)

---

## 📌 Overview

**Smart PDF Organizer** is a lightweight desktop application developed using **Python** and **Tkinter** for efficiently organizing and managing PDF files.

The application recursively scans folders, extracts PDF metadata, stores scan history in a local SQLite database, detects duplicate PDF files using **SHA-256 hashing**, organizes files into structured folders, and generates reports in both **CSV** and **Excel** formats.

It is a lightweight, fully offline application that requires no internet connection or cloud services.

---

## ⭐ Key Highlights

- 📂 Recursive PDF Folder Scanning
- 🔍 SHA-256 Duplicate File Detection
- 📑 PDF Metadata Extraction
- 🗃 SQLite Database Integration
- 📁 Automatic PDF Organization
- 📊 CSV & Excel Report Generation
- 🔎 Searchable Scan History
- 💻 Fully Offline Desktop Application
- ⚡ Lightweight and Easy to Use
- 🖥 Cross-Platform Desktop Application

---

## ✨ Features

- Scan folders recursively for PDF files
- Extract PDF metadata including:
  - File Name
  - File Path
  - File Size
  - Number of Pages
  - Created Date
  - Modified Date
- Store scan history using SQLite
- Detect duplicate PDF files using SHA-256 hashing
- Automatically organize PDF files into destination folders
- Export reports in CSV format
- Export reports in Excel (.xlsx) format
- Search previously scanned PDF files
- Display real-time progress and status updates
- Maintain application logs
- Safely organize files without overwriting existing files

---

## 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| Programming Language | Python 3 |
| GUI Framework | Tkinter |
| Database | SQLite |
| PDF Library | pypdf |
| Excel Reports | openpyxl |
| CSV Reports | csv |
| File Hashing | hashlib |
| Logging | logging |

---

## 📂 Project Structure

```text
Smart_PDF_Organizer/

├── main.py
├── gui.py
├── scanner.py
├── organizer.py
├── duplicate.py
├── report.py
├── database.py
├── config.py
├── utils.py
├── requirements.txt
├── reports/
├── logs/
├── organized_files/
└── smart_pdf_organizer.db
```

---

## 📋 Requirements

- Python 3.9 or later
- pypdf
- openpyxl

---

## ⚙ Installation

### Clone the Repository

```bash
git clone https://github.com/Aravinthasamy112/Smart_PDF_Organizer.git
```

### Navigate to the Project Folder

```bash
cd Smart_PDF_Organizer
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install Required Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶ Running the Application

Run the following command:

```bash
python main.py
```

The Smart PDF Organizer application will launch automatically.

---

## 📊 Application Workflow

```text
Select Folder
      │
      ▼
Scan PDF Files
      │
      ▼
Extract PDF Metadata
      │
      ▼
Store Information in SQLite Database
      │
      ▼
Detect Duplicate Files
      │
      ▼
Organize PDF Files
      │
      ▼
Generate CSV / Excel Reports
```

---

## 🚀 Future Enhancements

- OCR Support
- Drag-and-Drop File Support
- PDF Preview
- Background Scanning
- AI-Based Document Classification
- Cloud Synchronization
- Scheduled Automatic Scanning
- Light & Dark Theme
- Batch File Renaming
- Standalone Executable (.exe)

---

## 👨‍💻 Developed By

### Aravinthasamy A

[![Email](https://img.shields.io/badge/Email-Contact-red?style=for-the-badge&logo=gmail)](mailto:aravinthasamy2006as@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-Profile-black?style=for-the-badge&logo=github)](https://github.com/Aravinthasamy112)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/aravinthasamyas)

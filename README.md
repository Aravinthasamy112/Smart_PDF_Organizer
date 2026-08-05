# Smart PDF Organizer

A Python desktop application that scans PDF files, extracts metadata, detects duplicate files using SHA-256 hashing, organizes PDFs into folders, stores scan history in SQLite, and exports reports in CSV and Excel formats.

---

## Features

- Recursive PDF folder scanning
- PDF metadata extraction
- SHA-256 duplicate detection
- SQLite database integration
- Automatic PDF organization
- CSV and Excel report generation
- Search scan history
- Logging and exception handling
- User-friendly Tkinter GUI

---

## Tech Stack

- Python 3
- Tkinter
- SQLite3
- pypdf
- pandas
- openpyxl
- hashlib
- shutil
- logging

---

## Project Structure

```
SmartPDFOrganizer/
│
├── assets/
├── sample_pdfs/
├── reports/
├── organized_files/
├── logs/
│
├── main.py
├── gui.py
├── scanner.py
├── database.py
├── duplicate.py
├── organizer.py
├── report.py
├── utils.py
├── config.py
├── requirements.txt
├── README.md
└── smart_pdf_organizer.db
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Aravinthasamy112/SmartPDFOrganizer.git
```

Navigate to the project folder:

```bash
cd SmartPDFOrganizer
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
python main.py
```

---

## Workflow

1. Select a PDF folder.
2. Scan PDF files.
3. Extract metadata.
4. Store details in SQLite.
5. Detect duplicate PDFs using SHA-256.
6. Organize PDFs into folders.
7. Export reports in CSV or Excel format.

---

## Technologies Used

| Category | Technology |
|----------|------------|
| Programming Language | Python 3 |
| GUI | Tkinter |
| Database | SQLite3 |
| PDF Processing | pypdf |
| Report Generation | pandas, openpyxl |
| Duplicate Detection | hashlib (SHA-256) |
| File Operations | shutil |
| Logging | logging |

---

## Future Enhancements

- OCR support
- Drag and Drop functionality
- PDF Preview
- Automatic PDF Categorization
- Multi-threaded scanning
- Standalone Executable (PyInstaller)

---

## Author

**Aravinthasamy A**

B.Tech Artificial Intelligence & Data Science

- GitHub: [Aravinthasamy112](https://github.com/Aravinthasamy112)
- LinkedIn: [aravinthasamyas](https://linkedin.com/in/aravinthasamyas)
---

## License

This project is intended for educational and academic purposes only.
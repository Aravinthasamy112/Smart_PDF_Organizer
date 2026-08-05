"""Application configuration constants for Smart PDF Organizer."""

import os

# Base directory of the application
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Folder paths
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
ORGANIZED_FILES_DIR = os.path.join(BASE_DIR, "organized_files")
SAMPLE_PDFS_DIR = os.path.join(BASE_DIR, "sample_pdfs")

REQUIRED_DIRECTORIES = [
    ASSETS_DIR,
    LOGS_DIR,
    REPORTS_DIR,
    ORGANIZED_FILES_DIR,
    SAMPLE_PDFS_DIR,
]

# Database settings
DATABASE_NAME = "smart_pdf_organizer.db"
DATABASE_PATH = os.path.join(BASE_DIR, DATABASE_NAME)

# Logging settings
LOG_FILE_NAME = "smart_pdf_organizer.log"
LOG_FILE_PATH = os.path.join(LOGS_DIR, LOG_FILE_NAME)
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_MAX_BYTES = 5 * 1024 * 1024
LOG_BACKUP_COUNT = 3

# Application metadata
APP_NAME = "Smart PDF Organizer"
APP_VERSION = "1.0.0"
ORGANIZATION_NAME = "Smart PDF Organizer Project"

# Window settings
WINDOW_TITLE = f"{APP_NAME} v{APP_VERSION}"
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 720
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600
WINDOW_RESIZABLE_WIDTH = True
WINDOW_RESIZABLE_HEIGHT = True

# Theme constants
THEME_BACKGROUND = "#1e1e2e"
THEME_SURFACE = "#282838"
THEME_PRIMARY = "#4f8cff"
THEME_PRIMARY_HOVER = "#3a73e0"
THEME_SECONDARY = "#7c5cff"
THEME_TEXT_PRIMARY = "#f5f5f7"
THEME_TEXT_SECONDARY = "#a0a0b2"
THEME_SUCCESS = "#3ddc97"
THEME_WARNING = "#ffb454"
THEME_ERROR = "#ff5c5c"
THEME_BORDER = "#3a3a4d"

THEME_FONT_FAMILY = "Segoe UI"
THEME_FONT_SIZE_NORMAL = 11
THEME_FONT_SIZE_HEADING = 16
THEME_FONT_SIZE_SUBHEADING = 13

# Hashing settings
HASH_CHUNK_SIZE = 8192

# File type settings
PDF_EXTENSION = ".pdf"

"""Utility helper functions for Smart PDF Organizer."""

import hashlib
import logging
import os
import re
from datetime import datetime
from logging.handlers import RotatingFileHandler

import config


def create_directories():
    """Create all required application directories if they do not exist."""
    for directory in config.REQUIRED_DIRECTORIES:
        os.makedirs(directory, exist_ok=True)


def format_size(size_in_bytes):
    """Convert a size in bytes to a human-readable string."""
    if size_in_bytes < 0:
        raise ValueError("size_in_bytes must not be negative")

    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = float(size_in_bytes)
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    return f"{size:.2f} {units[unit_index]}"


def format_date(timestamp, date_format="%Y-%m-%d %H:%M:%S"):
    """Convert a Unix timestamp or datetime object to a formatted string."""
    if isinstance(timestamp, datetime):
        dt_object = timestamp
    else:
        dt_object = datetime.fromtimestamp(timestamp)
    return dt_object.strftime(date_format)


def sha256_hash(file_path):
    """Compute the SHA-256 hash of a file's contents."""
    if not validate_path(file_path):
        raise FileNotFoundError(f"File does not exist: {file_path}")

    hasher = hashlib.sha256()
    with open(file_path, "rb") as file_handle:
        while True:
            chunk = file_handle.read(config.HASH_CHUNK_SIZE)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def validate_path(path):
    """Check whether the given path exists on the filesystem."""
    return bool(path) and os.path.exists(path)


def safe_filename(filename):
    """Sanitize a filename by removing unsafe or reserved characters."""
    if not filename:
        raise ValueError("filename must not be empty")

    name, extension = os.path.splitext(filename)
    sanitized_name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name)
    sanitized_name = sanitized_name.strip().strip(".")

    if not sanitized_name:
        sanitized_name = "unnamed"

    sanitized_extension = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", extension)

    return f"{sanitized_name}{sanitized_extension}"


def configure_logger(name=config.APP_NAME):
    """Configure and return a logger with console and rotating file handlers."""
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    formatter = logging.Formatter(config.LOG_FORMAT, config.LOG_DATE_FORMAT)

    os.makedirs(config.LOGS_DIR, exist_ok=True)

    file_handler = RotatingFileHandler(
        config.LOG_FILE_PATH,
        maxBytes=config.LOG_MAX_BYTES,
        backupCount=config.LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

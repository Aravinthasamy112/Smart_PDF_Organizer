"""Database access layer for Smart PDF Organizer."""

import sqlite3
from datetime import datetime

import config
import utils


class DatabaseManager:
    """Handles SQLite storage and retrieval of PDF scan history."""

    def __init__(self, database_path=None, logger=None):
        self.database_path = database_path or config.DATABASE_PATH
        self.logger = logger or utils.configure_logger()

    def _get_connection(self):
        """Reusable helper that opens a new SQLite connection."""
        return sqlite3.connect(self.database_path)

    def create_tables(self):
        """Create the scan_history table if it does not already exist."""
        query = """
            CREATE TABLE IF NOT EXISTS scan_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                page_count INTEGER,
                created_date TEXT,
                modified_date TEXT,
                scan_timestamp TEXT NOT NULL
            )
        """
        try:
            connection = self._get_connection()
            try:
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()
                self.logger.info("scan_history table verified at %s", self.database_path)
            finally:
                connection.close()
        except sqlite3.Error as error:
            self.logger.error("Failed to create tables: %s", error)

    def insert_scan(self, file_info):
        """Insert a single scanned PDF record into scan_history."""
        query = """
            INSERT INTO scan_history (
                file_name, file_path, file_size, page_count,
                created_date, modified_date, scan_timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        parameters = (
            file_info.get("name"),
            file_info.get("path"),
            file_info.get("size_bytes"),
            file_info.get("page_count"),
            file_info.get("created"),
            file_info.get("modified"),
            self._current_timestamp(),
        )

        try:
            connection = self._get_connection()
            try:
                cursor = connection.cursor()
                cursor.execute(query, parameters)
                connection.commit()
                self.logger.info("Scan record inserted for %s", file_info.get("name"))
                return cursor.lastrowid
            finally:
                connection.close()
        except sqlite3.Error as error:
            self.logger.error(
                "Failed to insert scan for %s: %s", file_info.get("name"), error
            )
            return None

    def fetch_all_scans(self):
        """Return every scan history record ordered by most recent first."""
        query = "SELECT * FROM scan_history ORDER BY scan_timestamp DESC"

        try:
            connection = self._get_connection()
            try:
                connection.row_factory = sqlite3.Row
                cursor = connection.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
            finally:
                connection.close()
        except sqlite3.Error as error:
            self.logger.error("Failed to fetch scan history: %s", error)
            return []

    def search_by_filename(self, filename):
        """Return scan history records whose file name matches the given term."""
        query = "SELECT * FROM scan_history WHERE file_name LIKE ? ORDER BY scan_timestamp DESC"
        parameters = (f"%{filename}%",)

        try:
            connection = self._get_connection()
            try:
                connection.row_factory = sqlite3.Row
                cursor = connection.cursor()
                cursor.execute(query, parameters)
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
            finally:
                connection.close()
        except sqlite3.Error as error:
            self.logger.error("Failed to search scan history for '%s': %s", filename, error)
            return []

    def clear_history(self):
        """Delete all records from scan_history. Returns True on success."""
        query = "DELETE FROM scan_history"

        try:
            connection = self._get_connection()
            try:
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()
                self.logger.info("Scan history cleared")
                return True
            finally:
                connection.close()
        except sqlite3.Error as error:
            self.logger.error("Failed to clear scan history: %s", error)
            return False

    def _current_timestamp(self):
        """Reusable helper that returns the current timestamp as a formatted string."""
        return utils.format_date(datetime.now())

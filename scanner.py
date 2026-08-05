"""PDF scanning logic for Smart PDF Organizer."""

import os

try:
    from pypdf import PdfReader
    from pypdf.errors import PdfReadError
except ImportError:  # pragma: no cover - defensive import guard
    PdfReader = None
    PdfReadError = Exception

import config
import utils


class PDFScanner:
    """Recursively scans a folder for PDF files and extracts their metadata."""

    def __init__(self, logger=None):
        self.logger = logger or utils.configure_logger()

    def scan_folder(self, folder_path):
        """Validate a folder and return metadata for every PDF file within it."""
        if not self._validate_folder(folder_path):
            self.logger.warning("Invalid folder path: %s", folder_path)
            return []

        results = []
        for file_path in self._find_pdf_files(folder_path):
            file_info = self._extract_file_info(file_path)
            if file_info is not None:
                results.append(file_info)

        self.logger.info(
            "Scan complete: %d PDF file(s) processed in %s", len(results), folder_path
        )
        return results

    def _validate_folder(self, folder_path):
        """Check that the given path is a usable, readable directory."""
        if not folder_path:
            return False
        if not utils.validate_path(folder_path):
            return False
        if not os.path.isdir(folder_path):
            return False
        if not os.access(folder_path, os.R_OK):
            return False
        return True

    def _find_pdf_files(self, folder_path):
        """Yield absolute paths for every PDF file found recursively."""
        for root, _dirs, files in os.walk(folder_path):
            for file_name in files:
                if file_name.lower().endswith(config.PDF_EXTENSION):
                    yield os.path.join(root, file_name)

    def _extract_file_info(self, file_path):
        """Build a metadata dictionary for a single PDF file, or None on failure."""
        try:
            stat_result = os.stat(file_path)
        except OSError as error:
            self.logger.error("Unable to read file stats for %s: %s", file_path, error)
            return None

        page_count = self._get_page_count(file_path)

        return {
            "name": os.path.basename(file_path),
            "path": file_path,
            "size": utils.format_size(stat_result.st_size),
            "size_bytes": stat_result.st_size,
            "page_count": page_count,
            "created": utils.format_date(stat_result.st_ctime),
            "modified": utils.format_date(stat_result.st_mtime),
        }

    def _get_page_count(self, file_path):
        """Return the page count for a PDF, or None if it cannot be determined."""
        if PdfReader is None:
            self.logger.error("pypdf is not installed; cannot read PDF contents")
            return None

        try:
            reader = PdfReader(file_path)
        except FileNotFoundError as error:
            self.logger.error("PDF file not found: %s (%s)", file_path, error)
            return None
        except PermissionError as error:
            self.logger.error("Permission denied reading %s: %s", file_path, error)
            return None
        except (PdfReadError, OSError, ValueError) as error:
            self.logger.error("Corrupted or unreadable PDF %s: %s", file_path, error)
            return None

        if reader.is_encrypted:
            decrypted = self._try_decrypt(reader, file_path)
            if not decrypted:
                self.logger.warning("Encrypted PDF could not be opened: %s", file_path)
                return None

        try:
            return len(reader.pages)
        except (PdfReadError, OSError, ValueError) as error:
            self.logger.error("Failed to count pages for %s: %s", file_path, error)
            return None

    def _try_decrypt(self, reader, file_path):
        """Attempt to decrypt a PDF using an empty password. Return success flag."""
        try:
            result = reader.decrypt("")
            return bool(result)
        except (PdfReadError, NotImplementedError, ValueError) as error:
            self.logger.error("Decryption failed for %s: %s", file_path, error)
            return False

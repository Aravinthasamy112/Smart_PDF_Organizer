"""Duplicate PDF detection logic for Smart PDF Organizer."""

from collections import defaultdict

import utils


class DuplicateFinder:
    """Detects duplicate PDF files within a scanned file list using SHA-256 hashes."""

    def __init__(self, logger=None):
        self.logger = logger or utils.configure_logger()

    def find_duplicates(self, scanned_files):
        """Identify duplicate PDFs among a list of scanned file info dictionaries.

        Args:
            scanned_files: A list of dictionaries as produced by PDFScanner,
                each expected to contain at least a "path" key.

        Returns:
            A list of dictionaries, one per group of duplicates, each with:
                - "hash": the shared SHA-256 hash
                - "count": number of files sharing that hash
                - "files": list of the original file info dictionaries
        """
        if not scanned_files:
            self.logger.info("No scanned files provided; skipping duplicate check")
            return []

        hash_groups = self._group_by_hash(scanned_files)
        duplicates = self._build_duplicate_list(hash_groups)

        self.logger.info(
            "Duplicate scan complete: %d duplicate group(s) found", len(duplicates)
        )
        return duplicates

    def _group_by_hash(self, scanned_files):
        """Reusable helper that groups file info dictionaries by SHA-256 hash."""
        hash_groups = defaultdict(list)

        for file_info in scanned_files:
            file_path = file_info.get("path")
            file_hash = self._safe_hash(file_path)
            if file_hash is not None:
                hash_groups[file_hash].append(file_info)

        return hash_groups

    def _build_duplicate_list(self, hash_groups):
        """Reusable helper that converts hash groups into the duplicate result format."""
        duplicates = []

        for file_hash, files in hash_groups.items():
            if len(files) > 1:
                duplicates.append(
                    {
                        "hash": file_hash,
                        "count": len(files),
                        "files": files,
                    }
                )

        return duplicates

    def _safe_hash(self, file_path):
        """Reusable helper that computes a file's SHA-256 hash with error handling."""
        if not file_path:
            self.logger.warning("Encountered scanned file entry without a path")
            return None

        try:
            return utils.sha256_hash(file_path)
        except FileNotFoundError as error:
            self.logger.error("File not found while hashing %s: %s", file_path, error)
        except PermissionError as error:
            self.logger.error("Permission denied while hashing %s: %s", file_path, error)
        except OSError as error:
            self.logger.error("OS error while hashing %s: %s", file_path, error)

        return None
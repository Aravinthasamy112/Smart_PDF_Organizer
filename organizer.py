"""PDF file organization logic for Smart PDF Organizer."""

import os
import shutil

import config
import utils


class PDFOrganizer:
    """Moves scanned PDF files into organized destination folders on disk."""

    DEFAULT_CATEGORY = "Uncategorized"

    def __init__(self, destination_root=None, logger=None):
        self.destination_root = destination_root or config.ORGANIZED_FILES_DIR
        self.logger = logger or utils.configure_logger()

    def organize(self, scanned_files):
        """Organize a list of scanned PDF file info dictionaries into folders.

        Args:
            scanned_files: A list of dictionaries as produced by PDFScanner,
                each expected to contain at least a "path" and "name" key.
                An optional "category" key determines the destination
                subfolder; files without one fall back to DEFAULT_CATEGORY.

        Returns:
            A summary dictionary containing:
                - "total": total number of files processed
                - "moved": number of files successfully moved
                - "skipped": number of files skipped
                - "errors": list of error detail dictionaries
        """
        summary = self._new_summary()

        if not scanned_files:
            self.logger.info("No scanned files provided; nothing to organize")
            return summary

        for file_info in scanned_files:
            summary["total"] += 1
            self._organize_single_file(file_info, summary)

        self.logger.info(
            "Organize complete: %d total, %d moved, %d skipped, %d error(s)",
            summary["total"],
            summary["moved"],
            summary["skipped"],
            len(summary["errors"]),
        )
        return summary

    def _new_summary(self):
        """Reusable helper that builds an empty summary dictionary."""
        return {"total": 0, "moved": 0, "skipped": 0, "errors": []}

    def _organize_single_file(self, file_info, summary):
        """Reusable helper that organizes one file and updates the summary."""
        source_path = file_info.get("path")
        file_name = file_info.get("name") or os.path.basename(source_path or "")

        if not source_path or not utils.validate_path(source_path):
            self.logger.warning("Skipping missing or invalid file: %s", source_path)
            summary["skipped"] += 1
            return

        category = file_info.get("category") or self.DEFAULT_CATEGORY
        destination_dir = os.path.join(self.destination_root, category)

        try:
            self._ensure_directory(destination_dir)
            destination_path = self._build_unique_destination(destination_dir, file_name)
            self._move_file(source_path, destination_path)
            summary["moved"] += 1
            self.logger.info("Moved %s to %s", source_path, destination_path)
        except OSError as error:
            self.logger.error("Failed to organize %s: %s", source_path, error)
            summary["errors"].append({"file": source_path, "error": str(error)})

    def _ensure_directory(self, directory_path):
        """Reusable helper that creates a destination folder if it does not exist."""
        os.makedirs(directory_path, exist_ok=True)

    def _build_unique_destination(self, destination_dir, file_name):
        """Reusable helper that generates a non-colliding destination file path."""
        safe_name = utils.safe_filename(file_name)
        base_name, extension = os.path.splitext(safe_name)
        candidate_path = os.path.join(destination_dir, safe_name)

        counter = 1
        while utils.validate_path(candidate_path):
            candidate_name = f"{base_name}_{counter}{extension}"
            candidate_path = os.path.join(destination_dir, candidate_name)
            counter += 1

        return candidate_path

    def _move_file(self, source_path, destination_path):
        """Reusable helper that safely moves a file using shutil."""
        shutil.move(source_path, destination_path)
"""Report generation logic for Smart PDF Organizer."""

import csv
import os
from datetime import datetime

try:
    from openpyxl import Workbook
except ImportError:  # pragma: no cover - defensive import guard
    Workbook = None

import config
import utils


class ReportGenerator:
    """Generates CSV and Excel reports summarizing scanned PDF data."""

    COLUMNS = (
        ("name", "File Name"),
        ("path", "File Path"),
        ("size", "File Size"),
        ("page_count", "Page Count"),
        ("created", "Created Date"),
        ("modified", "Modified Date"),
    )

    def __init__(self, reports_dir=None, logger=None):
        self.reports_dir = reports_dir or config.REPORTS_DIR
        self.logger = logger or utils.configure_logger()

    def export_csv(self, scanned_files, file_name=None):
        """Export scanned PDF data to a CSV report.

        Args:
            scanned_files: A list of dictionaries as produced by PDFScanner.
            file_name: Optional custom file name for the report.

        Returns:
            The full path to the generated CSV file, or None on failure.
        """
        self._ensure_reports_dir()
        report_path = self._build_report_path(file_name, "csv")

        try:
            with open(report_path, "w", newline="", encoding="utf-8") as report_file:
                writer = csv.writer(report_file)
                writer.writerow(self._column_headers())
                for row in self._build_rows(scanned_files):
                    writer.writerow(row)

            self.logger.info("CSV report generated at %s", report_path)
            return report_path
        except OSError as error:
            self.logger.error("Failed to generate CSV report: %s", error)
            return None

    def export_excel(self, scanned_files, file_name=None):
        """Export scanned PDF data to an Excel (.xlsx) report.

        Args:
            scanned_files: A list of dictionaries as produced by PDFScanner.
            file_name: Optional custom file name for the report.

        Returns:
            The full path to the generated Excel file, or None on failure.
        """
        if Workbook is None:
            self.logger.error("openpyxl is not installed; cannot generate Excel report")
            return None

        self._ensure_reports_dir()
        report_path = self._build_report_path(file_name, "xlsx")

        try:
            workbook = Workbook()
            worksheet = workbook.active
            worksheet.title = "Scan Report"
            worksheet.append(self._column_headers())

            for row in self._build_rows(scanned_files):
                worksheet.append(row)

            workbook.save(report_path)
            self.logger.info("Excel report generated at %s", report_path)
            return report_path
        except OSError as error:
            self.logger.error("Failed to generate Excel report: %s", error)
            return None

    def _ensure_reports_dir(self):
        """Reusable helper that creates the reports folder if it does not exist."""
        os.makedirs(self.reports_dir, exist_ok=True)

    def _column_headers(self):
        """Reusable helper that returns the report column header labels."""
        return [label for _key, label in self.COLUMNS]

    def _build_rows(self, scanned_files):
        """Reusable helper that converts scanned file dictionaries into report rows."""
        rows = []
        for file_info in scanned_files or []:
            rows.append([file_info.get(key) for key, _label in self.COLUMNS])
        return rows

    def _build_report_path(self, file_name, extension):
        """Reusable helper that builds a unique, safe report file path."""
        if file_name:
            base_name = utils.safe_filename(file_name)
            if not base_name.lower().endswith(f".{extension}"):
                base_name = f"{os.path.splitext(base_name)[0]}.{extension}"
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = f"scan_report_{timestamp}.{extension}"

        return os.path.join(self.reports_dir, base_name)
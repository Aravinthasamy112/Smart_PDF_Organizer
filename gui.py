"""Graphical user interface for Smart PDF Organizer."""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import config
import database
import duplicate
import organizer
import report
import scanner
import utils


class SmartPDFOrganizerGUI:
    """Builds and manages the main Tkinter/ttk interface."""

    TREE_COLUMNS = ("name", "size", "modified", "hash", "category")
    TREE_HEADINGS = {
        "name": "File Name",
        "size": "Size",
        "modified": "Date Modified",
        "hash": "SHA-256 Hash",
        "category": "Category",
    }
    TREE_COLUMN_WIDTHS = {
        "name": 260,
        "size": 100,
        "modified": 150,
        "hash": 260,
        "category": 140,
    }

    def __init__(self, root):
        self.root = root
        self.logger = utils.configure_logger()

        self.scanner = scanner.PDFScanner(logger=self.logger)
        self.database = database.DatabaseManager(logger=self.logger)
        self.duplicate_finder = duplicate.DuplicateFinder(logger=self.logger)
        self.organizer = organizer.PDFOrganizer(logger=self.logger)
        self.report_generator = report.ReportGenerator(logger=self.logger)
        self.database.create_tables()

        self.scanned_files = []
        self.file_hashes = {}

        self.selected_folder_var = tk.StringVar(value="No folder selected")
        self.search_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")
        self.progress_var = tk.DoubleVar(value=0.0)

        self._configure_root()
        self._create_menu_bar()
        self._create_toolbar()
        self._create_search_bar()
        self._create_treeview()
        self._create_progress_bar()
        self._create_status_bar()

        self.logger.info("GUI initialized")

    def _configure_root(self):
        """Apply window settings and configure the responsive grid layout."""
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.root.minsize(config.WINDOW_MIN_WIDTH, config.WINDOW_MIN_HEIGHT)
        self.root.configure(background=config.THEME_BACKGROUND)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(3, weight=1)

    def _create_menu_bar(self):
        """Build the top menu bar with File, Tools and Help menus."""
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=False)
        self._add_menu_command(file_menu, "Browse Folder", self.on_browse_folder)
        self._add_menu_command(file_menu, "Scan PDFs", self.on_scan_pdfs)
        self._add_menu_command(file_menu, "Export Report", self.on_export_report)
        file_menu.add_separator()
        self._add_menu_command(file_menu, "Exit", self.on_exit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        tools_menu = tk.Menu(menu_bar, tearoff=False)
        self._add_menu_command(tools_menu, "Find Duplicates", self.on_find_duplicates)
        self._add_menu_command(tools_menu, "Organize PDFs", self.on_organize_pdfs)
        self._add_menu_command(tools_menu, "Refresh", self.on_refresh)
        self._add_menu_command(tools_menu, "Clear", self.on_clear)
        menu_bar.add_cascade(label="Tools", menu=tools_menu)

        help_menu = tk.Menu(menu_bar, tearoff=False)
        self._add_menu_command(help_menu, "About", self.on_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menu_bar)

    def _add_menu_command(self, menu, label, command):
        """Reusable helper to add a labeled command to a menu."""
        menu.add_command(label=label, command=command)

    def _create_toolbar(self):
        """Build the toolbar row containing the primary action buttons."""
        toolbar = ttk.Frame(self.root, padding=(6, 6))
        toolbar.grid(row=0, column=0, sticky="ew")

        button_specs = (
            ("Browse Folder", self.on_browse_folder),
            ("Scan PDFs", self.on_scan_pdfs),
            ("Find Duplicates", self.on_find_duplicates),
            ("Organize PDFs", self.on_organize_pdfs),
            ("Export Report", self.on_export_report),
            ("Refresh", self.on_refresh),
            ("Clear", self.on_clear),
            ("Exit", self.on_exit),
        )

        for column_index, (label, command) in enumerate(button_specs):
            self._create_toolbar_button(toolbar, label, command, column_index)

        folder_label = ttk.Label(toolbar, textvariable=self.selected_folder_var)
        folder_label.grid(
            row=1, column=0, columnspan=len(button_specs), sticky="w", pady=(6, 0)
        )

    def _create_toolbar_button(self, parent, label, command, column_index):
        """Reusable helper to create and place a toolbar button."""
        button = ttk.Button(parent, text=label, command=command)
        button.grid(row=0, column=column_index, padx=4, pady=2, sticky="w")
        return button

    def _create_search_bar(self):
        """Build the search box row."""
        search_frame = ttk.Frame(self.root, padding=(6, 4))
        search_frame.grid(row=1, column=0, sticky="ew")
        search_frame.grid_columnconfigure(0, weight=1)

        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        search_entry.bind("<Return>", lambda event: self.on_search())

        search_button = ttk.Button(search_frame, text="Search", command=self.on_search)
        search_button.grid(row=0, column=1, sticky="e")

    def _create_treeview(self):
        """Build the Treeview with vertical and horizontal scrollbars."""
        tree_frame = ttk.Frame(self.root, padding=(6, 4))
        tree_frame.grid(row=3, column=0, sticky="nsew")
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=self.TREE_COLUMNS,
            show="headings",
            selectmode="extended",
        )

        for column in self.TREE_COLUMNS:
            self.tree.heading(column, text=self.TREE_HEADINGS[column])
            self.tree.column(
                column, width=self.TREE_COLUMN_WIDTHS[column], anchor="w"
            )

        self.tree.tag_configure("duplicate", background=config.THEME_WARNING)

        vertical_scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.tree.yview
        )
        horizontal_scrollbar = ttk.Scrollbar(
            tree_frame, orient="horizontal", command=self.tree.xview
        )
        self.tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set,
        )

        self.tree.grid(row=0, column=0, sticky="nsew")
        vertical_scrollbar.grid(row=0, column=1, sticky="ns")
        horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

    def _create_progress_bar(self):
        """Build the progress bar row."""
        progress_frame = ttk.Frame(self.root, padding=(6, 4))
        progress_frame.grid(row=4, column=0, sticky="ew")
        progress_frame.grid_columnconfigure(0, weight=1)

        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            mode="determinate",
        )
        self.progress_bar.grid(row=0, column=0, sticky="ew")

    def _create_status_bar(self):
        """Build the status bar row."""
        status_frame = ttk.Frame(self.root, padding=(6, 2), relief="sunken")
        status_frame.grid(row=5, column=0, sticky="ew")
        status_frame.grid_columnconfigure(0, weight=1)

        status_label = ttk.Label(status_frame, textvariable=self.status_var, anchor="w")
        status_label.grid(row=0, column=0, sticky="ew")

    def _set_status(self, message):
        """Reusable helper to update the status bar and log the message."""
        self.status_var.set(message)
        self.logger.info(message)

    def _show_info(self, title, message):
        """Reusable helper to display an informational message box."""
        messagebox.showinfo(title, message, parent=self.root)

    def _show_warning(self, title, message):
        """Reusable helper to display a warning message box."""
        messagebox.showwarning(title, message, parent=self.root)

    def _clear_treeview(self):
        """Reusable helper to remove all rows from the Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)

    def _populate_treeview(self, files, highlight_paths=None):
        """Reusable helper that clears and repopulates the Treeview with file data."""
        highlight_paths = highlight_paths or set()
        self._clear_treeview()

        for file_info in files:
            path = file_info.get("path")
            file_hash = self.file_hashes.get(path, "")
            values = (
                file_info.get("name", ""),
                file_info.get("size", ""),
                file_info.get("modified", ""),
                file_hash,
                file_info.get("category") or "",
            )
            tags = ("duplicate",) if path in highlight_paths else ()
            self.tree.insert("", "end", values=values, tags=tags)

    def _db_record_to_display(self, record):
        """Reusable helper that converts a scan_history DB record into display fields."""
        return {
            "name": record.get("file_name"),
            "path": record.get("file_path"),
            "size": utils.format_size(record.get("file_size") or 0),
            "modified": record.get("modified_date"),
            "category": "",
        }

    def on_browse_folder(self):
        """Handle the Browse Folder action."""
        folder_path = filedialog.askdirectory(parent=self.root)
        if not folder_path:
            self._set_status("Folder selection cancelled")
            return

        self.selected_folder_var.set(folder_path)
        self._set_status(f"Folder selected: {folder_path}")
        self._show_info("Browse Folder", f"Selected folder:\n{folder_path}")

    def on_scan_pdfs(self):
        """Handle the Scan PDFs action."""
        folder_path = self.selected_folder_var.get()
        if folder_path == "No folder selected" or not utils.validate_path(folder_path):
            self._show_warning("Scan PDFs", "Please select a valid folder first.")
            self._set_status("Scan cancelled: no folder selected")
            return

        self._set_status(f"Scanning PDFs in {folder_path}...")
        self.progress_bar.config(mode="indeterminate")
        self.progress_bar.start(10)
        self.root.update_idletasks()

        try:
            scanned_files = self.scanner.scan_folder(folder_path)
            self.scanned_files = scanned_files
            self.file_hashes = {}

            for file_info in scanned_files:
                self.database.insert_scan(file_info)

            self._populate_treeview(scanned_files)
            self._set_status(f"Scan complete: {len(scanned_files)} PDF(s) found")
            self._show_info(
                "Scan PDFs",
                f"Found {len(scanned_files)} PDF file(s) in the selected folder.",
            )
        except Exception as error:
            self.logger.error("Scan failed: %s", error)
            self._show_warning("Scan PDFs", f"An error occurred while scanning:\n{error}")
            self._set_status("Scan failed")
        finally:
            self.progress_bar.stop()
            self.progress_bar.config(mode="determinate")
            self.progress_var.set(100.0 if self.scanned_files else 0.0)

    def on_search(self):
        """Handle the Search action."""
        query = self.search_var.get().strip()
        if not query:
            self._show_warning("Search", "Please enter a search term.")
            self._set_status("Search cancelled: empty query")
            return

        self._set_status(f"Searching for: {query}")
        try:
            records = self.database.search_by_filename(query)
            display_rows = [self._db_record_to_display(record) for record in records]
            self._populate_treeview(display_rows)
            self._set_status(f"Search complete: {len(records)} result(s) for '{query}'")
            self._show_info(
                "Search", f"Found {len(records)} matching record(s) in scan history."
            )
        except Exception as error:
            self.logger.error("Search failed: %s", error)
            self._show_warning("Search", f"An error occurred while searching:\n{error}")
            self._set_status("Search failed")

    def on_find_duplicates(self):
        """Handle the Find Duplicates action."""
        if not self.scanned_files:
            self._show_warning("Find Duplicates", "Please scan a folder first.")
            self._set_status("Duplicate check cancelled: no scanned files")
            return

        self._set_status("Searching for duplicate files...")
        self.progress_var.set(50.0)
        self.root.update_idletasks()

        try:
            duplicate_groups = self.duplicate_finder.find_duplicates(self.scanned_files)
            self.file_hashes = {}
            for group in duplicate_groups:
                for file_info in group["files"]:
                    self.file_hashes[file_info.get("path")] = group["hash"]

            duplicate_paths = set(self.file_hashes.keys())
            self._populate_treeview(self.scanned_files, highlight_paths=duplicate_paths)
            self.progress_var.set(100.0)

            total_duplicates = sum(group["count"] for group in duplicate_groups)
            self._set_status(
                f"Duplicate check complete: {len(duplicate_groups)} group(s), "
                f"{total_duplicates} file(s)"
            )
            self._show_info(
                "Find Duplicates",
                f"Found {len(duplicate_groups)} duplicate group(s) "
                f"totaling {total_duplicates} file(s).",
            )
        except Exception as error:
            self.logger.error("Duplicate check failed: %s", error)
            self._show_warning("Find Duplicates", f"An error occurred:\n{error}")
            self._set_status("Duplicate check failed")
            self.progress_var.set(0.0)

    def on_organize_pdfs(self):
        """Handle the Organize PDFs action."""
        if not self.scanned_files:
            self._show_warning("Organize PDFs", "Please scan a folder first.")
            self._set_status("Organize cancelled: no scanned files")
            return

        if not messagebox.askyesno(
            "Organize PDFs",
            "This will move scanned PDF files into organized_files. Continue?",
            parent=self.root,
        ):
            self._set_status("Organize cancelled by user")
            return

        self._set_status("Organizing PDFs...")
        self.progress_var.set(50.0)
        self.root.update_idletasks()

        try:
            summary = self.organizer.organize(self.scanned_files)
            self.progress_var.set(100.0)

            self.scanned_files = []
            self.file_hashes = {}
            self._clear_treeview()

            self._set_status(
                f"Organize complete: {summary['moved']} moved, "
                f"{summary['skipped']} skipped, {len(summary['errors'])} error(s)"
            )
            self._show_info(
                "Organize PDFs",
                f"Total: {summary['total']}\nMoved: {summary['moved']}\n"
                f"Skipped: {summary['skipped']}\nErrors: {len(summary['errors'])}",
            )
        except Exception as error:
            self.logger.error("Organize failed: %s", error)
            self._show_warning("Organize PDFs", f"An error occurred:\n{error}")
            self._set_status("Organize failed")
            self.progress_var.set(0.0)

    def on_export_report(self):
        """Handle the Export Report action."""
        if not self.scanned_files:
            self._show_warning("Export Report", "Please scan a folder first.")
            self._set_status("Export cancelled: no scanned files")
            return

        export_as_excel = messagebox.askyesno(
            "Export Report",
            "Export as Excel (.xlsx)?\nChoose 'No' to export as CSV.",
            parent=self.root,
        )

        self._set_status("Exporting report...")
        try:
            if export_as_excel:
                report_path = self.report_generator.export_excel(self.scanned_files)
            else:
                report_path = self.report_generator.export_csv(self.scanned_files)

            if report_path:
                self._set_status(f"Report exported to {report_path}")
                self._show_info("Export Report", f"Report generated at:\n{report_path}")
            else:
                self._set_status("Export failed")
                self._show_warning("Export Report", "Failed to generate the report.")
        except Exception as error:
            self.logger.error("Export failed: %s", error)
            self._show_warning("Export Report", f"An error occurred:\n{error}")
            self._set_status("Export failed")

    def on_refresh(self):
        """Handle the Refresh action."""
        self._populate_treeview(self.scanned_files)
        self.progress_var.set(0.0)
        self._set_status("View refreshed")
        self._show_info("Refresh", "The file list has been refreshed.")

    def on_clear(self):
        """Handle the Clear action."""
        self._clear_treeview()
        self.search_var.set("")
        self.progress_var.set(0.0)
        self.scanned_files = []
        self.file_hashes = {}
        self._set_status("Cleared results and search field")
        self._show_info("Clear", "Results and search field have been cleared.")

    def on_about(self):
        """Handle the About action."""
        self._show_info(
            "About",
            f"{config.APP_NAME}\nVersion {config.APP_VERSION}\n{config.ORGANIZATION_NAME}",
        )

    def on_exit(self):
        """Handle the Exit action."""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=self.root):
            self.logger.info("Exiting application from GUI")
            self.root.destroy()


def main():
    """Standalone entry point for running the GUI independently."""
    utils.create_directories()
    root = tk.Tk()
    SmartPDFOrganizerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
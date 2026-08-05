"""Entry point for the Smart PDF Organizer desktop application."""

import tkinter as tk

import config
import utils
from database import DatabaseManager
from gui import SmartPDFOrganizerGUI


class SmartPDFOrganizerApp:
    """Top-level application controller responsible for startup sequencing."""

    def __init__(self):
        self.logger = utils.configure_logger()
        self.root = None
        self.gui = None

    def run(self):
        """Run the full startup sequence and launch the application window."""
        self.logger.info("Starting %s v%s", config.APP_NAME, config.APP_VERSION)

        utils.create_directories()
        self.logger.info("Application directories verified")

        database_manager = DatabaseManager(logger=self.logger)
        database_manager.create_tables()

        self.root = tk.Tk()
        self.gui = SmartPDFOrganizerGUI(self.root)
        self.logger.info("Launching main event loop")
        self.root.mainloop()

        self.logger.info("Application closed")


def main():
    """Application entry point."""
    app = SmartPDFOrganizerApp()
    app.run()


if __name__ == "__main__":
    main()
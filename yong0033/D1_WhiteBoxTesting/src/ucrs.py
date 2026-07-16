# src/ucrs.py
# pylint: disable=protected-access
"""
URCS entrypoint (mirrors teacher's bat.py pattern).
Initialises data + UI and runs the main loop.
"""

# Use whichever filename you have for the data manager.
# If your file is src/data_mgmt.py (as in your run.py), keep this:
from src.data_mgmt import DataManager

# If your file is src/data_manager.py instead, switch the import to:
# from src.data_manager import DataManager

from src.ucrs_ui import UCRSUI


class UCRS:  # pylint: disable=too-few-public-methods
    """Bootstrap URCS and run the UI loop."""
    @staticmethod
    def run():
        dm = DataManager()
        ui = UCRSUI(dm)
        while ui.get_current_screen() != "QUIT":
            ui.run_current_screen()
        # run the quit screen once (saves and exits)
        ui.run_current_screen()

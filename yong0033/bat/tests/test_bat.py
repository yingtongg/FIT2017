import unittest
from unittest.mock import patch
from src.bat import Bat

class TestBatCoverage(unittest.TestCase):

    # We patch the external dependencies required by Bat.run()
    @patch('src.bat.DataManager')
    @patch('src.bat.BatUI')
    def test_bat_run_executes_loop_and_quits(self, MockBatUI):
        """
        Covers the initialisation (DataManager, BatUI), the while loop,
        and the final run_current_screen() call (Lines 22-30).
        """
        mock_ui_instance = MockBatUI.return_value
        mock_ui_instance.get_current_screen.side_effect = ["HOME", "QUIT"]

        # --- Execution ---
        Bat.run()
        self.assertEqual(mock_ui_instance.run_current_screen.call_count, 2)
'''
Author: Charlotte Pierce

Assignment code for FIT2107 Software Quality and Testing.
Not to be shared or distributed without permission.
'''

from src.bat_ui import BatUI
from src.data_mgmt import DataManager


class Bat:  # pylint: disable=too-few-public-methods
    '''
    This class is responsible for initialising BAT data and executing
    the BAT software.
    '''
    @staticmethod
    def run():
        '''
        Run BAT.

        Creates an instance of the BAT software and a data manager with
        patron and catalogue data loaded, then runs the main BAT execution
        loop.
        '''
        data_manager = DataManager()
        user_interface = BatUI(data_manager)
        while user_interface.get_current_screen() != "QUIT":
            user_interface.run_current_screen()
        user_interface.run_current_screen()  # run the quit screen

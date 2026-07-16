# pylint: disable=protected-access
'''
Author: Charlotte Pierce

Assignment code for FIT2107 Software Quality and Testing.
Not to be shared or distributed without permission.
'''

import json
import sys

from src.patron import Patron
from src.borrowable_item import BorrowableItem
from src import config

class DataManager():
    '''
    Manages catalogue and patron data.
    '''
    def __init__(self):
        '''
        Create a new data manager, loading catalogue and patron data
        from the files specified in the software configuration.
        '''
        self._catalogue_data = None
        self.load_catalogue()
        self._patron_data = None
        self.load_patrons()

    def register_patron(self, patron_name, patron_age):
        '''
        Register a new patron.
        It is assumed that the name and age combination is unique with
        respect to any existing data.
        The patron is assigned a unique ID, and initialised with zero loans
        and no training completed.
            Args:
                patron_name (string): the patron's name.
                patron_age (int): the patron's age in years.
        '''
        next_id = max(self._patron_data, key=lambda p: p._id)._id + 1

        new_patron = Patron()
        new_patron.set_new_patron_data(next_id, patron_name, patron_age)

        self._patron_data.append(new_patron)

    def load_patrons(self):
        '''
        Load patron data from the file specified in config.
        If there is an error loading the data, print an error message
        and crash the program.
        '''
        try:
            with open(config.PATRON_DATA, 'r', encoding='utf-8') as file_:
                data = json.load(file_)

            patrons = []
            for record in data:
                new_patron = Patron()
                new_patron.load_data(record, self._catalogue_data)
                patrons.append(new_patron)

            self._patron_data = patrons
        except (OSError, json.JSONDecodeError):
            print("ERROR LOADING PATRON DATA: EXITING.")
            sys.exit()

    def save_patrons(self):
        '''
        Save patron data to the file specified in config.
        Overrites any existing data.
        '''
        with open(config.PATRON_DATA, 'w', encoding='utf-8') as file_:
            file_.write("[")
            for patron_obj in self._patron_data:
                file_.write(json.dumps(patron_obj, cls=self.PatronEncoder))
                if patron_obj != self._patron_data[-1]:
                    file_.write(",")
            file_.write("]")

    def load_catalogue(self):
        '''
        Load catalogue data from the file specified in config.
        If there is an error loading the data, print an error message
        and crash the program.
        '''
        try:
            with open(config.CATALOGUE_DATA, 'r', encoding='utf-8') as file_:
                data = json.load(file_)

            items = []
            for record in data:
                new_item = BorrowableItem()
                new_item.load_data(record)
                items.append(new_item)

            self._catalogue_data = items
        except (OSError, json.JSONDecodeError):
            print("ERROR LOADING CATALOGUE DATA: EXITING.")
            sys.exit()

    def save_catalogue(self):
        '''
        Save catalogue data to the file specified in config.
        Overrites any existing data.
        '''
        with open(config.CATALOGUE_DATA, 'w', encoding='utf-8') as file_:
            file_.write("[")
            for record in self._catalogue_data:
                file_.write(json.dumps(record, cls=self.BorrowableItemEncoder))
                if record != self._catalogue_data[-1]:
                    file_.write(",")
            file_.write("]")

    class PatronEncoder(json.JSONEncoder):
        '''
        Translates instances of the Patron class to JSON for
        saving to file.
        '''
        def default(self, o):
            if isinstance(o, Patron):
                return {
                    "patron_id": o._id,
                    "name": o._name,
                    "age": o._age,
                    "outstanding_fees": o._outstanding_fees,
                    "gardening_tool_training": o._gardening_tool_training,
                    "carpentry_tool_training": o._carpentry_tool_training,
                    "makerspace_training": o._makerspace_training,
                    "loans" :
                    [{"item": l._item._id,"due":
                      l._due_date.strftime('%d/%m/%Y')} for l in o._loans]
                }
            return super().default(o)

    class BorrowableItemEncoder(json.JSONEncoder):
        '''
        Translates instances of the BorrowableItem class to JSON for
        saving to file.
        '''
        def default(self, o):
            if isinstance(o, BorrowableItem):
                return {
                    "item_id": o._id,
                    "item_name": o._name,
                    "item_type": o._type,
                    "year": o._year,
                    "number_owned": o._number_owned,
                    "on_loan": o._on_loan,
                }
            return super().default(o)

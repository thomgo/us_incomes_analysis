import pandas as pd
import re
import matplotlib
import matplotlib.pyplot as plt

from data.geographical_information import states_location


class DataManipulator():
    """Make all operation on the application data
    All the views logic to be lighhter"""

    data_file = "data/median_income_data.csv"

    def __init__(self):
        pass

    @classmethod
    def generate_improved_data(cls):
        """read data, call methods to keep only numbers,
        add information about location, inequalities and save the file """
        data = pd.read_csv(DataManipulator.data_file, decimal=",")
        # Rename columns with shorter names
        data.columns = ["state", "white", "error1", "black", "error2", "indian", "error3", "asian", "error4", "pacific", "error5", "other", "error6", "two_or_more_races", "error7" ]
        data = cls.keep_numbers_only(data)

        # Keep only data related to incomes by race
        races_values = data[["white", "asian", "black", "indian", "pacific", "other", "two_or_more_races"]]
        # Add column with richest race and highest income for each state
        data["richest_race"] = races_values.idxmax(axis=1)
        data["richest"] = races_values.max(axis=1)
        # Add column with poorest race and lowest income for each state
        data["poorest_race"] = races_values.idxmin(axis=1)
        data["poorest"] = races_values.min(axis=1)
        # Add column with diffeence beetwen highest and lowest income
        data["difference"] = data["richest"] - data["poorest"]

        # Add column with each state location in the US
        # For location see geographical_information
        location = []
        for state in data["state"]:
            if state in states_location["northern"]:
                location.append("northern")
            elif state in states_location["southern"]:
                location.append("southern")
            else:
                location.append("western")
        data["location"] = location

        # Save the improved data as a csv file
        data.to_csv(path_or_buf="data/final_income_data.csv", index=False)

    @staticmethod
    def keep_numbers_only(data):
        """Clean strings and turn all data in pure integers"""
        for column in data.columns[1:]:
            column_values = list(data[column])
            for index, value in enumerate(column_values):
                # Keep only integer value from the string
                try:
                    value = int(re.sub('[^0-9]', "", value))
                    column_values[index] = value
                except ValueError:
                    column_values[index] = None
            data[column] = column_values
        return data

    # @staticmethod
    # def keep_numbers_only(cls):
    #     pass
    #
    # @staticmethod
    # def keep_numbers_only(cls):
    #     pass

import pandas as pd
import re
import matplotlib
import matplotlib.pyplot as plt

from os import path
from flask import Flask
from flask import render_template
from data.geographical_information import states_location
from service.data_manipulator import DataManipulator as dm

app = Flask(__name__)
# Avoid runtime and threading errors because not displaying the charts
matplotlib.use('Agg')

@app.route('/')
def index():
    """Display improved data as HTML table if data available
    If not, read base data, improve it and save it as final_income_data.csv"""
    if path.exists("data/final_income_data.csv"):
        data = pd.read_csv("data/final_income_data.csv", decimal=",")
    else:
        data = pd.read_csv("data/median_income_data.csv", decimal=",")
        # Rename columns with shorter names
        data.columns = ["state", "white", "error1", "black", "error2", "indian", "error3", "asian", "error4", "pacific", "error5", "other", "error6", "two_or_more_races", "error7" ]

        # Clean strings and turn all data in pure integers
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

    # Produce an html table to be displayed in the template
    data = data.to_html(classes=["table", "table-striped", "table-bordered", "table-responsive"])
    return render_template("index.html", data_table=data)

@app.route('/analysis')
def analysis():
    """Create and save as images all the figures needed for the analysis"""
    if path.exists("data/final_income_data.csv"):
        data = pd.read_csv("data/final_income_data.csv", decimal=",")
        # Piechart with frequence of races in % in richest_race column
        data["richest_race"].value_counts(normalize=True).plot(kind='pie', autopct='%1.1f%%', title="Races with highest income")
        plt.savefig(fname="static/images/distri_richest_race")
        plt.close()
        # Piechart with frequence of races in % in poorest_race column
        data["poorest_race"].value_counts(normalize=True).plot(kind='pie', autopct='%1.1f%%', title="races with lowest income")
        plt.savefig(fname="static/images/distri_poorest_race")
        plt.close()

        # Keep only the incomes by race
        subset = data[["white", "asian", "black", "indian", "pacific", "other", "two_or_more_races"]]
        # Turn pacific column to float, if not mean and median does not work
        subset["pacific"] = subset["pacific"].astype(float)
        # Create one histogram by race for incomes
        for label, column in subset.iteritems():
            mean = int(round(column.mean(skipna=True)))
            median = int(round(column.median(skipna=True)))
            title = "Histrogram of {} incomes".format(label)
            text = "mean : {}  median : {}".format(mean, median)
            fname = "static/images/hist_{}".format(label)
            column.plot(kind='hist', title=title)
            plt.figtext(x=0.2, y=0.01, s=text)
            plt.savefig(fname=fname)
            plt.close()

    return render_template("analysis.html")

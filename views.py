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
    if not path.exists("data/final_income_data.csv"):
        dm.generate_improved_data()
    data = pd.read_csv("data/final_income_data.csv", decimal=",")
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

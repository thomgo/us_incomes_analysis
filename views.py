import pandas as pd

from os import path
from flask import Flask
from flask import render_template
from service.data_manipulator import DataManipulator as dm
from service.figure_generator import FigureGenerator as fg

app = Flask(__name__)


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
    if not path.exists("data/final_income_data.csv"):
        dm.generate_improved_data()
    fg.generate_richest_poorest_chart_by_race()
    fg.generate_incomes_hist_by_race()

    return render_template("analysis.html")

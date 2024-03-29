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
    contengency_tab = fg.generate_incomes_by_race_state_tab()
    poorest_tab, khi2_poorest = fg.generate_poorest_race_by_location_tabs()
    richest_tab, khi2_richest = fg.generate_richest_race_by_location_tabs()
    fg.generate_difference_boxplot()
    fg.generate_error_scatterplot()
    return render_template(
        "analysis.html",
        contengency_tab=contengency_tab,
        poorest_tab=poorest_tab,
        khi2_poorest=khi2_poorest,
        richest_tab=richest_tab,
        khi2_richest=khi2_richest
    )

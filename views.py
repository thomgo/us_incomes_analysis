from os import path

import pandas as pd
import re

from flask import Flask
from flask import render_template

from data.geographical_information import states_location

app = Flask(__name__)

@app.route('/')
def index():
    if path.exists("data/final_income_data.csv"):
        data = pd.read_csv("data/final_income_data.csv", decimal=",")
    else:
        data = pd.read_csv("data/median_income_data.csv", decimal=",")
        # Rename columns with shorter names
        columns = ["state", "white", "error1", "black", "error2", "indian", "error3", "asian", "error4", "pacific", "error5", "other", "error6", "two_or_more_races", "error7" ]
        data.columns = columns

        #Turn all data in pure integers
        for column in columns:
            if column != "state":
                test = list(data[column])
                for index, value in enumerate(test):
                    value = re.sub('[^0-9]', "", value)
                    try:
                        value = int(value)
                        test[index] = value
                    except Exception as e:
                        test[index] = None
                data[column] = test

        # Add data about richest and poorest race and difference between poorest and richest
        races_values = data[["white", "asian", "black", "indian", "pacific", "other", "two_or_more_races"]]
        data["richest_race"] = races_values.idxmax(axis=1)
        data["richest"] = races_values.max(axis=1)
        data["poorest_race"] = races_values.idxmin(axis=1)
        data["poorest"] = races_values.min(axis=1)
        data["difference"] = data["richest"] - data["poorest"]

        # Add géographical data about where the state is located in the US
        location = []
        for state in data["state"]:
            if state in states_location["northern"]:
                location.append("northern")
            elif state in states_location["southern"]:
                location.append("southern")
            else:
                location.append("western")
        data["location"] = location
        data.to_csv(path_or_buf="data/final_income_data.csv", index=False)

    return render_template("index.html", data_table=data.to_html(classes=["table", "table-striped", "table-bordered", "table-responsive"]), border="None")

@app.route('/analysis')
def analysis():
    return render_template("analysis.html")

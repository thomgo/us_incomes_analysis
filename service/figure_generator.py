import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# Avoid runtime and threading errors because not displaying the charts
matplotlib.use('Agg')


class FigureGenerator():
    """Produce figures needed for analysis"""

    data = pd.read_csv("data/final_income_data.csv", decimal=",")

    def __init__(self):
        pass

    @classmethod
    def generate_richest_poorest_chart_by_race(cls):
        """Generate pie chart to show frequency in percentage
        of races beeing richest or poorest"""
        # Piechart with frequence of races in % in richest_race column
        cls.data["richest_race"].value_counts(normalize=True).plot(kind='pie', autopct='%1.1f%%', title="Races with highest income")
        plt.savefig(fname="static/images/distri_richest_race")
        plt.close()
        # Piechart with frequence of races in % in poorest_race column
        cls.data["poorest_race"].value_counts(normalize=True).plot(kind='pie', autopct='%1.1f%%', title="races with lowest income")
        plt.savefig(fname="static/images/distri_poorest_race")
        plt.close()

    @classmethod
    def generate_incomes_hist_by_race(cls):
        """Generate histograms to show distribution of median incomes
        for each race with global mean and median in description"""
        # Keep only the incomes by race
        subset = cls.data[["white", "asian", "black", "indian", "pacific", "other", "two_or_more_races"]]
        # Turn pacific column to float, if not mean and median does not work
        subset["pacific"] = subset["pacific"].astype(float)
        # Create one histogram by race for incomes
        for label, column in subset.iteritems():
            mean = int(round(column.mean(skipna=True)))
            median = int(round(column.median(skipna=True)))
            std = int(round(column.std()))
            cv = round(std/mean, 2)
            skew = round(column.skew(), 2)
            title = "Histrogram of {} incomes".format(label)
            text = "mean : {}  median : {}  std : {}  cv = {}  skew = {}".format(mean, median, std, cv, skew)
            fname = "static/images/hist_{}".format(label)
            column.plot(kind='hist', title=title, xticks=range(0,140000, 20000), yticks=range(0, 28, 2))
            plt.figtext(x=0.1, y=0.01, s=text)
            plt.savefig(fname=fname)
            plt.close()

    @classmethod
    def generate_contengency_tab(cls):
        """Generate an html contengency table to check for correlation
        between race median incomes and the state location in the US"""
        tab = pd.DataFrame(columns=["southern", "northern", "western"], index=["white", "asian", "black", "indian", "other"])
        for index, values in tab.iterrows():
            subset = cls.data[[index, "location"]]
            southern = subset[subset["location"] == "southern"]
            northern = subset[subset["location"] == "northern"]
            western = subset[subset["location"] == "western"]
            tab["southern"][index] = round(southern[index].median())
            tab["northern"][index] = round(northern[index].median())
            tab["western"][index] = round(western[index].median())
        return tab.to_html(classes=["table", "table-striped", "table-bordered", "text-center"])

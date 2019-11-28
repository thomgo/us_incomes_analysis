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
        subset = cls.data[["white", "asian", "black", "indian", "other"]]
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
    def generate_incomes_by_race_state_tab(cls):
        """Generate an html contengency table to check for correlation
        between race median incomes and the state location in the US"""
        # Create an empty dataframe with races and possible locations
        tab = pd.DataFrame(columns=["southern", "northern", "western"], index=["white", "asian", "black", "indian", "other"])
        # Iterate through rows
        for index, values in tab.iterrows():
            # Keep only income of specific race and location
            subset = cls.data[[index, "location"]]
            # Separate data bewteen the three possible locations
            southern = subset[subset["location"] == "southern"]
            northern = subset[subset["location"] == "northern"]
            western = subset[subset["location"] == "western"]
            # For each location add the race median of median incomes
            tab["southern"][index] = round(southern[index].median())
            tab["northern"][index] = round(northern[index].median())
            tab["western"][index] = round(western[index].median())
        return tab.to_html(classes=["table", "table-striped", "table-bordered", "text-center"])

    @classmethod
    def generate_poorest_race_by_location_tabs(cls):
        """Analysis of the correlation bewteen poorest race and state location
        with the Khi2 method. Returns two html tables"""
        # Create an empty contengency table
        poorest_tab = pd.DataFrame(columns=["white", "asian", "black", "indian", "other", "total"], index=["southern", "northern", "western", "total"])
        subset = cls.data[["poorest_race", "location"]]
        for index, values in poorest_tab.iterrows():
            # Keep data of a certain location
            location_data = subset[subset["location"] == index]
            # Count the occurences of poorest races for this location
            data = location_data["poorest_race"].value_counts()
            # Replace the data at the location by the generated serie
            poorest_tab.loc[index] = data
        # Count the total horizontaly and verticaly
        poorest_tab.loc["total"] = poorest_tab.sum(axis=0)
        poorest_tab["total"] = poorest_tab.sum(axis=1)
        poorest_tab = poorest_tab.fillna(0)
        # Start a new dataframe with what the repartition should be
        khi2_poorest = poorest_tab.copy()
        for label, values in khi2_poorest.iteritems():
            # Get the frequence of each race as poorest amoung all the states
            rate = khi2_poorest[label]["total"]/khi2_poorest["total"]["total"]
            # Replace race values by a list with values based on the rate
            khi2_poorest[label] = [round(x*rate) for x in khi2_poorest["total"]]
        poorest_tab = poorest_tab.to_html(classes=["table", "table-striped", "table-bordered", "text-center"])
        khi2_poorest = khi2_poorest.to_html(classes=["table", "table-striped", "table-bordered", "text-center"])
        return poorest_tab, khi2_poorest

    @classmethod
    def generate_richest_race_by_location_tabs(cls):
        """Analysis of the correlation bewteen richest race and state location
        with the Khi2 method. Returns two html tables"""
        richest_tab = pd.DataFrame(columns=["white", "asian", "black", "indian", "other", "total"], index=["southern", "northern", "western", "total"])
        subset = cls.data[["richest_race", "location"]]
        for index, values in richest_tab.iterrows():
            location_data = subset[subset["location"] == index]
            data = location_data["richest_race"].value_counts()
            richest_tab.loc[index] = data
        richest_tab.loc["total"] = richest_tab.sum(axis=0)
        richest_tab["total"] = richest_tab.sum(axis=1)
        richest_tab = richest_tab.fillna(0)
        khi2_richest = richest_tab.copy()
        for label, values in khi2_richest.iteritems():
            rate = khi2_richest[label]["total"]/khi2_richest["total"]["total"]
            khi2_richest[label] = [round(x*rate) for x in khi2_richest["total"]]
        richest_tab = richest_tab.to_html(classes=["table", "table-striped", "table-bordered", "text-center"])
        khi2_richest = khi2_richest.to_html(classes=["table", "table-striped", "table-bordered", "text-center"])
        return richest_tab, khi2_richest

    @classmethod
    def generate_difference_boxplot(cls):
        """Generate boxplots showings the distribution of differences bewteen
        richest and poorest for each group of states"""
        result = []
        subset = cls.data[["difference", "location"]]
        # Loop through the possible location (southern, northern, western)
        for location in subset["location"].unique():
            # Keep only data of a specific location
            data = subset[subset["location"] == location]
            # Add the differences serie to the result tab and produce the box plot
            result.append(data["difference"])
        plt.boxplot(result, labels=subset["location"].unique(), showfliers=False, vert=False, patch_artist=True, showmeans=True )
        plt.savefig(fname="static/images/boxplot_diff")
        plt.close()

    @classmethod
    def generate_error_scatterplot(cls):
        """Generate a scatter plot for all the incomes and margin of error"""
        plt.plot(cls.data[["white", "asian", "black", "indian", "other"]],cls.data[["error1", "error2", "error3", "error4", "error6"]],"o",alpha=0.5)
        plt.xlabel("income")
        plt.ylabel("margin of error")
        plt.savefig(fname="static/images/scatterplot_error")
        plt.close()

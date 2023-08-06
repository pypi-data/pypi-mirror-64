# -*- coding: utf-8 -*-
"""Provide datastructures to handel single movies as well as databases.
"""
import csv
import time
from operator import itemgetter

import matplotlib.pyplot as plt
from matplotlib.dates import (DateFormatter, datestr2num)
import numpy as np


__all__ = [
    'Movie',
    'MovieDatabase',
]


class Movie:
    def __init__(self, title, date=None):
        self.title = title
        self.date = date

    def __repr__(self):
        return "'{title}'".format(title=self.title)

    def __lt__(self, other):
        # Compare Movie object using their numerical date representation.
        return self.datenum < other.datenum

    def __eq__(self, other):
        # Movie objects are equal when title **and** date agree.
        return self.title == other.title and self.date == other.date

    def __hash__(self):
        """Override the default hash behavior."""
        return hash(tuple((self.title, self.date)))

    @property
    def datenum(self):
        """Return datenum representation of date."""
        return datestr2num(self.date) if self.date is not None else None


class MovieDatabase(list):
    @classmethod
    def from_csv(cls, filename):
        """Load a movie database from CSV file.

        Note:
            If the movie title contains a comma, the title has to be quoted:
                2016-02-05,"Hail, Caesar!"

        Parameters:
            filename (str): Path to CSV file.
        """
        with open(filename, 'r') as csvfile:
            # Parse the CSV file into a dictionary (column names as keys).
            reader = csv.DictReader(csvfile)
            # Create Movie object from every entry in the CSV reader.
            movie_list = [Movie(title=line['movie'], date=line['date'])
                          for line in reader]

        # Return actual MovieDatabase.
        return cls(movie_list)

    def to_csv(self, filename, fields=('date', 'title')):
        """Write a movie database to CSV file.

        Parameters:
            filename (str): Path to CSV file.
            fields (seq): Names of fields to store (default is date and title).
        """
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile, quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)

            writer.writerow(fields)
            for movie in self:
                writer.writerow([getattr(movie, field) for field in fields])

    def get_datenumlim(self):
        """Return the start and end date of the database as datenum.

        Returns:
            float, float: Start date, end date
        """
        # Get the first and last movie of the list sorted by date.
        firstlast = itemgetter(0, -1)(sorted(self))

        # Return the datenum representation of both movies.
        return tuple(map(lambda m: m.datenum, firstlast))

    def get_polyfit(self, deg=1):
        """Perform a polynomial regression.

        Parameters:
            deg (int): Degree of the fitting polynomial.

        Returns:
            ndarray: Polynomial coefficients, highest power first.
        """
        # Create dummy array with the cumulative number of movies watched.
        number_of_films = np.arange(len(self))

        # Create array containing the datenum representation of dates.
        datenums = np.array([m.datenum for m in sorted(self)])

        # Perform a polynomial fit of number of movies against time.
        return np.polyfit(datenums, number_of_films, deg)

    def remove_duplicates(self):
        """Remove duplicates from database."""
        super().__init__(set(self))

    def plot_trend(self, end_date=None, num=50, deg=1, ax=None, **kwargs):
        """Plot the linear trend of movies watched against time.

        Parameters:
            end_date (str): End date for extrapolation (default end of year).
            num (int): Number of sampling points.
            deg (int): Degree of the fitting polynomial.
            ax (plt.AxesSubplot): Axes to plot in.
            **kwargs: Additional keyword arguments are collected
                and passed to `plt.plot`.

        Returns:
            list[Line2D]: List of lines added.
        """
        # If no matplotlib axes is passed, get the latest.
        if ax is None:
            ax = plt.gca()

        # Create an time array within the start and end date of the database.
        start_date = self.get_datenumlim()[0]
        if end_date is None:
            # If no end date is given, extrapolate to end of the year.
            end_date = '{}-12-31'.format(time.strftime('%Y'))
        x = np.linspace(start_date, datestr2num(end_date), num)

        # Perform polynomial regression and calculate values to plot.
        y = np.polyval(self.get_polyfit(deg=deg), x)

        return ax.plot(x, y, **kwargs)

    def plot_titles(self, ax=None, **kwargs):
        """Plot number of movies seen against date.

        Parameters:
            ax (plt.AxesSubplot): Axes to plot in.
            **kwargs: Additional keyword arguments are collected
                and passed to `plt.annotate`.
        """
        # If no matplotlib axes is passed, get the latest.
        if ax is None:
            ax = plt.gca()

        # Loop over all movies in the sorted database and ...
        for n, movie in enumerate(sorted(self), 1):
            # ... print their title against their position in the database.
            ax.annotate(' ' + movie.title, xy=(movie.datenum, n), **kwargs)

        # Date formatting for the x-axis.
        ax.xaxis.set_major_formatter(DateFormatter("%b"))

        # Axes limits have to be set as `plt.annotate` does not to this!
        ax.set_xbound(self.get_datenumlim())
        ax.set_ybound(lower=0)

    def plot_marker(self, marker='o', ax=None, **kwargs):
        """Plot number of movies seen against date.

        Parameters:
            ax (plt.AxesSubplot): Axes to plot in.
            marker (str): Marker to represent movies.
            **kwargs: Additional keyword arguments are collected
                and passed to `plt.plot`.
        """
        # If no matplotlib axes is passed, get the latest.
        if ax is None:
            ax = plt.gca()

        # Create dummy array with the cumulative number of movies watched.
        number_of_films = np.arange(len(self))

        # Create array containing the datenum representation of dates.
        datenums = np.array([m.datenum for m in sorted(self)])

        # Plot
        ret = ax.plot(datenums, number_of_films,
                      linestyle='none',
                      marker=marker,
                      **kwargs)

        # Date formatting for the x-axis.
        ax.xaxis.set_major_formatter(DateFormatter("%b"))

        # Axes limits have to be set as `plt.annotate` does not to this!
        ax.set_xbound(self.get_datenumlim())
        ax.set_ybound(lower=0)

        return ret

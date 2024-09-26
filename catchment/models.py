"""Module containing models representing catchment data.

The Model layer is responsible for the 'business logic' part of the software.

Catchment data is held in a Pandas dataframe (2D array) where each column contains
data for a single measurement site, and each row represents a single measurement
time across all sites.
"""

import pandas as pd

def read_variable_from_csv(filename):
    """Reads a named variable from a CSV file, and returns a
    pandas dataframe containing that variable. The CSV file must contain
    a column of dates, a column of site ID's, and (one or more) columns
    of data - only one of which will be read.

    :param filename: Filename of CSV to load
    :return: 2D array of given variable. Index will be dates,
             Columns will be the individual sites
    """
    dataset = pd.read_csv(filename, usecols=['Date', 'Site', 'Rainfall (mm)'])

    dataset = dataset.rename({'Date':'OldDate'}, axis='columns')
    dataset['Date'] = [pd.to_datetime(x,dayfirst=True) for x in dataset['OldDate']]
    dataset = dataset.drop('OldDate', axis='columns')

    newdataset = pd.DataFrame(index=dataset['Date'].unique())

    for site in dataset['Site'].unique():
        newdataset[site] = dataset[dataset['Site'] == site].set_index('Date')["Rainfall (mm)"]

    newdataset = newdataset.sort_index()

    return newdataset

def daily_total(data):
    """Calculate the daily total of a 2D data array.
    Index must be np.datetime64 compatible format."""
    return data.groupby(data.index.date).sum()

def daily_mean(data):
    """Calculate the daily mean of a 2d data array.
    Index must be np.datetime64 compatible format."""
    return data.groupby(data.index.date).mean()


def daily_max(data):
    """Calculate the daily max of a 2D data array.
    Index must be np.datetime64 compatible format."""
    return data.groupby(data.index.date).max()


def daily_min(data):
    """Calculate the daily min of a 2D data array.
    Index must be np.datetime64 compatible format."""
    return data.groupby(data.index.date).min()


def daily_count(data):
    """Calculate the daily count of a 2D data array.
    Index must be np.datetime64 compatible format."""
    return data.groupby(data.index.date).count()


def data_above_threshold(site_id, data, threshold):
    """ Determine if data measurement values for a
    given site exceed a given threshold.

    :param site_id: string indicating chosen Site ID
    :param data: pandas DataFrame containing measurements
    :param threshold: measurement threshold
    :return: list of booleans
    """
    return list(map(lambda x: x > threshold, data[site_id]))


class MeasurementSeries:
    def __init__(self, series, name, units):
        self.series = series
        self.name = name
        self.units = units
        self.series.name = self.name

    def add_measurement(self, data):
        self.series = pd.concat([self.series, data])
        self.series.name = self.name

    def __str__(self):
        if self.units:
            return f"{self.name} ({self.units})"
        else:
            return self.name


class Location:
    """A Location."""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Site(Location):
    """A measurement site in the study."""
    def __init__(self, name, longitude = None, latitude = None):
        super().__init__(name)
        self.measurements = {}
        if longitude and latitude:
            self.location = gpd.GeoDataFrame(
                            geometry = gpd.points_from_xy([longitude], [latitude], crs='EPSG:4326')
                            )

        else:
            self.location = gpd.GeoDataFrame()

    def add_measurement(self, measurement_id, data, units=None):
        if measurement_id in self.measurements.keys():
            self.measurements[measurement_id].add_measurement(data)

        else:
            self.measurements[measurement_id] = MeasurementSeries(data, measurement_id, units)

    @property
    def all_measurements(self):
        return pd.concat(
            [self.measurements[key].series for key in self.measurements.keys()],
            axis=1)


class Catchment(Location):
    """A catchment area in the study."""
    def __init__(self, name, shapefile = None):
        super().__init__(name)
        self.sites = {}
        if shapefile:
            self.area = gpd.GeoDataFrame.from_file(shapefile)
        else:
            self.area = gpd.GeoDataFrame()


    def add_site(self, new_site):
        # Check to ensure site is within catchment, if both the catchment area 
        # and the location have been defined 
        if self.area.size and new_site.location.size and not sjoin(new_site.location,self.area).size:
            print(f'{new_site.name} not within {self.name} catchment')
            return

        # Basic check to see if the site has already been added to the catchment area 
        for site in self.sites:
            if site == new_site.name:
                print(f'{new_site.name} has already been added to site list')
                return

        self.sites[new_site.name] = new_site

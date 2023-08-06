# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 10:45:18 2020

@author: mathias
"""

import datetime as dt
import pandas as pd


def import_ebase_csv_convert_datetime(filename, utc_in=False, utc_out=False):
    """
    Imports a file that is being exported from eBase. By default, the first column is the date, the second column the
    time (eBase default). This function combines them, and depending on the arguments, converrts it to the relevant
    timezone
    :param filename: filename to import
    :param utc_in: bool to denote if the input is in UTC. Otherwise in Europe/Amsterdam
    :param utc_out: bool to denote if the output is in UTC. Otherwise in Europe/Amsterdam
    :return: dataframe with a column datetime
    """
    df = pd.read_csv(filename)
    date_column = df.columns[0]
    time_column = df.columns[1]

    # These are eBase defaults
    df[date_column] = pd.to_datetime(df[date_column], format='%d-%m-%Y')
    df[time_column] = pd.to_datetime(df[time_column], format='%H:%M').dt.time

    # By default, use Europe/Amsterdam
    timezone_in = 'UTC' if utc_in else 'Europe/Amsterdam'
    timezone_out = 'UTC' if utc_in else 'Europe/Amsterdam'

    # combine the date and the time to a datetime. Localize it to the right timezone, and convert it.
    df['datetime'] = df.apply(lambda x: dt.datetime.combine(x[date_column],
                                                                  x[time_column]),
            axis=1).dt.tz_localize(timezone_in).dt.tz_convert(timezone_out)

    # Drop the date and time columns. If you need it later on, you have the datetime set as index
    try:
        df.drop(columns=[date_column, time_column])
    except TypeError:
        # Above statement requries pandas >= 0.21
        df = df.loc[:, [col for col in df.columns if col not in [date_column, time_column]]]
    return df.set_index('datetime')

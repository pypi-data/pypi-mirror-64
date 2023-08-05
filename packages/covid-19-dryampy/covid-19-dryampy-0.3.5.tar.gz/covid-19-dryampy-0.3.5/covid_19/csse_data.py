import pandas as pd
import numpy as np

class csse_retrieve:

    def __init__(self):

        self.url_ts_conf = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
        self.url_ts_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
        self.url_ts_reco = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'

    def fetch(self):

        df_conf = pd.read_csv(self.url_ts_conf, error_bad_lines=False)
        df_conf['metric'] = 'confirmed_cases'
        df_deaths = pd.read_csv(self.url_ts_deaths, error_bad_lines=False)
        df_deaths['metric'] = 'deaths'
        df_reco = pd.read_csv(self.url_ts_reco, error_bad_lines=False)
        df_reco['metric'] = 'recoveries'

        # Establish Dimension tables
        dim_metric = pd.DataFrame({'metric_id': [0, 1, 2], 'metric': ['confirmed_cases', 'deaths', 'recoveries']})
        dim_location = df_conf[['Country/Region', 'Province/State', 'Lat', 'Long']].reset_index().rename(columns={'index': 'loc_id'})

        # location merge criteria
        loc_joins = ['Country/Region', 'Province/State', 'Lat', 'Long']

        # key confirmed cases
        df_conf = pd.merge(
            df_conf,
            dim_location,
            on=loc_joins
        )
        df_conf = pd.merge(
            df_conf,
            dim_metric,
            on='metric'
        )

        # drop old columns
        df_conf = df_conf.drop(loc_joins, axis = 1)
        df_conf = df_conf.drop(['metric'], axis = 1)
        df_conf = df_conf.melt(id_vars=['loc_id', 'metric_id'], var_name='date', value_name='counts')

        # key death cases
        df_deaths = pd.merge(
            df_deaths,
            dim_location,
            on=loc_joins
        )
        df_deaths = pd.merge(
            df_deaths,
            dim_metric,
            on='metric'
        )

        # drop old columns
        df_deaths = df_deaths.drop(loc_joins, axis = 1)
        df_deaths = df_deaths.drop(['metric'], axis = 1)
        df_deaths = df_deaths.melt(id_vars=['loc_id', 'metric_id'], var_name='date', value_name='counts')

        # key recovered cases
        df_reco = pd.merge(
            df_reco,
            dim_location,
            on=loc_joins
        )
        df_reco = pd.merge(
            df_reco,
            dim_metric,
            on='metric'
        )

        # drop old columns
        df_reco = df_reco.drop(loc_joins, axis = 1)
        df_reco = df_reco.drop(['metric'], axis = 1)
        df_reco = df_reco.melt(id_vars=['loc_id', 'metric_id'], var_name='date', value_name='counts')

        self.final = pd.concat([df_deaths, df_conf, df_reco])
        self.dim_location = dim_location
        self.dim_metric = dim_metric

        return [self.final, self.dim_location, self.dim_metric]
from datetime import date, timedelta
import pandas
import urllib.request

class hopkins_timeseries:
    def __init__(self, states, regions, timeseries):
        self.__states = states
        self.__regions = regions
        self.__timeseries = timeseries
    
    def get(self):
        return self.__timeseries
        
    def __aggregate_regions_by_sum(self, names):
        aggregated_timeseries = pandas.DataFrame()
        for name in names:
            states_from_region = self.__get_states_from_region(name)
            if 0 < len(states_from_region):
                aggregated_timeseries[name] = self.__timeseries[states_from_region].sum(axis=1)                
            elif name in self.__timeseries.columns:
                aggregated_timeseries[name] = self.__timeseries[name]
        return aggregated_timeseries
        
    def __get_states_from_region(self, name):
        states = []
        region_indices = [index for index in range(0, len(self.__regions)) if name == self.__regions[index]]
        for region_index in region_indices:
            state = self.__states[region_index]
            if pandas.notna(state):
                states.append(state)
        return states
    
    def __get_states(self, names):
        states = []
        for name in names:
            states_from_region = self.__get_states_from_region(name)
            if 0 < len(states_from_region):
                states += states_from_region
            else:
                state_indices = [index for index in range(0, len(self.__states)) if name == self.__states[index]]
                for state_index in state_indices:
                    state = self.__states[state_index]
                    if pandas.notna(state):
                        states.append(state)
        return states
        


class hopkins_client:
    def __init__(self):
        self.__url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"

    def query_hopkins_data(self):
        with urllib.request.urlopen(self.__url) as stream:
            timeseries_hopkins = pandas.read_csv(stream)
            return timeseries_hopkins
        
    def query_hopkins_timeseries(self):
        with urllib.request.urlopen(self.__url) as stream:
            timeseries_hopkins = pandas.read_csv(stream)
            date_columns = timeseries_hopkins.columns[4:]
            timeseries_indexed = timeseries_hopkins[date_columns].T
            timeseries_indexed.index = pandas.to_datetime(timeseries_indexed.index)
            states = timeseries_hopkins["Province/State"]
            regions = timeseries_hopkins["Country/Region"]
            timeseries_indexed.columns = [states[index] if 0 < pandas.notna(states[index]) else regions[index] for index in range(0, len(states))]
            return hopkins_timeseries(states, regions, timeseries_indexed)
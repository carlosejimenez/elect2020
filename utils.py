import json
import pandas as pd
from us import states
import numpy as np


def get_state_yearly_aggregate(fred_api, state, code):
    data_str = f'{state.abbr}{code}'
    print(data_str)
    df = pd.DataFrame(fred_api.get_series(data_str)).resample('Y').mean()
    years = list(map(int, df.index.year))
    rates = list(df[0].values)
    return list(zip(years, rates))


def get_state_yearly_aggregate_str(fred_api, data_str):
    print(data_str)
    df = pd.DataFrame(fred_api.get_series(data_str)).resample('Y').mean()
    years = list(map(int, df.index.year))
    rates = list(df[0].values)
    return list(zip(years, rates))


def get_names2abbrs_dict():
    "converts state name + electoral districts into state_po code"
    names2abbrs = {s.name: s.abbr for s in states.STATES}
    names2abbrs['District of Columbia'] = 'DC'
    names2abbrs['Maine CD-1'] = names2abbrs['Maine']
    names2abbrs['Maine CD-2'] = names2abbrs['Maine']
    names2abbrs['Nebraska CD-2'] = names2abbrs['Nebraska']
    names2abbrs['Nebraska CD-1'] = names2abbrs['Nebraska']
    return names2abbrs

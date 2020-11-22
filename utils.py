import json
from math import exp
import pandas as pd
from us import states
from collections import defaultdict
import numpy as np
from sklearn import metrics


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


def get_d_probs():
    pass


def get_samples(in_d_probs, start_date, end_date):
    d_probs = in_d_probs.copy()
    mask = ((d_probs['date'] >= start_date) & (d_probs['date'] <= end_date))
    d_probs = d_probs[mask].sort_values(by='date').reset_index(drop=True)
    all_states = defaultdict(list)  # prior = 0.5 for all states
    for row in range(len(d_probs)):
        state_po = d_probs.iloc[row]['state_po']
        sample_size = d_probs.iloc[row]['sample_size'].item()
        if state_po == 'NAT':
            continue
        else:
            all_states[state_po].append(sample_size)
    return all_states


def logistic_weight(x):
    k = 0.001
    x0 = 1000
    e = exp(-k * (x - x0))
    return 1/(1+e)


def get_predictions(in_d_probs, start_date, end_date, alpha, logistic):
    for date in [start_date, end_date]:
        y, m, d = date.split('-')
        if len(y) != 4 or len(m) != 2 or len(d) != 2:
            raise ValueError(f'Date format is incorrect! Make sure to include leading zeros for month and day.\n'
                             f'Proper format is YYYY-MM_DD.')
    d_probs = in_d_probs.copy()
    if logistic:
        weight_func = logistic_weight
    else:
        weight_func = lambda x: 1
    mask = ((d_probs['date'] >= start_date) & (d_probs['date'] <= end_date))
    d_probs = d_probs[mask].sort_values(by='date').reset_index(drop=True)
    all_states = {k: 0.5 for k in set(get_names2abbrs_dict().values())}  # prior = 0.5 for all states
    for row in range(len(d_probs)):
        state_po = d_probs.iloc[row]['state_po']
        sample_size = d_probs.iloc[row]['sample_size'].item()
        d_prob = d_probs.iloc[row]['d_prob'].item()
        sample_weight = weight_func(sample_size)
        if state_po == 'NAT':
            continue
        else:
            weight = alpha * sample_weight
            all_states[state_po] = (all_states[state_po] * (1 - weight)) + (d_prob * weight)
    return sorted(all_states.items(), key=lambda kv: kv[1])


def get_predictions_df(in_d_probs, start_date, end_date, alpha, logistic):
    preds = get_predictions(in_d_probs, start_date, end_date, alpha, logistic)
    return pd.DataFrame.from_dict(preds).rename(columns={0: 'state_po', 1: 'd_prob'})


def get_error_df(true_df, pred_df):
    combined = pd.merge(true_df, pred_df, on=['state_po'], suffixes=['', '_preds'])[['state_po', 'd_prob_preds',
                                                                                     'd_prob']]
    combined['error'] = combined['d_prob'] - combined['d_prob_preds']
    return combined


def get_state_error_df(true_df, pred_df):
    combined = pd.merge(true_df, pred_df, on=['state_po'], suffixes=['', '_preds'])[['state_po', 'd_prob_preds',
                                                                                     'd_prob']]
    combined['error'] = combined['d_prob'] - combined['d_prob_preds']
    results = dict()
    for state in set(combined['state_po']):
        row = combined[combined['state_po'] == state]
        pred = row['d_prob_preds'].item()
        label = row['d_prob'].item()
        error = label - pred
        abs_error = abs(error)
        results[state] = {'abs_error': abs_error, 'error': error, 'squared_error': error**2}
    return pd.DataFrame(results).T.reset_index().rename(columns={'index': 'state_po'})


def get_mse(error_df):
    return np.mean(np.square(error_df['error'].values))


def get_mae(error_df):
    return np.mean(np.abs(error_df['error'].values))


def get_mean_error(error_df):
    return np.mean(error_df['error'].values)

def get_r2(combined_df):
    true_y = combined_df['d_prob'].values
    preds = combined_df['d_prob_preds'].values
    return metrics.r2(true_y, preds)

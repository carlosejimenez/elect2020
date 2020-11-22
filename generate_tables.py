import argparse
import pandas as pd
import numpy as np
from utils import get_names2abbrs_dict
from collections import defaultdict
from sklearn import metrics

BATTLEGROUND_FILE = f'pop_data/2016_pres_labels_battleground.csv'
LABELS_FILE = f'election_data/final_results_by_state.csv'
RAW_LABELS_FILE = f'election_data/final_results_raw_by_state.csv'



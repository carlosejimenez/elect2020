## Getting Started
Install python dependencies
```bash
pip install -r requirements.txt
```

Enable plotly plots in jupyter lab
```bash
bash enable_plotly.sh
```

### Generate Polling Statistics
See generate_sample_size_figures.ipynb

### Evaluate Predictions
See evaluate_preds.ipynb

## Figures
The figures directory contains all generated figures 
visualizing polling data, prediction accuracy, 
and more.

### figures/data
In the figures directory, the data directory holds all 
the csv files that were used in generating the figures.

## Data Directory
__election_data__ - Results from the NYTimes 2020 [general
election data](https://github.com/alex/nyt-2020-election-scraper), as well as processed "final results" (the most
recent values for each state).

__label_data__ - This directory contains a few different
files.
- Normalized vote share results for 2016 presidential 
race
- Normalized vote share results for 2018 senate races.
- Vote share results with battleground classification 
for 2016 presidential election.
- Electoral vote data, to be used for final election 
outcome prediction.

__poll_data__ - Poll data contains all polling data for 
the presidential race.
It also contains cleaned, normalized, vote share
labels from the raw poll data.

__population_data__ - Population data, generated from FRED.

__predictions__ - Predicted noramlized vote share for
each model.

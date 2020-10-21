#!/usr/bin/env python3
import wget


poll_urls = {
        'president_2020': 'https://projects.fivethirtyeight.com/polls-page/president_polls.csv',
        'senate_2020': 'https://projects.fivethirtyeight.com/polls-page/senate_polls.csv',
        'president_2020_avgs': 'https://projects.fivethirtyeight.com/2020-general-data/presidential_poll_averages_2020.csv',
        'president_hist_avgs': 'https://github.com/fivethirtyeight/data/blob/master/polls/pres_pollaverages_1968-2016.csv',
        }


if __name__ == '__main__':
    for poll in poll_urls.keys():
        filename = wget.download(poll_urls[poll])
        print(f'Updated {filename}')
    print(f'Done.')

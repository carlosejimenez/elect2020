import argparse
import wget


poll_urls = {
        'president_2020': 'https://projects.fivethirtyeight.com/polls-page/president_polls.csv',
        'senate_2020': 'https://projects.fivethirtyeight.com/polls-page/senate_polls.csv',
        'president_2020_avgs': 'https://projects.fivethirtyeight.com/2020-general-data/presidential_poll_averages_2020.csv',
        'president_hist_avgs': 'https://github.com/fivethirtyeight/data/blob/master/polls/pres_pollaverages_1968-2016.csv',
        }


if __name__ == '__main__':
    params = argparse.ArgumentParser(description='Downloads recent polling data from fivethirtyeight.')
    params.add_argument('--all', action='store_true')
    params.add_argument('--president-2020', action='store_true')
    params.add_argument('--senate-2020', action='store_true')
    params.add_argument('--president-2020-avgs', action='store_true')
    params.add_argument('--president-hist-avgs', action='store_true')

    args = params.parse_args()
    if args.all:
        for url in poll_urls.values():
            filename = wget.download(url)
            print(f'Updated {filename}')
    else:
        for poll in poll_urls.keys():
            if getattr(args, poll):
                filename = wget.download(poll_urls[poll])
                print(f'Updated {filename}')
    print(f'Done.')

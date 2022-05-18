import datetime as dt
import time

import pandas as pd
from psaw import PushshiftAPI
import config
from comments_collection.comments_praw import main_function

SIZE = 500
api = PushshiftAPI()


def time_spans(start_time, end_time, time_interval=3):
    period = 86000 * time_interval

    end = start_time + period
    yield int(start_time), int(end)

    pandding = 1
    while end < end_time:
        start_time = end + pandding
        end = (start_time - pandding) + period
        yield int(start_time), int(end)


def scrapp_submission(subreddit_name, start_time, end_time):
    final_data = []
    try:
        gen = api.search_submissions(subreddit=subreddit_name, after=start_time, before=end_time, size=SIZE,
                                     filter=['id', 'selftext', 'url', 'author', 'title', 'num_comments'])

        data_list = list(gen)
        for data in data_list:
            data.d_['date'] = dt.datetime.fromtimestamp(data.d_['created_utc'])
            final_data.append(data.d_)
        n = len(data_list)
        print(data_list[-1].d_['created_utc'])
        while n == SIZE:
            last = data_list[-1]
            new_start_time = last.d_['created_utc']
            gen = api.search_submissions(subreddit=subreddit_name, after=new_start_time, before=end_time, size=SIZE,
                                         filter=['id', 'selftext', 'url', 'author', 'title', 'num_comments'])

            data_list = list(gen)
            n = len(data_list)
            for data in data_list:
                data.d_['date'] = dt.datetime.fromtimestamp(data.d_['created_utc'])
                final_data.append(data.d_)
    except Exception as err:
        print(err)

    return final_data


# Before covid time period
# start date == 1st July 2018
# end date == 29th February 2020

# After covid time period
# start date == 1st March 2020
# end date == 31st October 2021

if __name__ == '__main__':
    post = []
    subreddits = config.SUBREDDIT_NAMES
    strt_time_year = config.START_TIME_YEAR
    strt_time_month = config.START_TIME_MONTH
    strt_time_day = config.START_TIME_DAY
    end_time_year = config.END_TIME_YEAR
    end_time_month = config.END_TIME_MONTH
    end_time_day = config.END_TIME_DAY
    for subreddit in subreddits:
        s_time = int(dt.datetime(int(strt_time_year), int(strt_time_month), int(strt_time_day)).timestamp())
        e_time = int(dt.datetime(int(end_time_year), int(end_time_month), int(end_time_day)).timestamp())
        for time_span in time_spans(s_time, e_time, 7):
            pulled_posts = scrapp_submission(subreddit, time_span[0], time_span[1])
            post.extend(pulled_posts)
            time.sleep(0.5)

        data_frame = pd.DataFrame(post)
        csv_file_name = subreddit + "_" + strt_time_year + "_" + end_time_year + ".csv"
        data_frame.to_csv(csv_file_name, encoding='utf-8-sig')
        print(data_frame.id)
        post.clear()
        main_function([data_frame.id.tolist(), data_frame.author.tolist()])

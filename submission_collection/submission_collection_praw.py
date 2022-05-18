import praw as pr
import pandas as pd
import datetime as dt
import time
import config

reddit = pr.Reddit(client_id='6peMbHx5tjvuHtu3dxm47w', client_secret='sACOL-6WhqFQ4CVsCt3cMQTyQJlzfA',
                   user_agent='python:DataCollectionTesting:0.0.1(by/alamincse32')

SIZE = 500


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
        for submission in reddit.subreddit(subreddit_name).top("month"):
            print(submission.id, submission.author, dt.datetime.fromtimestamp(submission.created_utc))
    except Exception as err:
        print(err)

    return final_data


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
        print(subreddit)
        print(strt_time_year)
        s_time = int(dt.datetime(int(strt_time_year), int(strt_time_month), int(strt_time_day)).timestamp())
        e_time = int(dt.datetime(int(end_time_year), int(end_time_month), int(end_time_day)).timestamp())
        for time_span in time_spans(s_time, e_time, 7):
            pulled_posts = scrapp_submission(subreddit, time_span[0], time_span[1])
            post.extend(pulled_posts)
            time.sleep(0.5)

        # data_frame = pd.DataFrame(post)
        # csv_file_name = subreddit + "_" + strt_time_year + "_" + end_time_year + ".csv"
        # data_frame.to_csv(csv_file_name, encoding='utf-8-sig')
        # post.clear()

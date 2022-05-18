import datetime as dt
import time
import config
import os
import pandas as pd
from psaw import PushshiftAPI
from comments_collection.comments_praw import main_function

SIZE = 500
api = PushshiftAPI()


def time_spans(start_time, end_time, time_interval=3):
    period = 86400 * time_interval
    end = start_time + period - 1
    # yield int(start_time), int(end)

    padding = 1
    while end < end_time:
        print(dt.datetime.fromtimestamp(start_time).strftime("%Y-%m-%d"),
              dt.datetime.fromtimestamp(end).strftime("%Y-%m-%d"
                                                      "."))
        yield int(start_time), int(end)
        start_time = end + padding
        end = start_time + period - 1
    print(dt.datetime.fromtimestamp(start_time), dt.datetime.fromtimestamp(end_time))
    yield int(start_time), int(end_time)


def scrapp_submission(subreddit_name, start_time, end_time):
    final_data = []
    try:
        gen = api.search_submissions(subreddit=subreddit_name, after=start_time, before=end_time, size=SIZE,
                                     filter=['id', 'selftext', 'full_link', 'author', 'title', 'num_comments'])
        data_list = list(gen)
        for data in data_list:
            data.d_['date'] = dt.datetime.fromtimestamp(data.d_['created_utc'])
            final_data.append(data.d_)
        n = len(data_list)
        while n == SIZE:
            last = data_list[-1]
            new_start_time = last.d_['created_utc']
            print(dt.datetime.fromtimestamp(new_start_time))
            gen = api.search_submissions(subreddit=subreddit_name, after=new_start_time, before=end_time, size=SIZE,
                                         filter=['id', 'selftext', 'full_link', 'author', 'title', 'num_comments'])

            data_list = list(gen)
            n = len(data_list)
            for data in data_list:
                data.d_['date'] = dt.datetime.fromtimestamp(data.d_['created_utc'])
                final_data.append(data.d_)
    except Exception as err:
        print(err)

    return final_data


if __name__ == '__main__':
    week_count = 1
    month_count = 0
    weekly_data = []
    monthly_data = []
    post = []
    subreddits = config.SUBREDDIT_NAMES
    strt_time_year = config.START_TIME_YEAR
    strt_time_month = config.START_TIME_MONTH
    strt_time_day = config.START_TIME_DAY
    end_time_year = config.END_TIME_YEAR
    end_time_month = config.END_TIME_MONTH
    end_time_day = config.END_TIME_DAY
    submission_file_name = config.SUBMISSION_FILE_NAME
    comment_file_name = config.COMMENT_FILE_NAME
    directory_name = config.DIRECTORY_NAME
    for subreddit in subreddits:
        s_time = int(dt.datetime(int(strt_time_year), int(strt_time_month), int(strt_time_day)).timestamp())
        e_time = int(dt.datetime(int(end_time_year), int(end_time_month), int(end_time_day), 23, 59, 59).timestamp())
        for time_span in time_spans(s_time, e_time, 7):
            pulled_posts = scrapp_submission(subreddit, time_span[0], time_span[1])
            post.extend(pulled_posts)
            time.sleep(0.5)

        path = os.getcwd() + "/" + directory_name
        if not os.path.exists(path):
            os.mkdir(path)
        df_submission = pd.DataFrame(post)
        df_submission.to_csv(directory_name + "/" + subreddit + "_" + submission_file_name, encoding='utf-8-sig')
        comment_data = main_function([df_submission.id.tolist(), df_submission.author.tolist()], s_time, e_time)
        df_comment = pd.DataFrame(comment_data[0])
        df_comment.to_csv(directory_name + "/" + subreddit + "_" + comment_file_name, encoding='utf-8-sig')
        df_comment_dis = pd.DataFrame(comment_data[2])
        df_comment_dis.to_csv(directory_name + "/" + subreddit + "_discarded_" + comment_file_name,
                              encoding='utf-8-sig')
        post.clear()

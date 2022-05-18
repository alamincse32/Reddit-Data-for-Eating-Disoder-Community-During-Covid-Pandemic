import datetime as dt
from datetime import timezone
import pandas as pd
from psaw import PushshiftAPI
import praw as pr
import pandas as ps
from collections import Counter
e_time = int(dt.datetime(int(2022), int(1), int(1)).timestamp())
r_time = int(dt.datetime(int(2022), int(2), int(28)).timestamp())
print(e_time)
reddit = pr.Reddit(client_id='6peMbHx5tjvuHtu3dxm47w', client_secret='sACOL-6WhqFQ4CVsCt3cMQTyQJlzfA',
                   user_agent='python:DataCollectionTesting:0.0.1(by/alamincse32')
#
# subreddit = reddit.subreddit("EatingDisorders").new(limit=None)
# print(len(list(subreddit)))
subreddit = reddit.subreddit("EatingDisorders").new(limit=None)
print(len(list(subreddit)))
daily_post_count = {}
for submission in reddit.subreddit("BingeEatingDisorder").new(limit=None):
    print(dt.datetime.fromtimestamp(submission.created_utc))
    # if e_time <= submission.created_utc <= r_time:
    #     s = dt.datetime.fromtimestamp(submission.created_utc, timezone.utc).date()
    #     print(s)
    #     if s not in daily_post_count.keys():
    #         daily_post_count[s] = 1
    #     else:
    #         daily_post_count[s] += 1
print(daily_post_count)
# start_epoch = int(dt.datetime(2020,3,1).timestamp())
# end_epoch = int(dt.datetime(2020,4,1).timestamp())
#
# print(dt.datetime.fromtimestamp(start_epoch/1000).strftime("'%Y-%m-%d %H:%M:%S.%f"))
# reddit = praw.Reddit("bot1")
#
# api = PushshiftAPI()
#
# gen = api.search_submissions(after=start_epoch, before=end_epoch, subreddit='EatingDisorders',filter=['id','selftext','url','author','title','subreddit'], limit=20000)
# results = list(gen)
#
# data_file = []
# a = [thing for thing in gen]
# for item in results:
#     item.d_['date'] = dt.datetime.fromtimestamp(item.d_['created_utc'])
#     data_file.append(item.d_)
#
#
# data = pd.DataFrame(data_file)
# data.to_csv("submission_data.csv", encoding='utf-8-sig')
# # start_time = int(dt.datetime(2019, 1, 1).timestamp())
# # end_time = int(dt.datetime(2019, 1, 3).timestamp())
# #
# # print(list(api.search_submissions(after=start_time, before=end_time, subreddit='learnmachinelearning',
# # filter=['url','author', 'title', 'subreddit'])))

# from datetime import datetime, timedelta
#
# current_date = datetime.now(timezone.utc)
# end_date = current_date + timedelta(days=5) # Adding 5 days.
# end_date_formatted = end_date.strftime('%Y-%m-%d')
# print(current_date)
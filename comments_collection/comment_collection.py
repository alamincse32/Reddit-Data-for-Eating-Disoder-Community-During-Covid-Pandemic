import json
import time

import pandas as pd
import datetime as dt
from psaw import PushshiftAPI
import requests

SIZE = 500
api = PushshiftAPI()


def read_submission_ids(file_name):
    try:
        # path = os.path.join(r"submission_collection\\before_pendamic",file_name)
        # print(path)
        data = pd.read_csv(
            r'I:\NDSU\MSCourses\pythonProject\submission_collection\before_pendamic\eating_disorder.csv')
        return list(data['id'])
    except Exception as err:
        print(err)


def read_comments(sub_ids):
    base_url = "https://api.pushshift.io/reddit/submission/comment_ids/"
    comment_base_url = "https://api.pushshift.io/reddit/search/comment/?ids="
    comment_body_data = []

    try:
        final_url = base_url + sub_ids
        response = requests.get(final_url)
        assert response.status_code == 200
        data = json.loads(response.content)
        # print(data['data'])
        # # time.sleep(0.25)
        print(sub_ids)
        local_comment_data = [sub_ids]
        local_comment_data.extend(data['data'])
        # if data['data']:
        #     print(len(data['data']))
            # for item in data['data']:
            #     final_comment_url = comment_base_url+item
            #     res = requests.get(final_comment_url)
            #     assert res.status_code == 200
            #     com_data = json.loads(res.content)
            #     author_name = com_data['data'][0]['author']
            #     comment_time = com_data['data'][0]['created_utc']
            #     comment_body = com_data['data'][0]['body']
            #     standard_time = dt.datetime.fromtimestamp(comment_time)
            #     local_comment_data.append(author_name)
            #     local_comment_data.append(comment_time)
            #     local_comment_data.append(standard_time)
            #     local_comment_data.append(comment_body)
            #     time.sleep(0.1)
            # print(local_comment_data)
        # else:
        #     print("alamin")

        #     for item in data['data']:
        #         final_comment_url = comment_base_url+item
        #         res = requests.get(final_comment_url)
        #         assert res.status_code == 200
        #         com_data = json.loads(res.content)
        #         print(com_data['data'][0]['body'])
        #         time.sleep(0.5)
        #         #     if com_data['data'] and len(com_data['data']) >= 1:
        #         #         for datum in com_data['data']:
        #         #             local_comment_data.append([datum["author"],datum["body"],datum["created_utc"]])
        #         #     time.sleep(0.25)
        #         # comment_body_data.append(local_comment_data)
        #         # print(comment_body_data)
        #     else:
        #         print("Alamin")
        # time.sleep(0.10)

        return local_comment_data

    except Exception as err:
        print(err)


if __name__ == '__main__':
    total_comment_data = []
    file_name = 'anorexia_nervosa.csv'
    submission_ids = read_submission_ids(file_name)
    print(len(submission_ids))

    # submission_ids = submission_ids[:20]
    try:
        i = 1
        for id in submission_ids:
            temp_comment_data = read_comments(id)
            if temp_comment_data is None:
                temp_comment_data = [id,"None"]
            total_comment_data.append(temp_comment_data)
        #time.sleep(0.1)
            #print(len(temp_comment_data))
        #     print("i === " + str(i))
        #     i+=1
        datafram = pd.DataFrame(total_comment_data)
        datafram.to_csv('eating_disorder_comments_id.csv', encoding='utf-8-sig')
    except Exception as err:
        print(err)




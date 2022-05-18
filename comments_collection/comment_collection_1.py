import json
import time

import pandas as pd
import datetime as dt
from pmaw import PushshiftAPI
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
    # comment_base_url = "https://api.pushshift.io/reddit/search/comment/?ids="
    # comment_body_data = []
    local_comment_data = [sub_ids]
    try:
        final_url = base_url + sub_ids
        response = requests.get(final_url)
        assert response.status_code == 200
        data = json.loads(response.content)
        data = data['data']
        if data is None:
            local_comment_data.append('None Data')
            print("None Data")
        else:
            if len(data) > 0:
                comments = api.search_comments(ids=data)
                print(comments)
                if comments is None:
                    print("Alamin is None")
                for comment in comments:
                    local_comment_data.append(comment['author'])
                    local_comment_data.append(comment['created_utc'])
                    local_comment_data.append(dt.datetime.fromtimestamp(comment['created_utc']))
                    local_comment_data.append(comment['body'])
        return local_comment_data
    except Exception as err:
        print(err)


if __name__ == '__main__':
    total_comment_data = []
    file_name = 'anorexia_nervosa.csv'
    # submission_ids = read_submission_ids(file_name)
    # submission_ids = submission_ids[:30]
    submission_ids = ['ab3po0',
'al0ofm',
'as67wa',
'arw3v3',
'ayne9o',
'btwtoe',
'c33r98',
'cwsqce',
'ebkx1n',
'fc5qxm']
    try:
        i = 1
        for id in submission_ids:
            temp_comment_data = read_comments(id)
            if temp_comment_data is None:
                print(temp_comment_data)
                temp_comment_data = [id,"None"]
            total_comment_data.append(temp_comment_data)
        #time.sleep(0.1)
            #print(len(temp_comment_data))
            print("i === " + str(i))
            i+=1
            time.sleep(0.5)
        datafram = pd.DataFrame(total_comment_data)
        datafram.to_csv('anorexia_nervosa_rest_of_comments_1.csv', encoding='utf-8-sig')
    except Exception as err:
        print(err)




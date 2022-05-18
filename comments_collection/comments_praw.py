import praw as pr
import pandas as pd
import datetime as dt
import time

reddit = pr.Reddit(client_id='6peMbHx5tjvuHtu3dxm47w', client_secret='sACOL-6WhqFQ4CVsCt3cMQTyQJlzfA',
                   user_agent='python:DataCollectionTesting:0.0.1(by/alamincse32')


def read_comments(submission_id, id, author, s, e):
    local_data = [id]
    local_nodes = [[id, author]]
    discarded_data = [id]
    print("Submission ID: " + id)
    count = 0
    try:
        submission_id.comments.replace_more(limit=None)
        for comment in submission_id.comments.list():
            count += 1
            print(count)
            author_name = str(comment.author)
            comment_text = comment.body
            time = comment.created_utc
            standard_time = str(dt.datetime.fromtimestamp(time))
            patent_node = str(comment.parent_id).split('_')[1]

            # append all comment data into local_data list

            if s <= time <= e:
                local_data.append(author_name)
                local_data.append(comment_text)
                local_data.append(time)
                local_data.append(standard_time)
                local_nodes.append([str(comment.id), author_name, patent_node])
            # else:
            #     # discarded_data.append(id)
            #     discarded_data.append(author_name)
            #     discarded_data.append(comment_text)
            #     discarded_data.append(time)
            #     discarded_data.append(standard_time)
            #     local_nodes.append([str(comment.id), author_name, patent_node])

    except Exception as err:
        print(err)
    return [local_data, local_nodes, discarded_data]


def main_function(submission_id_author, start_time, end_time):
    total_comments = []
    total_nodes = []
    discarded_data = []
    for id, author in zip(submission_id_author[0], submission_id_author[1]):
        if id is not None:
            submission = reddit.submission(id)
            temp_comment_data = read_comments(submission, id, author, start_time, end_time)
            if temp_comment_data[2]:
                discarded_data.append(temp_comment_data[2])
            if temp_comment_data[0]:
                total_comments.append(temp_comment_data[0])
            total_nodes.append(temp_comment_data[1])

    return [total_comments, total_nodes, discarded_data]

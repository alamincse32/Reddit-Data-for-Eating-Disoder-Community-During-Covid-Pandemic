import pandas as pd
import numpy as np
from datetime import timezone, datetime


def read_file(file_name):
    try:
        df = pd.read_csv(file_name)
        return df
    except FileNotFoundError as err:
        print(err)


def get_comment_count(data):
    row = data.shape[0]
    time_2018 = datetime(2018, 2, 28)
    timestamp_2018 = time_2018.replace(tzinfo=timezone.utc).timestamp()
    time_2019_2 = datetime(2019, 3, 1)
    timestamp_2019_2 = time_2019_2.replace(tzinfo=timezone.utc).timestamp()

    time_2019_3 = datetime(2019, 2, 28)
    timestamp_2019_3 = time_2019_3.replace(tzinfo=timezone.utc).timestamp()
    time_2020_2 = datetime(2020, 3, 1)
    timestamp_2020_2 = time_2020_2.replace(tzinfo=timezone.utc).timestamp()

    time_2020_3 = datetime(2020, 2, 29)
    timestamp_2020_3 = time_2020_3.replace(tzinfo=timezone.utc).timestamp()
    time_2021_2 = datetime(2021, 3, 1)
    timestamp_2021_2 = time_2021_2.replace(tzinfo=timezone.utc).timestamp()

    time_2021_3 = datetime(2021, 2, 28)
    timestamp_2021_3 = time_2021_3.replace(tzinfo=timezone.utc).timestamp()
    time_2022_1 = datetime(2022, 3, 1)
    timestamp_2022_1 = time_2022_1.replace(tzinfo=timezone.utc).timestamp()

    count_2018_2019 = 0
    count_2019_2020 = 0
    count_2020_2021 = 0
    count_2021_2022 = 0
    for i in range(row):
        row_data = data.iloc[i].dropna()
        row_length = len(row_data)
        row_length = row_length -2
        if row_length > 0:
            row_length = int(row_length/4)
            for j in range(row_length):
                time_stamp = data.iloc[i][str(3 + 4*j)]
                if timestamp_2018 <= time_stamp <= timestamp_2019_2:
                    count_2018_2019 += 1
                elif timestamp_2019_3 <= time_stamp <= timestamp_2020_2:
                    count_2019_2020 += 1
                elif timestamp_2020_3 <= time_stamp <= timestamp_2021_2:
                    count_2020_2021 += 1
                elif timestamp_2021_3 <= time_stamp <= timestamp_2022_1:
                    count_2021_2022 +=1
                else:
                    print("This time is out of boundary: ", datetime.fromtimestamp(time_stamp))

    return [count_2018_2019,count_2019_2020,count_2020_2021,count_2021_2022]

if __name__ == '__main__':
    file_name = 'cancer_praw_comments_3_2018_2_2020.csv'
    data = read_file(file_name)
    comment_count = get_comment_count(data)
    print(comment_count)




import pandas as pd
import numpy as np
from datetime import timezone, datetime


def read_file(file_name):
    try:
        df = pd.read_csv(file_name)
        utc_time = df['created_utc'].tolist()
        # print(utc_time)
        return utc_time
    except FileNotFoundError as err:
        print(err)

def get_submission_count(utc_time_list):
    time_2020 = datetime(2018, 2, 28)
    timestamp_2020 = time_2020.replace(tzinfo=timezone.utc).timestamp()
    time_2021 = datetime(2019,3,1)
    timestamp_2021 = time_2021.replace(tzinfo=timezone.utc).timestamp()
    time_2022 = datetime(2020,3,1)
    timestamp_2022 = time_2022.replace(tzinfo=timezone.utc).timestamp()

    count_2020_2021 = 0
    count_2021_2022 = 0
    for time in utc_time_list:
        if timestamp_2020 <= time <= timestamp_2021:
            count_2020_2021 += 1
        elif timestamp_2021 <= time <= timestamp_2022:
            count_2021_2022 += 1
        else:
            print("This time is out of boundary: ", datetime.fromtimestamp(time))

    return [count_2020_2021, count_2021_2022]


if __name__ == '__main__':
    file_name = 'cancer_3_2018_2_2020.csv'
    utc_time = read_file(file_name)
    submission_count = get_submission_count(utc_time)
    print(submission_count)

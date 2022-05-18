import pandas as pd
import config
import datetime as dt
from datetime import timezone


def get_date_range(s_time, e_time):
    s_time = dt.datetime.fromtimestamp(s_time, timezone.utc).date()
    e_time = dt.datetime.fromtimestamp(e_time, timezone.utc).date()

    start_date = dt.datetime(s_time.year, s_time.month, s_time.day)
    end_date = dt.datetime(e_time.year, e_time.month, e_time.day)

    curr_date = start_date
    curr_month = start_date.strftime("%m")
    segments = []

    loop = (curr_date != end_date)
    days_increment = 1

    while loop:
        curr_date = start_date + dt.timedelta(days=days_increment)
        prev_month = curr_month
        curr_month = curr_date.strftime("%m")
        # Add to segments if new month
        if prev_month != curr_month:
            # get start of segment
            if not segments:
                start_segment = start_date
            else:
                start_segment = segments[-1][1] + dt.timedelta(days=1)
            # get end of segment
            end_segment = curr_date - dt.timedelta(days=1)
            # define and add segment
            segment = [start_segment.date(), end_segment]
            segments.append(segment)
        # stop if last day reached
        loop = (curr_date != end_date)
        # increment added days
        days_increment += 1

    if not segments or segments[-1][1] != end_date:
        if not segments:
            start_last_segment = start_date
        else:
            start_last_segment = segments[-1][1] + dt.timedelta(days=1)
        last_segment = [start_last_segment, end_date.date()]
        segments.append(last_segment)

    for i in range(len(segments)):
        segments[i][0] = segments[i][0].strftime("%Y-%m-%d")
        segments[i][1] = segments[i][1].strftime("%Y-%m-%d")

    return segments


def get_weekly_interval(s_time, e_time):
    weekly_interval_date = []
    s_time = dt.datetime.fromtimestamp(s_time, timezone.utc).date()
    e_time = dt.datetime.fromtimestamp(e_time, timezone.utc).date()
    start_date = dt.datetime(s_time.year, s_time.month, s_time.day)
    end_date = dt.datetime(e_time.year, e_time.month, e_time.day)

    next_date = start_date
    while next_date <= end_date:
        next_date = start_date + dt.timedelta(days=6)
        weekly_interval_date.append([start_date.strftime("%Y-%m-%d"), next_date.strftime("%Y-%m-%d")])
        start_date = next_date + dt.timedelta(days=1)
    return weekly_interval_date


def count_submission_datewise(submission_file):
    submission_count = []
    date_ranges = []
    try:
        df_submission = pd.read_csv(submission_file)
        utc_times = sorted(df_submission['created_utc'].tolist(), reverse=False)
        start_time = utc_times[0]
        end_time = utc_times[-1]
        daily_post_count = {}
        for utc_time in utc_times:
            d = dt.datetime.fromtimestamp(utc_time, timezone.utc).strftime("%Y-%m-%d")
            if d not in daily_post_count.keys():
                daily_post_count[d] = 1
            else:
                daily_post_count[d] += 1
        submission_count.append(daily_post_count)

        weekly_date_interval = get_weekly_interval(start_time, end_time)
        for week in weekly_date_interval:
            week.append(0)

        for utc_time in utc_times:
            d = dt.datetime.fromtimestamp(utc_time, timezone.utc).strftime("%Y-%m-%d")
            for week in weekly_date_interval:
                if week[0] <= d <= week[1]:
                    week[2] += 1
        submission_count.append(weekly_date_interval)

        date_ranges = get_date_range(start_time, end_time)
        for date_range in date_ranges:
            date_range.append(0)

        for utc_time in utc_times:
            date_time = dt.datetime.fromtimestamp(utc_time, timezone.utc).date().strftime("%Y-%m-%d")
            for date_range in date_ranges:
                if date_range[0] <= date_time <= date_range[1]:
                    date_range[2] += 1
        submission_count.append(date_ranges)
    except FileNotFoundError as err:
        print(err)
    return submission_count


def count_comment_datewise(comment_file):
    comment_count = []
    comment_date_count = []
    utc_time_list = []
    try:
        df_comment = pd.read_csv(comment_file)
        length = df_comment.shape[0]
        for i in range(length):
            row = df_comment.loc[i].dropna()
            row_length = len(row) - 1
            if row_length > 0:
                row_length /= 4
                for j in range(int(row_length)):
                    utc_time = df_comment.iloc[i][str(3 + 4 * j)]
                    utc_time_list.append(utc_time)
        print(utc_time_list)
        utc_time_list = sorted(utc_time_list, reverse=False)
        start_time = utc_time_list[0]
        end_time = utc_time_list[-1]
        daily_comment_count = {}
        for utc_time in utc_time_list:
            d = dt.datetime.fromtimestamp(utc_time, timezone.utc).strftime("%Y-%m-%d")
            if d not in daily_comment_count.keys():
                daily_comment_count[d] = 1
            else:
                daily_comment_count[d] += 1
        comment_count.append(daily_comment_count)
        weekly_date_interval = get_weekly_interval(start_time, end_time)
        for week in weekly_date_interval:
            week.append(0)

        for utc_time in utc_time_list:
            d = dt.datetime.fromtimestamp(utc_time, timezone.utc).strftime("%Y-%m-%d")
            for week in weekly_date_interval:
                if week[0] <= d <= week[1]:
                    week[2] += 1
        comment_count.append(weekly_date_interval)
        comment_date_count = get_date_range(start_time, end_time)
        for date_range in comment_date_count:
            date_range.append(0)
        for utc_time in utc_time_list:
            date_time = dt.datetime.fromtimestamp(utc_time, timezone.utc).date().strftime("%Y-%m-%d")
            for date_range in comment_date_count:
                if date_range[0] <= date_time <= date_range[1]:
                    date_range[2] += 1
        comment_count.append(comment_date_count)
    except FileNotFoundError as err:
        print(err)

    return comment_count


if __name__ == '__main__':
    submission_file_path = config.SUBMISSION_DIRECTORY
    comment_file_path = config.COMMENT_DIRECTORY
    submission = count_submission_datewise(submission_file_path)

    df_daily = pd.DataFrame(submission[0].items(), columns=['Date', 'Submission Count'])
    df_weekly = pd.DataFrame(submission[1], columns=['Start Date', 'End Date', 'Submission Count'])
    df_monthly = pd.DataFrame(submission[2], columns=['Start Date', 'End Date', 'Submission Count'])

    writer = pd.ExcelWriter('Submissin_Count.xlsx', engine='xlsxwriter')

    df_daily.to_excel(writer, sheet_name='Daily Count')
    df_weekly.to_excel(writer, sheet_name='Weekly Count')
    df_monthly.to_excel(writer, sheet_name='Monthly Count')

    writer.save()

    comment_count = count_comment_datewise(comment_file_path)

    df_daily = pd.DataFrame(comment_count[0].items(), columns=['Date', 'Comment Count'])
    df_weekly = pd.DataFrame(comment_count[1], columns=['Start Date', 'End Date', 'Comment Count'])
    df_monthly = pd.DataFrame(comment_count[2], columns=['Start Date', 'End Date', 'Comment Count'])

    writer = pd.ExcelWriter('Comment_Count.xlsx', engine='xlsxwriter')

    df_daily.to_excel(writer, sheet_name='Daily Count')
    df_weekly.to_excel(writer, sheet_name='Weekly Count')
    df_monthly.to_excel(writer, sheet_name='Monthly Count')

    writer.save()
    writer.close()

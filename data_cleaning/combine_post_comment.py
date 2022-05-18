import pandas as pd
import data_cleaning_config
import data_cleaning


def read_post_comment(submission_file_path, comment_file_path):
    post_comment_combine = []
    try:
        post_df = pd.read_csv(submission_file_path)
        comment_df = pd.read_csv(comment_file_path)
        if post_df.shape[0] != comment_df.shape[0]:
            print("The number post and corresponding number of comments are mismatched")
            return None
        for i in range(post_df.shape[0]):
            post_and_comment = []
            post_id = post_df.iloc[i]['id']
            corresponding_comment_id = comment_df.iloc[i]['0']
            if post_id == corresponding_comment_id:
                post_and_comment.append(post_df.iloc[i]['id'])
                post_and_comment.append(post_df.iloc[i]['author'])
                post_and_comment.append(post_df.iloc[i]['title'])
                post_and_comment.append(post_df.iloc[i]['selftext'])

                comment_num = len(comment_df.iloc[i].dropna())
                if comment_num > 2:
                    for j in range(1, comment_num - 2 + 1):
                        post_and_comment.append(comment_df.iloc[i][str(j)])
            else:
                print('None ' + post_id + "  " + corresponding_comment_id)
            post_comment_combine.append(post_and_comment)

    except Exception as err:
        print(err)
    return post_comment_combine


if __name__ == '__main__':
    submission_file = data_cleaning_config.SUBMISSION_DIRECTORY
    comment_file = data_cleaning_config.COMMENT_DIRECTORY
    directory_name = data_cleaning_config.DIRECTORY_NAME

    combined_post_comment = read_post_comment(submission_file, comment_file)
    if combined_post_comment is not None:
        df = pd.DataFrame(combined_post_comment)
        df.to_csv('combined_submission_and_comment.csv', encoding='utf-8-sig')
        print(df.head(2))
        cleaned_data = data_cleaning.data_cleaning_submission_comments(df,directory_name)




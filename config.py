import configparser
from configparser import ConfigParser
SUBREDDIT_NAMES = []
config = configparser.ConfigParser()
config.read('config_information.ini')
for subreddit in config['subreddit']:
    SUBREDDIT_NAMES.append(config['subreddit'][subreddit])
START_TIME_YEAR = config['timeline']['START_TIME_YEAR']
START_TIME_MONTH = config['timeline']['START_TIME_MONTH']
START_TIME_DAY = config['timeline']['START_TIME_DAY']
END_TIME_YEAR = config['timeline']['END_TIME_YEAR']
END_TIME_MONTH = config['timeline']['END_TIME_MONTH']
END_TIME_DAY = config['timeline']['END_TIME_DAY']
SUBMISSION_FILE_NAME = config['submission_file_name']['FILE_NAME']
COMMENT_FILE_NAME = config['comments_file_name']['FILE_NAME']
DIRECTORY_NAME = config['directory_name']['DIRECTORY']

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

SUBMISSION_DIRECTORY = config['directories']['submission_file']
COMMENT_DIRECTORY = config['directories']['comment_file']
START_TIME_YEAR = config['timeline']['START_TIME_YEAR']
START_TIME_MONTH = config['timeline']['START_TIME_MONTH']
START_TIME_DAY = config['timeline']['START_TIME_DAY']
END_TIME_YEAR = config['timeline']['END_TIME_YEAR']
END_TIME_MONTH = config['timeline']['END_TIME_MONTH']
END_TIME_DAY = config['timeline']['END_TIME_DAY']
import configparser

config = configparser.ConfigParser()
config.read('data_cleaning_config.ini')

SUBMISSION_DIRECTORY = config['directories']['submission_file']
COMMENT_DIRECTORY = config['directories']['comment_file']
DIRECTORY_NAME = config['directory_name']['directory_name']
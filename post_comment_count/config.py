import configparser

config = configparser.ConfigParser()
config.read('config.ini')

SUBMISSION_DIRECTORY = config['directories']['submission_file']
COMMENT_DIRECTORY = config['directories']['comment_file']
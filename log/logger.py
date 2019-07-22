import logging
import datetime

logging.getLogger(__name__).addHandler(logging.NullHandler())


def create_log_file(attempt, target_entry_spread, profit_target):
    now = datetime.datetime.now()
    formated_date = now.strftime("%Y_%m_%d##%H_%M_%S")
    log_filename = './data/logs/' + str(attempt) + '#' + formated_date

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S')

    logging.info("Starting attempt number %s as %s with the follow parameters target_entry_spread: %s profit_target %s",
                 attempt, now, target_entry_spread, profit_target)


def run(log_message):
    logging.info(log_message)
    print(log_message)

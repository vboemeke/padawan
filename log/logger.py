import datetime
import logging


class Logger:

    def __init__(self, attempt, target_entry_spread, profit_target):
        self.__attempt = attempt
        self.__target_entry_spread = target_entry_spread
        self.__profit_target = profit_target

        self.__create_log_file()

        logging.getLogger(__name__).addHandler(logging.NullHandler())

    def __create_log_file(self):
        now = datetime.datetime.now()
        formated_date = now.strftime("%Y_%m_%d##%H_%M_%S")
        log_filename = './data/logs/' + str(self.__attempt) + '#' + formated_date

        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S')

        logging.info(
            "Starting attempt number %s as %s with the follow parameters target_entry_spread: %s profit_target %s",
            self.__attempt, now, self.__target_entry_spread, self.__profit_target)

    @staticmethod
    def run(log_message):
        logging.info(log_message)
        print(log_message)

import logging

# TODO rotate logs every month
LOG_FORMAT = "%(asctime)s %(message)s"

class Statisctic:
    def __init__(
            self,
            logfile='stat.log',
            loggername='stat.log',
            logformat=LOG_FORMAT) -> None:
        self.logfile = 'files/' + logfile
        self.logformate = logformat
        self.loggername = loggername
        self.logger = self.__create_logger()


    def __create_logger(self):
        statlogger = logging.getLogger(__name__)
        statlogger.setLevel(logging.INFO)
        handler = logging.FileHandler(self.logfile)
        handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT))
        statlogger.addHandler(handler)

        return statlogger

    def write_entry(self, user_id: str, verse_id: str):
        text_name = ''
        tt = verse_id.split('_')
        if tt[1].lower() == 'sb':
            text_name = f'{tt[0]} {tt[1].upper()} {tt[2]} {tt[3]} {tt[4]}'
        elif tt[1].lower() == 'cc':
            text_name = f'{tt[0]} {tt[1].upper()} {tt[2].title()} {tt[3]} {tt[4]}'
        elif tt[1].lower() == 'bg':
            text_name = f'{tt[0]} {tt[1].upper()} - {tt[2]} {tt[3]}'
            
        self.logger.warning(f'{user_id} {text_name}')


#stat = Statisctic('files/stattest.log', 'statlogger', LOG_FORMAT)
#stat.write_entry('user', 'ru_cc_adi_33_61')

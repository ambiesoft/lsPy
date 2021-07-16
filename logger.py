
import os
import datetime
import __main__

class Logger:
    def __init__(self) -> None:
        if not __main__.__file__:
            exit('__main__.__file__ is empty')
        # get logfile name from __main__.__file__ in the same directory
        logfilename = os.path.join(
            os.path.dirname(os.path.realpath(__main__.__file__)),
            os.path.splitext(os.path.basename(__main__.__file__))[0] + '.log')
        log = open(logfilename,'a')
        self.log = log

    def write(self, text):
        self.log.write('{}\t{}\n'.format(str(datetime.datetime.today()),text))
        self.log.flush()

    def __del__(self):
        self.log.write('\n\n')
        self.log.close()

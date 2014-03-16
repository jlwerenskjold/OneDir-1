__author__ = 'cce6g'

import time
import os
import getpass
import errno
from myeventhandler import myEventHandler
from watchdog.observers import Observer
import time

if __name__ == "__main__":

    #use testdir as default source directory
    user = getpass.getuser()
    path = '/home/' + user + '/testfolder/testdir'

    #Try to create the testdir directory it if it doesn't exist
    try:
        os.makedirs(path)
    except OSError as exception:
        #only raise an exception if it is one besides the folder already existing
        if exception.errno != errno.EEXIST:
            raise
    #assign our custom event handler
    event_handler = myEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    #loop until a keyboard interrupt watching for changes in the source directory
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
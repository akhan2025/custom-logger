import logging
import os
from contextlib import contextmanager
from collections import deque
import time
import sys
import math

#Things to do:
#round to nearest centisecond and clean up test file and make test format method

#Handles all extra args provided by the dev and stores it in the first index of attributes
class ContextHandler:
    def __init__(self):
        self.attributes = deque([{}])
        
    def add(self, **new_context_vars):
        old_context = self.attributes[0]
        new_context = {**old_context, **new_context_vars}
        self.attributes.appendleft(new_context)
        #print(self.attributes)

    def get(self, key):
        return self.attributes[0].get(key)

    def remove(self):
        self.attributes.popleft()

logging_context_handler = ContextHandler()

#Responsible for storing the args into the context handler
#This is the function called using a with statement
@contextmanager
def logging_context(**kwargs):
    """Pass in any variable through this function to add it to the context handler. 
    This can take in any number of variables as long as its formatted VariableName = Variable"""
    try:
        logging_context_handler.add(**kwargs)

        yield
    finally:
        logging_context_handler.remove()

#creates a logger with the set format and env
def create_logger(name: str) -> logging.Logger:
    """Standard logger with all settings formatted out of the box.
    Can be used with both context logging as well as the Timer class"""
    logger = logging.getLogger(name)
    logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))
    ch = logging.StreamHandler(sys.stdout)

    # create formatter
    formatter = ExtraLogFormatter("%(asctime)s %(levelname)s [%(pathname)s:%(lineno)d] %(message)8s",
                                  "%a, %d %b %Y %H:%M:%S") 
                                  #The first part specifies the format for the entire message
                                  #The second parameter specifies the asctime

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger

    logger.addHandler(ch)

    return logger

#formats all extra args provided by the context handler and adds it to the log
class ExtraLogFormatter(logging.Formatter):                                                                             
    def format(self, record) -> str:                                                                                           
        dummy = logging.LogRecord(None,None,None,None,None,None,None)                                                   
        extra_txt = ', '.join([f'{k}={v}' for k, v in logging_context_handler.attributes[0].items()])                                                                                                  
        for k,v in record.__dict__.items():                                                                             
            if k not in dummy.__dict__:                                                                                 
                extra_txt += ', {}={}'.format(k,v)                                                                      
        message = super().format(record)
        #print(extra_txt)                                                                                
        return message + ' ' + extra_txt 

# A timer class that uses the logger provided and allows it 
# to print the time a function takes to run
class Timer:
    def __init__(self, function: str, logger: logging.Logger):
        """Timer class for providing logs with a stopwatch using the timing library."""
        self.function = function
        self.logger = logger

    def __enter__(self):
        #record time
        self.start = time.perf_counter()
        

    def __exit__(self, exc_type, exc_value, traceback):
        #catch errors in code
        if exc_type is not None:
            print(exc_type, exc_value, traceback)

        #calculate time passed since start   
        self.stop  = time.perf_counter()
        timely = round(self.stop - self.start, 3)
        
        #log time elapsed
        self.logger.info('%s_time'%self.function, extra = {"time":timely})

def caplog_formatter(caplog):
    formatter = ExtraLogFormatter("%(asctime)s %(levelname)s [%(pathname)s:%(lineno)d] %(message)8s",
                                  "%a, %d %b %Y %H:%M:%S")
    caplog.handler.setFormatter(formatter)
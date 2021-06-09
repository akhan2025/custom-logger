from custom_logger import logging_context, create_logger, ExtraLogFormatter, Timer, caplog_formatter
import logging

logger = create_logger(__name__)

def matrixMultiply():
    X = [[12,7,3, 4,54,33],
        [4,5,6,4,32,43],
        [7,8,9,4,24,74],
        [4,6,4,6,111,222],
        [9,9,9,9,9,9],
        [8,8,8,8,8,8]]
    # 3x4 matrix
    Y = [[5,8,1,2,3,2],
        [6,7,3,0,3,2],
        [4,5,9,1,3,2],
        [3,2,3,2,3,2],
        [2,3,5,6,7,8],
        [1,2,3,4,5,6]]
    # result is 3x4
    result = [[0,0,0,0,0,0],
            [0,0,0,0,0,0],
            [0,0,0,0,0,0],
            [0,0,0,0,0,0],
            [0,0,0,0,0,0],
            [0,0,0,0,0,0]]

    # iterate through rows of X
    for i in range(len(X)):
        #with logging_context(i=i):
    # iterate through columns of Y
            for j in range(len(Y[0])):
                #with logging_context(j=j):
            # iterate through rows of Y
                    for k in range(len(Y)):
                        #with logging_context(k=k):
                            result[i][j] += X[i][k] * Y[k][j]
                            #logger.info("the variables are changing")

# with Timer(function = 'matrixMultiply', logger = logger):
    # matrixMultiply()

    
def run_log():
    with logging_context(foo = 'a'):
        logger.info('outer context')
        with logging_context(bar = 'b'):
            logger.info('inner context')
    logger.info('no context')        


def test_context_logger(caplog):
    # caplog.handler = logging.StreamHandler()
    caplog_formatter(caplog = caplog)
    run_log()
    for x in ['outer context foo=a', 'inner context foo=a, bar=b', 'no context']:
        assert x in caplog.text

def test_timer(caplog):
    caplog_formatter(caplog = caplog)
    with Timer(function = 'matrixMultiply', logger = logger):
        matrixMultiply()
    assert 'matrixMultiply_time , time=' in caplog.text

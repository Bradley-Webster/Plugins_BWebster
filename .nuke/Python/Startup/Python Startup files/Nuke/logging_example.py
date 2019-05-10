import logging 
import os

# setting up logging so that it can be changed on the fly 
if 'LOG_FORMAT' in os.environ: 
    LOG_FORMAT = os.environ['LOG_FORMAT']
else: 
    print 'no LOG_FORMAT in environment'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

if 'LOG_LEVEL' in os.environ: 
    LOG_LEVEL = os.environ['LOG_LEVEL']
else: 
    print 'no LOG_LEVEL in environment'
    LOG_LEVEL = logging.DEBUG

# create logger 
logger = logging.getLogger('simple_example') 
logger.setLevel(LOG_LEVEL)

# create console handler and set level to debug 
ch = logging.StreamHandler() 
ch.setLevel(LOG_LEVEL)

# create formatter 
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch 
ch.setFormatter(formatter)

# add ch to logger 
logger.addHandler(ch)

# 'application' code 
logger.debug('debug message') 
logger.info('info message') 
logger.warn('warn message') 
logger.error('error message') 
logger.critical('critical message')


import logging, tempfile, os

def setuplogger(filename = 'python.log', directory = 'C:\ErrorLogs', format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
   if directory == None:
      fd, fname = tempfile.mkstemp()
      directory = os.path.dirname(fname)

   logging.basicConfig(filename = directory + '/' + filename, format = format)

def getlog(logname, level = logging.INFO):
   '''returns a logger with logname that will print to filename and directoryname.'''
   setuplogger()
   mylog = logging.getLogger(logname)
   mylog.setLevel(level)
   mylog.info('NEW LOGGER STARTED')
   return mylog

if __name__ == '__main__':
   log = getlog('testing log 1')
   log.debug('debug message')
   log.info('info message')
   log.warn('warn message')
   log.error('error message')
   log.critical('critical message')

   log2 = getlog('testing log 2')
   log2.info('info message second Log')

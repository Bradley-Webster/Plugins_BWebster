############################################################################

import logging, tempfile, os
from datetime import datetime

# Custom Output Log File Name
currentTime = datetime.now().strftime('%d-%m-%Y_%Hh-%Mm-%Ss')
logFile = 'NukeLog_' + str(currentTime) + '.log'

# Custom Output Log Directory Name
directoryLocation = 'C:\Users\CS_SYD_PC2\.nuke\TestLogs'

def setuplogger(filename = logFile, directory = directoryLocation, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
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
   log = getlog('Custom Log')
   log.debug('Nuke Logging has been redirected to: '+ directoryLocation)
   print 'Nuke Logging has been redirected to: ' + directoryLocation

############################################################################

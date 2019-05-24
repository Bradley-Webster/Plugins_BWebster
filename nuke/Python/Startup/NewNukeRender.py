# This is a very basic example of how you could submit a job to a render farm. This uses Popen to start a new nuke process and render the set of frames from the Nuke script. This in only set up for Windows

# The full examples can be found here: https://learn.foundry.com/hiero/developers/112/HieroPythonDevGuide/examples/rush_render_auto_submit.py



import hiero.core
from hiero.exporters.FnSubmission import Submission
import re
import os
import subprocess
from hiero.core import util

# Create a Task to handle Sequences and Clips for Transcoding. This is pulled from site-packages/hiero/exporters/FnLocalNukeRender.py
# Modify this to pass the information you want to your own external processes
class NewNukeRenderTask(hiero.core.TaskBase):
  def __init__(self, jobType, initDict, scriptPath):
    hiero.core.TaskBase.__init__(self, initDict)
    self._scriptPath = scriptPath
    self._logFileName = os.path.splitext(self._scriptPath)[0] + ".log"
    self._logFile = None
    self._newNukeProcess = None
    self._frameRange = " " + str(initDict["startFrame"]) + "-" + str(initDict["endFrame"])

  def startTask(self):
    self._logFile = open( self._logFileName, 'w' )
    nukePath ='C:\\Program Files\\Nuke11.2v3\\Nuke11.2.exe'
    scriptPath = ' "' + self._scriptPath + '"'
    flags = ["-x", "-F", self._frameRange, scriptPath]
    self._newNukeProcess = subprocess.Popen([nukePath, flags], shell=True, stdout=self._logFile, stderr=subprocess.PIPE)

  """
  Clean up after render.
  """
  def finishTask(self):
    # Close log file
    self._logFile.close()

  """
  Get the render progress.
  """
  def progress(self):
    return 1.0

# Create a Submission and add your Task
class NewNukeSubmission(Submission):
  def __init__(self):
    Submission.__init__(self)    
  
  def addJob(self, jobType, initDict, filePath):
    if jobType == Submission.kNukeRender:
      return NewNukeRenderTask( jobType, initDict, filePath )
    else:
      raise Exception("LocalNukeSubmission.addJob unknown type: " + jobType)

# Add the Custom Task Submission to the Export Queue           
registry = hiero.core.taskRegistry
registry.addSubmission( "New Nuke", NewNukeSubmission )

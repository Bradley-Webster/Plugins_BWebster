import subprocess
import nuke

def newCompWithArguments():
    commandLineArguments = "--safe"
    nukeProcess = subprocess.Popen([nuke.env['ExecutablePath'], commandLineArguments])



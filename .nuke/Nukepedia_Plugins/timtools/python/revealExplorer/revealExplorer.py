import nuke
import os

def revealExplorer():
    a=nuke.selectedNode()
    b=a['file'].value()
    u=os.path.split(b)[0]
    u = os.path.normpath(u)
    print u
    cmd = 'explorer "%s"' % (u)
    print cmd
    os.system(cmd)
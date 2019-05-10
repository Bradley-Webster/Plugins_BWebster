def changeOutput():
    import sys
    sys.stdout = open('C:/temp/stdout.txt', 'w')
    sys.stderr = open('C:/temp/stderr.txt', 'w')

nuke.addOnCreate(changeOutput, nodeClass='Root')

def pre_all_frames_rendered():
    sys.stdout.write("Starting rendering time %d" % nuke.frame())

def post_all_frames_rendered():
    sys.stderr.write("Finished rendering time %d" % nuke.frame())

def setup_during_init():
    nuke.addBeforeFrameRender(pre_all_frames_rendered)
    nuke.addAfterFrameRender(post_all_frames_rendered)

setup_during_init()

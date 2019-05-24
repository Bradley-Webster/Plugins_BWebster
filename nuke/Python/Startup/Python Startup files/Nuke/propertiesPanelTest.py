import nuke

def my_func():
        print 'testing'

def addCommand():
        menu = nuke.menu('Properties')
        menu.addCommand('my tool', my_func, index = len(menu.items()))

testNode = nuke.createNode('Dot')
nuke.delete(testNode)

addCommand()

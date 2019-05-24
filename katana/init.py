from Katana import Utils, Callbacks

def catalogErrorCheck_callback(event, eventId, **kwargs):
    print("[Catalog Event] %r %r %r" % (event, eventId, kwargs))

Utils.EventModule.RegisterEventHandler(catalogErrorCheck_callback, "catalog_renderLogAppend") 
    
def addGlobalFrameRange(**kwargs):

    nodeType = kwargs.get('nodeType')

    if nodeType == 'Render':
        renderNode = kwargs.get('node')
        frameRangeGroup = renderNode.getParameter('farmSettings.setActiveFrameRange')
        frameRangeStart = renderNode.getParameter('farmSettings.activeFrameRange.start')
        frameRangeEnd = renderNode.getParameter('farmSettings.activeFrameRange.end')
    
        frameRangeGroup.setValue('Yes',0)
        frameRangeStart.setExpression('globals.inTime',0)
        frameRangeEnd.setExpression('globals.outTime',0)

        frameRangeStart.setExpressionFlag(True)
        frameRangeEnd.setExpressionFlag(True)

Callbacks.addCallback(Callbacks.Type.onNodeCreate, addGlobalFrameRange)


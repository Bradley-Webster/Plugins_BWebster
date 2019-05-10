# Definition setup by Bradley Webster @ Foundry Support 02/10/2018
def slipTrackPython(debugValues=False):

    # Get selection
    seq = hiero.ui.activeSequence()
    te = hiero.ui.getTimelineEditor(seq)
    currentSelection = te.selection() 
    
    # Check if selected track is a TrackItem
    trackToSlip = ''
    if type(currentSelection[0]) is hiero.core.TrackItem:
        trackToSlip = currentSelection[0]
 
    # If the selected track is a trackItem, continue...
    if trackToSlip != '':

        # Get Source values to use further downstream
        sourceDuration = trackToSlip.sourceDuration()
        sourceIn = trackToSlip.sourceIn()
        sourceOut = trackToSlip.sourceOut()
        sourceLength = len(range(int(trackToSlip.sourceIn()), int(trackToSlip.sourceOut())))
    
        # Debug printing statements
        if debugValues == True:
            print '\n debug values of selected track: \n'
            print 'Source duration, in and out'
            print 'sourceDuration = ', sourceDuration
            print 'sourceIn = ', sourceIn
            print 'sourceOut = ', sourceOut
            print 'sourceLength = ', sourceLength
    
        # Ask user how much they want to slide clip, must be integer
        sliderValue = nuke.getInput('Slide amount:')
    
        try:
            if int(sliderValue):
                # Get original sourceIn and compare with newSourceIn,
                sliderValue = int(sliderValue)
                oldSource = sourceIn
                newSourceIn = sourceIn + sliderValue

                # Add or Minus the Source in with the User inputted value
                trackToSlip.setSourceIn(oldSource + sliderValue)
    
                # If the value is lower, negate the value from the sourceOut, or add the value if higher
                plusOrMinus = oldSource>newSourceIn

                if plusOrMinus:
                    sourceDifference = len(range(int(newSourceIn), int(oldSource)))
                    trackToSlip.setSourceOut(trackToSlip.sourceOut() - sourceDifference)
                    newSourceOut = trackToSlip.sourceOut()
                    nuke.message('Selected Track has been slipped backwards \n New SourceIn: %s \n New SourceOut: %s' % (newSourceIn, newSourceOut))   
                if plusOrMinus == False:
                    sourceDifference = len(range(int(oldSource), int(newSourceIn)))
                    trackToSlip.setSourceOut(trackToSlip.sourceOut() + sourceDifference)
                    newSourceOut = trackToSlip.sourceOut()
                    nuke.message('Selected Track has been slipped forwards \n New SourceIn: %s \n New SourceOut: %s' % (newSourceIn, newSourceOut))   
                             
                # Debug printing statements
                if debugValues == True:
                    print '\n\n\n'
                    print 'old SourceIn ', oldSource
                    print 'new SourceIn ', newSourceIn
                    print 'sourceDifference ',  sourceDifference

        # Let user know that inputted value MUST be an integer and quit.
        except ValueError:
            nuke.message('Error: Inputted value is not an integer, please try again.')

# Definition to call, set to True for debugging.
slipTrackPython(True)

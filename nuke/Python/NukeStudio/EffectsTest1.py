# https://github.com/antiero/dotStudio/blob/master/Python/Startup/nukestudio_extensions.py#L47

project = hiero.ui.activeSequence().project()
items = []
sequences = project.sequences()
sequenceName = 'TEST'
trackName = 'Shot0005'
selectedEffect = ''
for sequence in sequences:
    if sequence.name() == sequenceName:
      # Sequence Match found.. iterate Tracks...
      tracks = sequence.items()
      for track in tracks:
        if track.name() == trackName:
          # Track Match found.. iterate TrackItems...
          trackItems = track.items()
        # Handle SubTrackItems on Video Tracks
        if isinstance(track, hiero.core.VideoTrack):
          subTracks = track.subTrackItems()
          for subTrack in subTracks:
            for subTrackItem in subTrack:
              if subTrackItem.name() == trackItemName:
                  selectedEffect = subTrackItem

print 'Current Soft Effect Selected:' , selectedEffect


# End of Test


project = hiero.ui.activeSequence().project()
sequences = project.sequences()
sequenceName = hiero.ui.activeSequence()
sequenceTracks = sequenceName.items()
for track in sequenceTracks:
            print track.name()
            trackItems = track.items()
            # Handle SubTrackItems on Video Tracks
            for items in trackItems:
                    TrackItemClip= items.source()
                    print items.name()
                    print TrackItemClip
                    clipMediaSource = TrackItemClip.mediaSource()
                    #print clipMediaSource

                    mediaSourceMetaData = clipMediaSource.metadata()
                    #print mediaSourceMetaData

                    print mediaSourceMetaData.value("foundry.source.path")

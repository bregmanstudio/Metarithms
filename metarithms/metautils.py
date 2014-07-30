# metarithms.metautils - library for converting lists to music21 streams and pitch sequences in python
# Author: Michael A. Casey
# License: Apache License v. 2.0+
# Copyright: Bregman Labs, Dartmouth College, All Rights Reserved
# convert numpy arrays or python lists to music 21 format for MIDI playback
try:
    import music21.tempo as T
    import music21.stream as S
    import music21.note as N
    _HAVE_MUSIC21 = True
except:
    print "Warning: Music21 not installed, some functionality not supported"
    _HAVE_MUSIC21 = False
finally:
    pass

if _HAVE_MUSIC21:
    def list2mus(l):
        """
        convert a list of notes (pitch,dur) into music21 stream format
        """
        s = S.Stream()
        for p,d in l:
            n = N.Note()
            n.midi=p
            n.quarterLength=d
            n.octave=p/12-1
            s.append(n)
        return s
  

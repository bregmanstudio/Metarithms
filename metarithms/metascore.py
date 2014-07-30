# metarithms.metascore - library for musical score metacreation with algorithms
# Author: Michael A. Casey
# License: Apache License v. 2.0+
# Copyright: Bregman Labs, Dartmouth College, All Rights Reserved

import numpy as np
import sys

# intervals
pU=0
PU=0
m2=1
M2=2
a2=3
A2=3
m3=3
M3=4
p4=5
P4=5
a4=6
A4=6
d5=6
D5=6
p5=7
P5=7
m6=8
M6=9
m7=10
M7=11
p8=12
P8=12

rel_scale = {
'maj':np.array([PU,M2,M2,m2,M2,M2,M2,m2]),
'mel_up':np.array([PU,M2,m2,M2,M2,M2,M2,m2]),
'mel_dn':np.array([PU,M2,m2,M2,M2,m2,M2,M2]),
'har':np.array([PU,M2,m2,M2,M2,m2,A2,m2]),
'pen':np.array([PU,M2,A2,M2,M2,A2]),
'who':np.array([PU,M2,M2,M2,M2,M2,M2]),
'oct':np.array([PU,m2,M2,m2,M2,m2,M2,m2,M2]),
'oct2':np.array([PU,M2,m2,M2,m2,M2,m2,M2,m2])
}

abs_scale = {
'maj':np.cumsum(rel_scale['maj']),
'mel_up':np.cumsum(rel_scale['mel_up']),
'mel_dn':np.cumsum(rel_scale['mel_dn']),
'har':np.cumsum(rel_scale['har']),
'pen':np.cumsum(rel_scale['pen']),
'who':np.cumsum(rel_scale['who']),
'oct':np.cumsum(rel_scale['oct']),
'oct2':np.cumsum(rel_scale['oct2'])
}

rel_chord = {
'maj':np.array([PU,M3,m3]),
'min':np.array([PU,m3,M3]),
'aug':np.array([PU,M3,M3]),
'dim':np.array([PU,m3,m3]),
'dom7':np.array([PU,M3,m3,m3]),
'maj7':np.array([PU,M3,m3,M3]),
'min7':np.array([PU,m3,M3,m3]),
'minmaj7':np.array([PU,m3,M3,M3])
}

abs_chord = {
'maj':np.cumsum(rel_chord['maj']),
'min':np.cumsum(rel_chord['min']),
'aug':np.cumsum(rel_chord['aug']),
'dim':np.cumsum(rel_chord['dim']),
'dom7':np.cumsum(rel_chord['dom7']),
'maj7':np.cumsum(rel_chord['maj7']),
'min7':np.cumsum(rel_chord['min7']),
'minmaj7':np.cumsum(rel_chord['minmaj7'])
}

triad = np.array([0,2,4])

header="""\\version "2.12.3"
\\header{
    title="%s"
}
\score{
\\new PianoStaff <<
      \\new Staff = "up" {
      \\clef treble
      \\time 15/16
      \\set beatGrouping = #'(5 5 5)
      """

tailer="""  }
      \\new Staff = "down" {
        \\time 15/16
        \\clef treble
        \\set beatGrouping = #'(5 5 5)
        s1*%d
      }
    >>
}"""

DEFAULT_TEMPLATE = """    
    \change Staff = "up"
    %s16
    \change Staff = "down"
    %s
    \change Staff = "up"
    %s
    %s
    \change Staff = "down"
    %s
    """

EXPERIMENTAL_TEMPLATE = """    
    %s16
    %s
    %s
    %s
    %s
    """

def make_pitch_map():
    pm=('c','cis','d','ees','e','f','fis','g','gis','a','bes','b')    
    pitch_map=[]
    for octave in range(0,4):
        po = [p+","*(4-octave) for p in pm]
        pitch_map.append(po)
    pitch_map.append(pm)    
    for octave in range(6,12):
        po = [p+"'"*(octave-5) for p in pm]
        pitch_map.append(po)        
    return np.array(pitch_map).flatten()

def foo(p, template=DEFAULT_TEMPLATE):
    pm = make_pitch_map()
    s=""
    for ip in p:
        t=tuple([pm[i] for i in ip])
        s+=template%t+'\n'
    return s

def min(a):
    return np.array([a, a+3, a+7])

def maj(a):
    return np.array([a, a+4, a+7])

def aug(a):
    return np.array([a, a+4, a+8])

def dim(a):
    return np.array([a, a+3, a+6])

def interval(a, i):
    return np.array([a, a+i])

def lookup(scale, chord):
    """ use lookup table approach to generating pitches from patterns (chords) and modes
    """
    scale = abs_scale[scale] if type(scale) is str else scale
    l = len(scale)-1
    height = (chord/l)*12 # octave offsets
    return scale[np.mod(chord,l)]+height

def interleave(l,r):
    """ combine separate streams into a single stream
    """
    return np.array([r[0],l[0],r[1],l[1],l[2]])


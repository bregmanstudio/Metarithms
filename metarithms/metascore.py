# metarithms.metascore - library for musical score metacreation with algorithms
# Author: Michael A. Casey
# License: Apache License v. 2.0+
# Copyright: Bregman Labs, Dartmouth College, All Rights Reserved

import numpy as np

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

def lookup(scale='maj', contour=[0,1,2,3,4], transposition=0):
    """ use lookup table to generate pitches from scale and contour
    inputs:
       scale - string or ordered list of scale intervals
       contour - list of indexes to lookup scale
       [transposition] - apply transposition in semitones to contour
    outputs:
       interval list as np.array 
    """
    _scale = abs_scale[scale] if type(scale) is str else scale
    _scale = np.array(_scale) if type(_scale)!=np.ndarray else _scale
    l = len(_scale)-1
    _contour = np.array(contour) if type(contour)!=np.ndarray else contour
    _contour += transposition
    height = (_contour//l)*_scale[-1] # octave offsets
    return _scale[np.mod(_contour,l)]+height

def interleave(l,r):
    """ combine separate streams into a single stream
    """
    return np.array([r[0],l[0],r[1],l[1],l[2]])

def nchoose2(N):
    """
    generate combinations of 2 values from a set of n values
    """
    L = list()
    for j in range(N-1):
        for k in range(j+1,N):
            L.append((j,k))
    return L

def nchoose3(N):
    """
    generate combinations of 3 values from a set of n values
    """
    L = list()
    for j in range(N-2):
        for k in range(j+1,N):
            for l in range(k+1,N):
                L.append((j,k,l))
    return L


def nkrec(N,K,L):
    """
    n choose k via recursion
    """
    if N==K:
        return L
    for k in range(K,N):
        nkrec(N,K+1,L[-1].extend([k]))
    return L
                
def nchoosek(N,K):
    """
    return list of combinations of N items taken K at a time
    """
    L = list()
    if K==N:
        return L
    for k in range(N-K):
        L.append([k])
        nkrec(N,K+1,L)
    return L


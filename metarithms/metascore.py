# metarithms.metascore - library for musical score metacreation with algorithms
# Author: Michael A. Casey
# License: Apache License v. 2.0+
# Copyright: Bregman Labs, Dartmouth College, All Rights Reserved

import numpy as np
import itertools

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

relative_scale = {
'major':np.array([PU,M2,M2,m2,M2,M2,M2,m2]),
'melodic_ascending':np.array([PU,M2,m2,M2,M2,M2,M2,m2]),
'melodic_descending':np.array([PU,M2,m2,M2,M2,m2,M2,M2]),
'harmonic':np.array([PU,M2,m2,M2,M2,m2,A2,m2]),
'pentatonic':np.array([PU,M2,A2,M2,M2,A2]),
'wholetone':np.array([PU,M2,M2,M2,M2,M2,M2]),
'octatonic':np.array([PU,m2,M2,m2,M2,m2,M2,m2,M2]),
'octatonic2':np.array([PU,M2,m2,M2,m2,M2,m2,M2,m2])
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

abs_scale = dict([(k,np.cumsum(rel_scale[k])) for k in rel_scale])
absolute_scale = dict([(k,np.cumsum(relative_scale[k])) for k in relative_scale])
abs_chord = dict([(k,np.cumsum(rel_chord[k])) for k in rel_chord])

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

def lookup(scale='maj', pattern=[0,1,2,3,4], shift=0):
    """ use lookup table to generate pitches from a scale and a pattern
    inputs:
       scale - string or ordered list of scale intervals
       pattern - list of indexes to lookup scale
       [shift] - apply scale degree shift to pattern
    outputs:
       interval list as np.array 
    """
    _scale = abs_scale[scale] if type(scale) is str else scale
    _scale = np.array(_scale) if type(_scale)!=np.ndarray else _scale
    l = len(_scale)-1
    _pattern = np.array(pattern) if type(pattern)!=np.ndarray else pattern
    _pattern += shift
    height = (_pattern//l)*_scale[-1] # octave offsets
    return _scale[np.mod(_pattern,l)]+height

def interleave(l,r):
    """ Deprecated: combine separate streams into a single stream
    """
    return np.array([r[0],l[0],r[1],l[1],l[2]])

def nchoosek(N,K, with_replacement=False):
    """
    return list of all combinations of N items taken K at a time
    """
    if with_replacement:
        return itertools.combinations_with_replacement(range(N),K)
    else:
        return itertools.combinations(range(N),K)

def lfsr(seed, mask):
    """
    Use lfsr tables for maximum length sequences, e.g.:
    lfsr(0b11001001, 0b11100001) # (8,7,6,1))
    """
    result = seed
    nbits = mask.bit_length()-1
    while True:
        result = (result << 1)
        xor = result >> nbits
        if xor != 0:
            result ^= mask
        yield xor, result

def mls(N=100, gen=lfsr(0b11001001, 0b11100001)):
    return [gen.next()[1] for _ in range(N)]
    

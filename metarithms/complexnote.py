import numpy as np
import matplotlib as mp
import cmath
# Coding of pitch-duration as complex sequences
def CNote(rat,dur):
    return cmath.rect(rat,dur)

# Class for organizing sequences hierarchically into graphs
class Node:
    """
    Members:
    .id   - node identifier
    .val  - value or array of values
    .parent - parent node, None if root of tree
    .child- child node
    .next - next node
    .prev - previous node
    .relative - node uses relative (to parent) pitch/duration coding [False]
    """
    def __init__(self, id="", v=None, val=CNote(1.0,1.0), parent=None, child=None, prev=None, next=None):
        self.id = id
        self.val = v if v is not None else val
        self.parent = parent
        self.child = child
        self.prev = prev
        self.next = next
        self.relative = False

    def add_sibling(self, v=None, **kwargs):
        kwargs['val'] = v if v is not None else kwargs.get('val')
        n = Node(**kwargs)
        t = self.bfs()
        t.next = n
        n.prev = t

    def add_child(self, v=None, **kwargs):
        kwargs['val'] = v if v is not None else kwargs.get('val')
        c = Node(**kwargs)
        p = self.dfs()
        c.parent = p
        p.child = c

    def bfs(self):
        t = self
        while t.next:
            t = t.next
        return t

    def dfs(self):
        c = self
        while c.child:
            c = c.child
        return c

    def siblings(self):
        p = self
        lst = []
        while p:
            lst.extend([p.val])
            p = p.next
        return lst
        
    def children(self):
        p = self.child
        lst = []
        while p:
            lst.extend([p.val])
            p = p.child
        return lst

    def gen_relative(self, val=CNote(1.0,1.0)):
        if not self: 
            return
        self.relative=True
        self.val = np.absolute(self.val)*np.absolute(val)*np.exp(1j*np.angle(val)*np.angle(self.val)) # phase modulation
        if self.child :
            self.child.gen_relative(self.val)
        if self.next:
            self.next.gen_relative(val)

    def gen_absolute(self, val=CNote(1.0,1.0)):
        if not self: 
            return            
        self.relative=False
        self.val /= val
        if self.child :
            self.child.gen_absolute(self.val)
        if self.next:
            self.next.gen_absolute(val)

# Routines to visualize and inspect complex sequences

"""
plot_abs - inspect the absolute values (magnitudes) of a sequence
"""
def plot_abs(x):    
    r = abs(x)
    mp.pyplot.stem(np.arange(len(r)),r)
    mp.pyplot.grid()
    mp.pyplot.title('Magnitudes')
    mp.pyplot.xlabel('Discrete time index')
    mp.pyplot.ylabel('Magnitude')
    
"""
relative_phase - return rhythmic phase in readable form (normalized 0..1)
"""
def relative_phase(x):
    p = np.angle(x) # get relative phase (0..1)
    p[p<0]=1.0+p[p<0]
    return p

"""
plot_angle - inspect the phase angles of a sequence
"""
def plot_angle(x):
    r = relative_phase(x)
    mp.pyplot.stem(np.arange(len(r)),r)
    mp.pyplot.xticks(np.arange(len(r)),r)
    mp.pyplot.grid()
    mp.pyplot.title('Phase Angles')
    mp.pyplot.xlabel('Discrete time index')
    mp.pyplot.ylabel('Relative phase (radians)')
    
"""
plot_seq - inspect the magnitudes and phase angles of a sequence
"""
def plot_seq(x, log_freq=True):    
    r = np.log2(np.absolute(x))*12.0 if log_freq else np.absolute(x)
    p = relative_phase(x)
    p[p<0]=1.0+p[p<0]
    mp.pyplot.stem(p,r)
    mp.pyplot.grid()
    mp.pyplot.title('Complex Sequence')
    mp.pyplot.xlabel('Relative phase (/2*pi)')
    if log_freq:
        mp.pyplot.ylabel('Half steps (relative pitch)')
    else:
        mp.pyplot.ylabel('Frequency ratio (relative pitch)')


# Routines to represent sequences of frequency ratios and rhythmic phases as complex numbers
"""
to_complex, convert between sequence and complex representations
"""
def to_complex(r, p=None):
    p = np.ones(len(r)) if p is None else p
    p = p / p.sum()
    return r*np.exp(1j*p)

"""
to_seq, convert between complex and sequence representations
"""
to_seq = lambda x: (np.absolute(x), relative_phase(x))

"""
to_ratios, convert between chromatic scale degrees and frequency ratios
"""
to_ratios = lambda x: to_complex(2**(x/12.))

"""
to_degrees, convert between frequency ratios and chromatic scale degrees
"""
to_degrees = lambda x: np.absolute(np.log2(x)*12)

# Manipulate phase to transform rhythmic information

"""
phase_offset - add a constant time offset to sequence, offset given as proportion of time duration
"""
phase_offset = lambda x, p : x*np.exp(1j*p) # set rhythmic offset

"""
phase_scale - scale sequence temporal durations, scale given as proportion of time duration
"""
phase_scale = lambda x, s: np.absolute(x)*np.exp(1j*(s*np.angle(x))) # set rhythmic scaling


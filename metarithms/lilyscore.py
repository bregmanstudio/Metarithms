# lilyscore - Lilypond notation structures (experimental)
#
# Templates would usually be generated to some contraints.
#
# Author: Michael A. Casey
# package: metarithms
# status: experimental

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

# The following example shows a 5 note pattern distributed across two PianoStaff staves
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

# Map from midi pitch to Lilypond pitch format
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

# Apply lilypond (or other notation) template to corresponding pitch n-tuple sequence
def foo(p, template=DEFAULT_TEMPLATE):
    pm = make_pitch_map()
    s=""
    for ip in p:
        t=tuple([pm[i] for i in ip]) # requires n-tuple to match string template
        s+=template%t+'\n' # by string substitution
    return s


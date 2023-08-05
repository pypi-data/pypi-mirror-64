from .matlab_like import double
import numpy as np
def aa2int(aa):
    aa = aa.lower()
    aa = list(aa)
    map = [
      0,
	  1, #"a": 
      21, #"b": 
      5, #"c": 
      4, #"d": 
      7, #"e": 
      14, #"f": 
      8, #"g": 
      9, #"h": 
      10, #"i": 
      0, #"j": 
      12, #"k": 
      11, #"l": 
      13, #"m": 
      3, #"n": 
      0, #"o": 
      15, #"p": 
      6, #"q": 
      2, #"r": 
      16, #"s": 
      17, #"t": 
      0, #"u":
      20, #"v": 
      18, #"w": 
      23, #"x": 
      19, #"y": 
      22, #"z": 
      24, #"*": 
      25, #"-": 
      0 #"?": 
    ]
    map = np.array(map)
    
    aa = double(aa)-96
    
    aa[aa==0] = 29
    aa[aa==27] = 29
    aa[aa==-51] = 28 #gaps (-)
    aa[aa==-54]  = 27 #stop (*)

    aa = map[aa]
    return aa.T
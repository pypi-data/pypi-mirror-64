from .matlab_like import repmat,size
from .aa2int import *
import numpy as np
def aa2idx(xseq, defSize):
    [n,m] = size(xseq)
    if m > n:
        xseq = xseq.T
        [n,m] = size(xseq)
    JF = lambda x:(''.join(x).upper())
    try:
        xseq=np.apply_along_axis(JF, 1, xseq)
    except:
        xseq=JF(xseq)
    if defSize == 20:
        A2IV = np.vectorize(lambda x:aa2int(x), signature='()->(n)')
        vls = A2IV(xseq)-1
    pot = repmat(list(range(0,m)),n,1)
    [l,c]=size(vls)
    if l > c and l > 1:
        vls = vls.T
    [l,c]=size(pot)
    if l > c and l > 1:
        pot = pot.T
    t=repmat(defSize,n,m)
    [l,c]=size(t)
    if l > c and l > 1:
        t = t.T    
    mret = np.sum((t**pot)*vls,axis=0)+1
    return mret
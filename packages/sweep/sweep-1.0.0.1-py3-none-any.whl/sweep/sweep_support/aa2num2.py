def aa2num2 (xseq):
    n, m = size(xseq)
    xseq2=[]
    for i in range(0,n):
        xseq2.append (''.join(xseq[i]))
    xseq=np.array(xseq2)
    n, m = size(xseq)
    vls = aa2int(xseq)-1
    pot = repmat(range(0,m),n)
    mret = sum(np.transpose((repmat(20,n,m)**pot)*vls))+1
    inot = find((prod(1-(((vls < 0) | (vls > 19))+0)) == 0)+0)
    mret[inot] = -1
    t=repmat(20,n,m)**pot
    return np.array(mret)
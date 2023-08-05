import sympy
from .sweep_support import fastaread,mask2vec,generate_chunk,length,zeros,ceil,size
import scipy.io as sio
import hdf5storage
import re
import os
import numpy as np
from .getMatrixFile import getMatrixFile
    
def fas2sweep(xfas,out_mat_file=None,orthMat=None,mask=None,verbose=False,maxs_seqs=2E+3):
    fasta_type='AA'
    if mask is None:
        mask = np.array([2,1,2])
    withPos = 0
    if fasta_type == 'AA':
        defSize = 20
    elif fasta_type == 'NT':
        defSize = 4
    Ps = sympy.prime(1)
    
    libLocal = re.sub('[\\\/][^\\\/]+$','',os.path.realpath(__file__))
    
    if verbose:
        message = 'Starting the HDV generation and transformation to SWEEP. Please wait...'
        print(message)
    
    # Extracts the sequences from the fasta file
    if isinstance(xfas, str):
        fas_cell = xfas = fastaread(xfas);
    else:
        fas_cell = xfas;
    headers=[]
    seqs=[]
    for i in fas_cell:
        seqs.append(str(i.seq))
        headers.append(str(i.description))
    seqs = np.array(seqs)
    headers = np.array(headers)

    # Checking if all sequences are bigger than de mask size
    vlen = np.vectorize(len)
    seq_size = np.array(vlen(seqs))
    headers_small = seq_size < sum(mask);

    if sum(headers_small.astype(int)) > 0:
        message = 'There are sequences smaller than the mask size.'
        print(message)
        quit()
    chunks = ceil(len(seqs)/maxs_seqs)
    idx = generate_chunk(chunks, length(seqs))-1;

    if orthMat is None:
        getMatrixFile(libLocal+'/orthMat_default600.mat')
        orthMat = hdf5storage.loadmat(libLocal+'/orthMat_default600.mat')['orthMat_default600'].astype('float')

    projMat = zeros(len(seqs),size(orthMat)[1])
    
    M2V = np.vectorize(lambda a: mask2vec(a, Ps, withPos, mask, defSize), signature='()->(n)')
    for i in range(0,chunks):
        if verbose:
            print(str(i)+'/'+str(chunks))
        parcM = seqs[np.array(range(int(idx[i,0]),int(idx[i,1])+1))]
        W160k = np.dot(M2V(parcM),orthMat)
        projMat[int(idx[i,0]):int(idx[i,1])+1,:] = W160k
    if verbose:
        print(str(chunks)+'/'+str(chunks))
        
    if not (out_mat_file is None):
        sio.savemat(out_mat_file,{re.sub('\..+','',out_mat_file):projMat})
    return projMat
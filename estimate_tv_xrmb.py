#!/usr/bin/env python
import os
import sys
import numpy as np
import scipy
import scipy.io
import librosa
import subprocess
import HTK
from contextualize import *
from writehtk import *
from subprocess import call
import matplotlib.pyplot as plt
from KalmanSmoother import *

def float2pcm16(f):    
    f = f * 32768 ;
    f[f > 32767] = 32767;
    f[f < -32768] = -32768;
    i = np.int16(f)
    return i


def estimate_tv_xrmb(infile, opdir):
#=========================================================================
# Function to estimate TVs from pretrained TV estimator
# Usage:        estimate_tv_xrmb(fpath)
# Inputs:       fpath - string specifying path to input wav file
# Outputs:      Saved mat file <filename_tv.mat> in the current directory
# Author:       Ganesh Sivaraman
# Date Created: 11/14/2016
# Date Modified:
#=========================================================================
    WAV_SRATE = 8000   # Signals will be downsampled to 8kHz
    std_frac = 0.25
    CONTEXT = 8
    SKIP = 2
    dirname, fname = os.path.split(infile)
    fname, ext = os.path.splitext(fname)
    temp_fpath = "./temp_data/"+fname+".wav"
    if not os.path.exists('./temp_data'):
        os.makedirs('./temp_data')
    call(["sox", infile, temp_fpath])
    sig, fs = librosa.load(temp_fpath, sr=WAV_SRATE)
    # To avoid clipping and normalize the maximum loudness, divide signal by
    # max of absolute amplitude
    sig = sig/max(abs(sig))
    sig = float2pcm16(sig)
    scipy.io.wavfile.write(temp_fpath, WAV_SRATE, sig)
    
    # Create HTK MFCC features
    cmd = 'HCopy -T 0 -C mfcc13.conf '+temp_fpath+' '+'./temp_data/'+fname+'.htk'
    subprocess.call(cmd.split(' '))
    
    # read HTK MFCC features and perform mvn
    htkfile = HTK.HTKFile()
    htkfile.load('./temp_data/'+fname+'.htk')
    feats = np.asarray(htkfile.data)
    mean_G = np.mean(feats, axis=0)
    std_G = np.std(feats, axis=0)
    feats = std_frac*(feats-mean_G)/std_G
    feats = feats.T    
    cont_feats = contextualize(feats,CONTEXT,SKIP)
    NET = scipy.io.loadmat('XRMB_htkMFCC_usable_spknorm_res_nrm.mat')
    NET = NET['NET']
    IW = NET['IW'][0][0][0][0]
    LW = NET['LW'][0][0][1][0]
    b_in = NET['b'][0][0][0][0]
    b_out = NET['b'][0][0][1][0]
    hlayer_act = np.tanh(np.dot(IW,cont_feats)+b_in)
    tv = np.tanh(np.dot(LW,hlayer_act)+b_out)/std_frac
    tv_smth = kalmansmooth(tv)

#    plt.figure()
#    for ii in range(tv.shape[0]):
#        plt.subplot(3,2,ii+1)
#        plt.plot(tv[ii,:],color='red')
#        plt.plot(tv_smth[ii,:],color='blue')       
#    plt.show()
    opdir = opdir+dirname
    opfnm = opdir+'/'+fname+'.htk'
    writehtk(tv_smth.T, 10, opfnm)
    os.remove(temp_fpath)
    os.remove('./temp_data/'+fname+'.htk')
    return
    
    
if __name__ == "__main__":
    estimate_tv_xrmb(sys.argv[1], sys.argv[2])

    

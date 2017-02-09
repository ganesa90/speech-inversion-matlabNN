# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 13:20:07 2016

@author: ganesh
"""
import numpy as np

#function mat_contxt = contextualize3(mat_inp,context,step)
def contextualize(mat_inp,context,step):
    feat_dim = mat_inp.shape[0]
    if context == 0:
        mat_contxt = mat_inp
    else:
        mat_g = mat_inp
        mat_rshft = mat_g
        mat_lshft = mat_g
        for iter1 in range(context):
            buff_r = []
            buff_l = []
            for iter2 in range(step):
                buff_r.append(mat_rshft[:,0,None])
                buff_l.append(mat_lshft[:,-1,None])
            buff_r = np.concatenate(buff_r, axis=1)
            buff_l = np.concatenate(buff_l, axis=1)
            mat_rshft = np.concatenate((buff_r, mat_rshft[:,0:-step]),axis=1)
            mat_lshft = np.concatenate((mat_lshft[:,step:], buff_l),axis=1)
            mat_g = np.concatenate((mat_rshft, mat_g, mat_lshft), axis=0) 
        mat_contxt = np.zeros(mat_g.shape)
        cdim = 2*context+1
        cfeat_dim = cdim*feat_dim    
        for i in range(feat_dim):
            st = cdim*i
            en = st+cdim
            mat_contxt[range(st,en),:] = mat_g[range(i,cfeat_dim,feat_dim),:]
    return mat_contxt
    
#if __name__ == "__main__":
#    a = np.round(np.random.rand(4,10)*100)
#    print(a)
#    b = contextualize(a,1,2)
#    print(b)
    
    

        
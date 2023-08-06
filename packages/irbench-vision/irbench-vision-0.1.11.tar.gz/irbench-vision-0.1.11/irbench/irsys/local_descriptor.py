''' local_descriptor.py
IR System for local descriptor
'''

import os, sys, time
import random

import numpy as np

__DEBUG__ = True

class LocalDescriptorIRHelper():
    def __init__(self):
        print('initialize LocalDescriptorIR ...')
        
    def __validate_format__(self, sample):
        lkeys = sample.keys()
        assert 'location_np_list' in lkeys, "'location_np_list' is not found."
        assert 'descriptor_np_list' in lkeys, "'descriptor_np_list' is not found."
        assert 'unique_id' in lkeys, "'unique_id' is not found."
    
    def __validate_format__(self, sample):
        lkeys = sample.keys()
        assert 'location_np_list' in lkeys, "'location_np_list' is not found."
        assert 'descriptor_np_list' in lkeys, "'descriptor_np_list' is not found."
        assert 'unique_id' in lkeys, "'unique_id' is not found."
        raise NotImplementedError()
   

    # public functios
    def build_index(
        self,
        x,
        m,
        n_bits):
        '''
        Args: 
            x: numpy array of descriptors, (ndescriptors x ndims)
            m: number of subquantizers
            n_bits: bits allocated per subquantizer
        Returns:
            indexed faiss
        '''
        dims = x.shape[1]
        
        # create index
        self.index = faiss.IndexPQ(dims, m, n_bits)
        
        # train
        self.index.train(x)
        
        if __DEBUG__:
            print('Training K-means for PQ ...')
            print('created index: ', self.index)

    def add_index(self, x_d):
        ''' populate the database
        '''
        self.index.add(x_d)

    def search(
        self,
        q_id,
        top_k = 10,
        method = 'BRUTE_FORCE'):
        '''
        Args:
            top_k: Top K index
        Returns:
            ret: id list of retrieved candidates
        '''
        assert method.upper() in ['BRUTE_FORCE', 'BF', 'PQ']
        raise NotImplementedError()


if __name__ == '__main__':
    pass;




















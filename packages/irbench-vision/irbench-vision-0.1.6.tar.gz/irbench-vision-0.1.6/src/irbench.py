'''irbench.py
'''
import os
import sys

import numpy as np

import .utils.utils as U 
from .irsys.global_descriptor import GlobalDescriptorIRHelper as GDIR
from .irsys.local_descriptor import LocalDescriptorIRHelper as LDIR


class IRBench():
    def __init__(self, config):
        '''
        config = {
            'srch_method': 'brute-force',   # 'bf / kdtree / lsh'
            'desc_type': 'global',
        }
        '''

        self.__VERBOSE__ = config.get('verbose')
        if self.__VERBOSE__ is None:
            self.__VERBOSE__ = False

        self.qk = config.get('qk')
        self.dk = config.get('dk')
        self.srch_method = config.get('srch_method')
        self.srch_lib = config.get('srch_lib')
        self.with_mtc = config.get('with_mtc') \
            if config.get('with_mtc') is not None \
            else False
        self.desc_type = config.get('desc_type') \
            if config.get('desc_type') is not None \
            else 'global'

        assert self.srch_lib in [ None, 'sklearn', 'flann'], \
            'Invalid srch_lib: {}'.format(self.srch_lib)
        assert self.srch_method in ['bf', 'kdtree', 'lsh', 'fashion'], \
            'Invalid srch_method: {}'.format(self.srch_method)
        assert self.desc_type in ['global', 'local'], \
            'Invalid desc_type: {}'.format(self.desc_type)
        
        # define ir system
        if self.desc_type in ['global']:
            self.irhelper = GDIR(
                srch_lib=self.srch_lib,
                srch_method=self.srch_method,
                with_mtc=self.with_mtc,
                qk=self.qk,
                dk=self.dk,
                verbose=self.__VERBOSE__)
        else:
            assert self.desc_type in ['local'], \
                'Invalid desc_type argument:{}'.format(self.desc_type)
            raise NotImplementedError()


    """feed
    """
    def feed_query_from_path(
        self,
        path,
        max_num=-1):
        '''feed_query_from_path
        Args:
            path: path to saved features (.npy)
            max_num: max # of feature to load
        '''
        unique_id_list = U.load_unique_id_list_from_path(path)
        if max_num != -1:
            unique_id_list = unique_id_list[:max_num]
        nfeats = self.irhelper.feed_from_path(
            path=path,
            target = 'query',
            unique_id_list=unique_id_list)
        if self.__VERBOSE__:
            print('feed_query_from_path> # of feeded query features: {}'.format(len(nfeats)))
        return nfeats

    def feed_index_from_path(
        self,
        path,
        max_num=-1):
        '''feed_index_from_path
        Args:
            path: path to saved features (.npy)
            max_num: max # of feature to load
        '''
        unique_id_list = U.load_unique_id_list_from_path(path)
        if max_num != -1:
            unique_id_list = unique_id_list[:max_num]
        nfeats = self.irhelper.feed_from_path(
            path=path,
            target = 'index',
            unique_id_list=unique_id_list)
        if self.__VERBOSE__:
            print('feed_index_from_path> # of feeded index features: {}'.format(len(nfeats)))
        return nfeats
    
    def feed_query(
        self,
        data):
        '''
        data = [<str>uid, <numpy>feat]
        (e.g.) ['d1eeytyo2kd3eerori7eop', np.ndarray([2,2,4,5,2,6,6])]
        '''
        assert isinstance(data, list) or isinstance(data, tuple), \
            'Invalid argument type data: {}'.format(type(data))
        #assert isinstance(data[1], np.ndarray), \
        #    'Invalid argument type data[1]: {}'.format(type(data[1]))
        self.irhelper.feed(
            target='query',
            unique_id=data[0],
            feat=data[1])

    def feed_index(
        self,
        data):
        '''
        data = [<str>uid, <numpy>feat]
        (e.g.) ['d1eeytyo2kd3eerori7eop', np.ndarray([2,2,4,5,2,6,6])]
        '''
        assert isinstance(data, list) or isinstance(data, tuple), \
            'Invalid argument type data: {}'.format(type(data))
        self.irhelper.feed(
            target='index',
            unique_id=data[0],
            feat=data[1])


    """load feature
    """
    def load_feat_by_unique_id(
        self,
        unique_id,
        target,
        mtc=False):
        '''load single feature with unique id.
        '''
        assert isinstance(unique_id, str), \
            'Invalid argument type unique_id: {}'.format(type(unique_id))
        return self.irhelper.load_feat_by_unique_id(
            unique_id=unique_id,
            target=target,
            mtc=mtc)
    
    def load_feat_by_index(
        self,
        idx,
        target,
        mtc=False):
        '''load single feature with unique id.
        '''
        assert isinstance(idx, int), \
            'Invalid argument type index: {}'.format(type(idx))
        return self.irhelper.load_feat_by_index(
            idx=idx,
            target=target,
            mtc=mtc)
    

    """search
    """
    def search(
        self,
        x,
        top_k=None,
        score_method='cosim',
        weights=None):
        '''search
        '''
        if isinstance(x, np.ndarray):
            return self.__search_by_feat__(
                x,
                top_k=top_k,
                score_method=score_method,
                weights=weights)
        elif isinstance(x, str):
            return self.__search_by_unique_id__(
                x,
                top_k=top_k,
                score_method=score_method,
                weights=weights)
        else:
            raise ValueError('Invalid argument x: {}'.format(type(x)))

    def search_all(
        self,
        top_k=None,
        score_method='cosim',
        weights=None):
        '''search with all given queries
        '''
        return self.irhelper.search_all(
            top_k=top_k,
            score_method=score_method,
            weights=weights)
    
    def __search_by_unique_id__(
        self,
        query_id, 
        top_k,
        score_method,
        weights):
        '''search_by_unique_id
        unique_id must be id from queries.
        '''
        return self.irhelper.search_by_unique_id(
            query_id=query_id,
            top_k=top_k,
            kappa=self.qk,
            weights=weights)

    def __search_by_feat__(
        self,
        feat,
        top_k,
        score_method,
        weights):
        return self.irhelper.search_by_feat(
            feat=feat,
            top_k=top_k,
            score_method=score_method,
            weights=weights)

    """utils
    """
    def clean(self, target=None):
        '''clean features
        '''
        if target is not None:
            assert target in ('query', 'index')
            self.irhelper.irsys.fs[target].clean()
        else:
            self.irhelper.irsys.fs['query'].clean()
            self.irhelper.irsys.fs['index'].clean()

    def render_result(
        self,
        result):
        if isinstance(result, np.ndarray):
            result = result.tolist()
        rank_dict = dict()
        for k, v in enumerate(result):
            qid = self.idx2id(k, 'query')
            iids = [ self.idx2id(x, 'index') for x in v ]
            rank_dict.update({qid: iids}) 
        return rank_dict 

    def sample(
        self,
        target='query',
        idx=-1,
        mtc=False,
        ):
        return self.irhelper.sample(
            target=target,
            idx=idx,
            mtc=mtc)

    def id2idx(
        self,
        unique_id,
        target):
        assert isinstance(unique_id, str), \
            'Invalid argument unique_id: {}'.format(type(unique_id))
        return self.irhelper.id_to_idx_fn(unique_id, target)
                
    def idx2id(
        self,
        idx,
        target):
        if isinstance(idx, np.int64):
            idx = idx.item()
        assert isinstance(idx, int), \
            'Invalid argument idx: {}'.format(type(idx))
        return self.irhelper.idx_to_id_fn(idx, target)
    
    def get_data_length(self, target=None):
        if target is None:
            return self.irhelper.get_data_length('query') +\
                   self.irhelper.get_data_length('index')
        else:
            return self.irhelper.get_data_length(target)
    
   


if __name__ == "__main__":
    '''
    feed query
    feed_query_from_path
    feed_index
    feed_index_from_path
    '''
    feat = [ x for x in range(2048) ]
    feat = np.asarray(feat)
    config = {}
    config['srch_method'] = 'bf'
    config['srch_libs'] = 'sklearn'         # sklearn/flann
    config['desc_type'] = 'global'          # local / global
    irbench = IRBench(config)
    for i in range(5):
        irbench.feed_query('q{}'.format(i), feat)

    irbench.feed_from_path(
        target = 'query',
        path = './sample/npy')
    """
    for i in range(20):
        irbench.feed_directly('index', feat, 'i{}'.format(i))
    """
    print(irbench.irhelper.qidx_to_qid)
    print(irbench.irhelper.qid_to_qidx)
    
    

        



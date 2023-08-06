''' global_descriptor.py
IR System for local descriptor
'''

import os
import sys
import time
import random

import itertools
import abc
import numpy as np
from collections import Counter
from tqdm import tqdm
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

from irsys.feature_store import FeatureStore

__VERBOSE__ = True

class BaseSearch(metaclass=abc.ABCMeta):
    def __init__(
        self,
        with_mtc,
        qk,
        dk):
        self.fs = dict()
        self.fs['query'] = FeatureStore(with_mtc=with_mtc, qk=qk, dk=dk)
        self.fs['index'] = FeatureStore(with_mtc=with_mtc, qk=qk, dk=dk)
        self.qk = qk
        self.dk = dk
        
    def feed_from_batch(
        self,
        target,
        feat_list,
        unique_id_list):
        '''feed features to search system.
        index_feats: list of numpy array of index features, [np_arr1, np_arr2, np_arr3, ...]
        query_feats: list of numpy array of query features, [np_arr1, np_arr2, np_arr3, ...]
        '''
        assert isinstance(feat_list, list), 'type(index_feats) is not List.'
        if feat_list is None:
            return;
        tmp = [ self.fs[target].insert([ unique_id_list[k], feat_list[k] ], target) \
              for k, _ in enumerate(tqdm(feat_list)) ]
    
    def feed_from_single(
        self,
        target,
        feat,
        unique_id):
        '''feed feature one by one.
        '''
        if feat is None:
            return;
        self.fs[target].insert([unique_id, feat], target)
    
    @abc.abstractmethod
    def search_all(
        self,
        top_k,
        scoring,
        weights):
        '''get BF result from all given query ids.
        This requires excessive memory.
        Make sure top_k > kappa
        Returns:
            retrieved index indices sorted by similiarity.
        '''
    
    @abc.abstractmethod
    def search(
        self,
        query_feat,
        top_k,
        scoring,
        weights):
        '''
        Note that search one by one in BF is not efficient.
        '''

# Brute Force Search
class bfSearch(BaseSearch):
    def __init__(
        self,
        with_mtc,
        qk, dk):
        super(bfSearch, self).__init__(with_mtc, qk, dk)
    
    def __get_maiv_terms__(self, x, kappa):
        '''get maiv terms
        return maximally activated index vector(maiv)
        '''
        return np.argsort(x)[::-1][:kappa]

    def __calc_match_term_count__(self, x1, x2):
        return len(np.intersect1d(x1, x2, assume_unique=True).tolist())
 
    def search_all(
        self,
        top_k,
        score_method,
        weights):
        if score_method == 'cosim':
            query_feats = self.fs['query'].export(mtc=False)
            index_feats = self.fs['index'].export(mtc=False)
            if isinstance(query_feats, list):
                query_feats = np.asarray(query_feats)
            if isinstance(index_feats, list):
                index_feats = np.asarray(index_feats)
            assert query_feats.shape[1] == index_feats.shape[1], \
                'feature dimension of query: {}, index:{} does not match' \
                .format(index_feats.shape[1], query_feats.shape[1])
            # https://oss.navercorp.com/VisualSearch/simage-qlty/blob/master/evaluation.py
            # mAP could be differerent depending on the use of np.argsort() or python sort().
            # To Do: Check if the result of python sort() and np.argsort() is same or not.
            print('calculating cosine similarity score...')
            cosim = np.dot(query_feats, index_feats.T)
            return np.argsort(-cosim, axis=1)[:,:top_k] \
                   if top_k is not None \
                   else np.argsort(-cosim, axis=1)

        elif score_method == 'mtc':
            q_feats = self.fs['query'].export(mtc=True)
            i_feats = self.fs['index'].export(mtc=True)
            if isinstance(q_feats, list):
                q_feats = np.asarray(q_feats)
            if isinstance(i_feats, list):
                i_feats = np.asarray(i_feats)
            mtc = np.dot(q_feats, i_feats.T)
            return np.argsort(-mtc, axis=1)[:,:top_k] \
                   if top_k is not None \
                   else np.argsort(-mtc, axis=1)

    def search(
        self,
        query_feat,
        top_k,
        score_method,
        weights):
        if score_method == 'cosim':
            index_feats = self.fs['index'].export(mtc=False)
            if isinstance(query_feat, list):
                query_feats = np.asarray(query_feats)
            if isinstance(index_feats, list):
                index_feats = np.asarray(index_feats)
            cosim = np.dot(query_feat, index_feats.T)
            return np.argsort(-cosim, axis=0)[:top_k] \
                   if top_k is not None \
                   else np.argsort(-cosim, axis=0)

        if score_method == 'mtc':
            i_feats = self.fs['index'].export(mtc=True)
            q_feat = self.fs['query'].__get_maiv_terms__(query_feat, self.qk)
            if isinstance(q_feat, list):
                q_feat = np.asarray(q_feat)
            if isinstance(i_feats, list):
                i_feats = np.asarray(i_feats)
            mtc = np.dot(q_feat, i_feats.T)
            return np.argsort(-mtc, axis=0)[:top_k] \
                   if top_k is not None \
                   else np.argsort(-mtc, axis=0)

class fashionSearch(BaseSearch):
    '''This is special search class only for fashion.
    '''
    def __init__(
        self,
        with_mtc,
        qk, dk):
        super(fashionSearch, self).__init__(with_mtc, qk, dk)
 
    def search_all(
        self,
        top_k,
        score_method,
        weights):
        assert (isinstance(weights, tuple) or isinstance(weights, list)), \
               'Invalid argument weights: {}'.format(type(weights))
        if score_method == 'cosim':
            query_feats = self.fs['query'].export(mtc=False)
            index_feats = self.fs['index'].export(mtc=False)
            # get weighted cosine similarity for shape/texture/color
            cosim = None
            for i, w in enumerate(weights):
                q_feats = [ x[i] for x in query_feats ]
                i_feats = [ x[i] for x in index_feats ]
                if isinstance(query_feats, list):
                    q_feats = np.asarray(q_feats)
                if isinstance(index_feats, list):
                    i_feats = np.asarray(i_feats)
                assert q_feats.shape[1] == i_feats.shape[1], \
                    'feature dimension of query: {}, index:{} does not match' \
                    .format(i_feats.shape[1], q_feats.shape[1])
                if i == 0:
                    cosim = w * np.dot(q_feats, i_feats.T)
                else:
                    cosim = cosim + float(w) * np.dot(q_feats, i_feats.T)

            return np.argsort(-cosim, axis=1)[:,:top_k] \
                   if top_k is not None \
                   else np.argsort(-mtc, axis=1)
        
        elif score_method == 'mtc':
            query_feats = self.fs['query'].export(mtc=True)
            index_feats = self.fs['index'].export(mtc=True)
            mtc = None
            for i, w in enumerate(weights):
                q_feats = [ x[i] for x in query_feats ]
                i_feats = [ x[i] for x in index_feats ]
                if isinstance(q_feats, list):
                    q_feats = np.asarray(q_feats)
                if isinstance(i_feats, list):
                    i_feats = np.asarray(i_feats)
               
                tmp = np.dot(q_feats, i_feats.T)
                mtc = tmp if i == 0 else mtc + float(w)*tmp
            # sorting
            if __VERBOSE__:
                print('sorting by score...')
            return np.argsort(-mtc, axis=1)[:,:top_k] \
                   if top_k is not None \
                   else np.argsort(-mtc, axis=1)
            
    def search(
        self,
        query_feat,
        top_k,
        score_method,
        weights):
        assert (isinstance(weights, tuple) or isinstance(weights, list)), \
               'Invalid argument weights: {}'.format(type(weights))
        if score_method == 'cosim':
            raise NotImplementedError()
        if score_method == 'mtc':
            raise NotImplementedError()
        

# sklearn Search
class sklearnSearch(BaseSearch):
    def __init__(self):
        raise NotImplementedError()
    
    def search(self):
        raise NotImplementedError()

# Flann Search
class flannSearch(BaseSearch):
    def __init__(self):
        raise NotImplementedError()
    
    def search(self):
        raise NotImplementedError()

# IR Helper
class GlobalDescriptorIRHelper():
    def __init__(
        self,
        srch_lib,
        srch_method,
        with_mtc,
        qk=30, dk=120,
        verbose=False):
        '''GlobalDescriptorIRHelper
        '''
        # select ir system method.
        self.srch_lib = srch_lib
        self.srch_method = srch_method.lower()
        self.with_mtc = with_mtc
        self.qk = qk
        self.dk = dk
        __VERBOSE__ = verbose
        self.__feature_path__ = dict()
        if self.srch_method == 'bf':
            if self.srch_lib is None:
                self.irsys = bfSearch(
                    with_mtc=with_mtc,
                    qk=qk, dk=dk)
        elif self.srch_method == 'fashion':
            self.irsys = fashionSearch(
                with_mtc=with_mtc,
                qk=qk, dk=dk)
        else:
            raise ValueError('Invalid IR method {}!!!'.format(method))

    def __load_feature_from_path__(
        self,
        target,
        unique_id_list):
        '''load features from given unique_id list.
        '''
        assert target in self.__feature_path__, \
            'feed {} before load features.'.format(target)
        feat_list = [np.load(os.path.join(self.__feature_path__[target], x+'.npy'))
                    for x in unique_id_list]
        assert len(unique_id_list) == len(feat_list), \
            'error: len(unique_id_list) != len(feat_list)'
        return feat_list, unique_id_list

    def feed_from_path(
        self,
        path,
        target,
        unique_id_list):
        '''feed feaures to irsystem with unique id of images
        '''
        assert isinstance(unique_id_list, list), \
            'type(unique_id_list) is not List.'
        assert target in ['index', 'query'], \
            '[feed_from_path] Invalid target argument: {}'.format(target)
      
        self.__feature_path__[target] = path
        print('Loading {} features({}) from {}'\
            .format(target, len(unique_id_list), path))
        
        # update features.
        if __VERBOSE__:
            print('Feed batch {} features to {} IR System'.format(target, self.srch_method))
        feat_list, unique_id_list = self.__load_feature_from_path__(
            target=target,
            unique_id_list=unique_id_list)
        self.irsys.feed_from_batch(
            target=target,
            unique_id_list=unique_id_list,
            feat_list=feat_list)
        return len(feat_list)

    def feed(
        self,
        target,
        feat,
        unique_id):
        '''feed features to irsystem directly with feat and unique_id.
        '''
        # update features.
        #if __VERBOSE__:
        #    msg = 'Feed single {}({}) feature to {} IR System'
        #    print(msg.format(target, unique_id, self.srch_method))
        if target == 'query':
            kappa = self.qk
        else:
            kappa = self.dk

        self.irsys.feed_from_single(
            target=target,
            feat=feat,
            unique_id = unique_id)

    def load_feat_by_unique_id(
        self,
        unique_id,
        target,
        mtc=False):
        '''load single feature with unique id.
        '''
        assert target in ['query', 'index']
        assert self.irsys.fs[target].exist(unique_id), \
            'unique id {} not found. please do "feed" before "load"'.format(unique_id)
        idx = self.id_to_idx_fn(unique_id, target)
        return self.irsys.fs[target].read(idx)
    
    def load_feat_by_index(
        self,
        idx,
        target,
        mtc=False):
        '''load single feature with index
        '''
        assert target in ['query', 'index']
        return self.irsys.fs[target].read(idx, mtc)

    def search_all(
        self,
        top_k,
        score_method,
        weights=None):
        '''search with all given queries
        '''
        return self.irsys.search_all(
            top_k,
            score_method,
            weights)

    def search_by_unique_id(
        self,
        query_id,
        top_k,
        score_method,
        weights=None):
        '''search with single query id.
        '''
        qidx = self.id_to_idx_fn(query_id, 'query')
        if score_method=='mtc':
            q_feat = self.irsys.fs['query'].read(qidx, mtc=True)
        else:
            q_feat = self.irsys.fs['query'].read(qidx, mtc=False)
        return self.irsys.search(
            q_feat,
            top_k,
            score_method,
            weights)

    def search_by_feat(
        self,
        feat,
        top_k,
        score_method,
        weights=None):
        '''search with the feature directly.
        '''
        return self.irsys.search(
            feat,
            top_k,
            score_method,
            weights)

    def sample(
        self,
        target,
        idx,
        mtc):
        assert target in ['index', 'query'], '[sample] Invalid target argument: {}'.format(target)
        if idx == -1:
            idx = random.randrange(0, len(self.irsys.fs[target].__raw_features__))
        return (self.irsys.fs[target].read(idx, mtc=mtc),
                self.idx_to_id_fn(idx, target), idx)
       
    def idx_to_id_fn(
        self,
        idx,
        target):
        return self.irsys.fs[target].idx_to_id(idx)
    
    def id_to_idx_fn(
        self,
        _id,
        target):
        return self.irsys.fs[target].id_to_idx(_id)
    
    
    def get_data_length(self, target):
        return len(self.irsys.fs[target].__raw_features__)

if __name__ == '__main__':
    pass;




















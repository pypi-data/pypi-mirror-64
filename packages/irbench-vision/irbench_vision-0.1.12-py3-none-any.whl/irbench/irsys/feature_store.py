'''feature_store.py
'''

import numpy as np
from zlib import crc32

class FeatureStore(object):
    def __init__(
        self,
        with_mtc,
        qk, dk):
        '''FeatureStore
        '''
        self.__with_mtc__ = with_mtc
        self.qk = qk
        self.dk = dk
        self.clean()

    def __hash_str_to_float__(self, s, encoding="utf-8"):
        return 1e-3 * float(crc32(s.encode(encoding)) & 0xffffffff) / 2**32

    def __get_maiv_terms__(self, x, kappa, eps=0.0):
        '''get maiv terms
        return maximally activated index form the vector
        '''
        if isinstance(x, tuple):
            res = list()
            for i, _x in enumerate(x):
                t = np.zeros(_x.shape[0], dtype=np.int8)
                indices = np.argsort(_x)[::-1][:kappa]
                t[indices] = 1.0 + eps
                res.append(t)
            return tuple(res)
        else:
            t = np.zeros(x.shape[0], dtype=np.int8)
            indices = np.argsort(x)[::-1][:kappa]
            t[indices] = 1.0 + eps
            return t
   
    def clean(self):
        self.__idx_to_id__ = list()
        self.__id_to_idx__ = dict()
        self.__raw_features__ = list()
        self.__mtc_features__ = list()
        
    def insert(self, x, target):
        '''
        x = [unique_id, feat]
        '''
        assert isinstance(x, list) and len(x) == 2
        if target == 'query':
            kappa = self.qk
        elif target == 'index':
            kappa = self.dk
        
        uid, feat = x
        if not uid in self.__id_to_idx__:
            self.__id_to_idx__.update(
                { uid: len(self.__idx_to_id__) }
            )
            self.__idx_to_id__.append(uid)
            self.__raw_features__.append(feat)
            if self.__with_mtc__:
                self.__mtc_features__.append(self.__get_maiv_terms__(
                    feat,
                    kappa,
                    self.__hash_str_to_float__(uid)))
            return True
        else:
            print('duplicated unique id found: {}'.format(uid))
            return False

    def export(self, mtc=False):
        if mtc:
            return self.__mtc_features__
        else:
            return self.__raw_features__

    def read(self, idx, mtc=False):
        if mtc:
            return self.__mtc_fatures__[idx]
        else:
            return self.__raw_features__[idx]

    def idx_to_id(self, idx):
        return self.__idx_to_id__[idx]
    
    def id_to_idx(self, _id):
        return self.__id_to_idx__[_id]
    
    def delete(self):
        pass;

    def exist(self, uid):
        return uid in self.__id_to_idx__



"""
class FashionFeatureStore(FeatureStore):
    def __init__(
        self,
        with_mtc,
        qk, dk):
        super(FeatureStore, self).__init__(with_mtc, qk, dk)
       
    def clean(self):
        self.__idx_to_id__ = dict()
        self.__id_to_idx__ = dict()
        self.__raw_features__ = list()
        
        self.__raw_features__['shape'] = list()
        self.__raw_features__['texture'] = list()
        self.__raw_features__['color'] = list()
        self.__mtc_features__ = dict()
        self.__mtc_features__['shape'] = list()
        self.__mtc_features__['texture'] = list()
        self.__mtc_features__['color'] = list()
    
    def insert(self, x, target):
        '''
        x = [unique_id, (shape_feat, texture_feat, color_feat)]
        '''
        assert len(x) == 2
        assert isinstance(x[1], tuple) or isinstance(x[1], list)

        if target == 'query':
            kappa = self.qk
        elif target == 'index':
            kappa = self.dk
        uid, feat = x
        if not uid in self.__id_to_idx__:
            self.__id_to_idx__.update(
                { uid: len(self.__idx_to_id__) }
            )
            self.__idx_to_id__.append(uid)
            eslf.__raw_features_.append
            self.__raw_features__['shape'].append(feat[0])
            self.__raw_features__['texture'].append(feat[1])
            self.__raw_features__['color'].append(feat[2])
            if self.__with_mtc__:
                self.__mtc_features__['shape'].append(self.__get_maiv_terms__(feat[0], kappa))
                self.__mtc_features__['texture'].append(self.__get_maiv_terms__(feat[1], kappa))
                self.__mtc_features__['pattern'].append(self.__get_maiv_terms__(feat[2], kappa))
            return True
        else:
            print('duplicated unique id found: {}'.format(uid))
            return False
"""
    

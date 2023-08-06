'''evaluate.py
evalutate mAP
'''

import csv
import json

import tqdm

__DEBUG__ = False



class PureInstanceRetrieval(object):
    '''For Instance Retrieval
    '''
    @staticmethod
    def compute_AP(
        pos_list,
        junk_list,
        rank_list,
        kappa):
        '''
        Ignore junk images if exists.
        reference: https://sites.google.com/site/hyunguk1986/personal-study/-ap-map-recall-precision
        reference: http://www.robots.ox.ac.uk/~vgg/data/oxbuildings/compute_ap.cpp
        '''
        num_pos_list = len(pos_list)
        if kappa is not None:
            rank_list = rank_list[:kappa]
            num_pos_list = min(num_pos_list, kappa)
    
        old_recall = 0.
        old_precision = 1.
        ap = 0.
    
        intersect_size = 0
        j = 0
        for i, rank in enumerate(rank_list):
            if rank in junk_list:
                continue;
            if rank in pos_list:
                intersect_size += 1
            
            j += 1.
            recall = intersect_size / float(num_pos_list)
            precision = intersect_size / float(j)
    
            ap += (recall - old_recall) * ((old_precision + precision)/2.)      # area of trapezoidal.
            #ap += (recall - old_recall) * (precision)                          # area of outer rectangle
       
            # udpate recall and precision.
            old_recall = recall
            old_precision = precision
            
            # escape if recall == 1.0
            if intersect_size >= num_pos_list:
                break;
    
        return ap, recall, precision
    
    
    @staticmethod
    def compute_mAP(
        rank_dict,
        gt_dict,
        indiv = True,
        kappa = None):
        '''compute mAP given set of return results.
        Args:
            gt_dict: Ground Truth json object.
            {
                <query_unique_id>: {
                    'positive': [ pos1, pos2, pos3, ... ],
                    'junk': [ junk1, junk2, junk3, ... ]
            }
            rank_dict: Prediction json object.
            {
                <query_unique_id>: [ rank1, rank2, rank3, ... ]
            }
        '''
        result = dict()
        result['overall'] = dict()
        if indiv:
            result['indiv'] = dict()
    
        mAP = 0.
        Precision = 0.
        Recall = 0.
        ncnt = 0
                
        for uid, rank_list in rank_dict.items():
            if not uid in gt_dict:
                print('no {} key exists in gt_dict'.format(uid))
                continue;   # if id not exists in GT, skip.
            pos_list =gt_dict[uid]['positive']
            junk_list = []       # ignore junk.
                
            # if GT list is empty, skip.
            if len(pos_list) > 0:
                ap, recall, precision = PureInstanceRetrieval.compute_AP(
                    pos_list,
                    junk_list,
                    rank_list,
                    kappa)
                
                mAP = mAP + ap
                Recall = Recall + recall
                Precision = Precision + precision
                ncnt = ncnt + 1
                
                if indiv:
                    if not uid in result['indiv']:
                        result['indiv'][uid] = dict()
                    data = dict()
                    data['ap'] = ap
                    data['recall'] = recall
                    data['precision'] = precision
                    result['indiv'][uid].update(data)
            else:
                print('no ground-truth was found for query: {}'.format(uid))
        
        
        # calc. ooveralll 
        kappa = 'All' if kappa is None else kappa
        mAP = mAP / float(ncnt)
        Precision = Precision / float(ncnt)
        Recall = Recall / float(ncnt)
        result['overall']['mAP'] = mAP
        result['overall']['recall'] = Recall
        result['overall']['precision'] = Precision
    
        return result, kappa
    
    @staticmethod
    def compute_top_k_acc(
        rank_dict,
        gt_dict,
        kappa=None):
        """compute top-k retrieval accuracy.
        """
        result = dict()
        hit = 0
        ncnt = 0
        for uid, rank_list in rank_dict.items():
            if not uid in gt_dict:
                print('no {} key exists in gt_dict'.format(uid))
                continue;   # if id not exists in GT, skip.
            pos_list =gt_dict[uid]['positive']
            junk_list = []       # ignore junk.
            
            # if GT list is empty, skip.
            if len(pos_list) > 0:
                rank_list = rank_list[:kappa] if kappa is not None else rank_list
                # hit if at least one gt exists in rank list.
                inter_sect = list(set(rank_list).intersection(pos_list))
                ncnt = ncnt + 1
                if len(inter_sect) > 0:
                    hit = hit + 1

        kappa = 'All' if kappa is None else kappa
        top_k_acc = hit / float(ncnt)
        result['top_k_acc'] = top_k_acc
        return result, kappa 

class AttributeManipulation(object):
    ''' For Attribute Mainpulation
    ref: Memory-Augmented Attribute Manipulation Networks for Interactive Fashion Search
    '''
    @staticmethod
    def compute_NDCG(
        inv_gt_json,
        rank_json,
        kappa=5):
        '''
        NDCG@k = \sum_{j=1}^{k}\frac{ 2^{rel(j)-1} }{log(j+1)}
        
        inv_gt_json: {
            <query_unique_id>: {
                'positive': [attr1, attr2, attr3]
            }
        }
        '''
        for targ_attr, res_dict in rank_json.items():
            for q_id, rank_dict in res_dict.items():
                for attr_key, rank_list in rank_dict.items():
                    assert attr_key in gt_json, 'attr_key "{}" does not exist in gt_json!!!'.format(attr_key)
                    gt_list = gt_json[attr_key]['positive']
                    for r_id in rank_list:
                       pass; 
    
    @staticmethod
    def compute_mAP(
        gt_json,
        rank_json,
        kappa=5):
        """compute top-k retrieval accuracy.
        we consider a hit if the method finds
        at least one clothing image with exactly
        the same attributes as indicated by the query 
        in top-k result. 
        
        Args:
            gt_json: Ground Truth json object.
            {
                <attr_comb_key>: {
                    'positive': [ pos1, pos2, pos3, ... ],
                }
            }
            rank_json: Prediction json object.
            {
                <targ_attr>: {
                    <query_unique_id>: {
                        <attr_comb_key1>: [rank1, rank2, rank3, ...],
                        <attr_comb_key2>: [rank1, rank2, rank3, ...],
                        <attr_comb_key3>: [rank1, rank2, rank3, ...],
                        <attr_comb_key4>: [rank1, rank2, rank3, ...],
                        <attr_comb_key5>: [rank1, rank2, rank3, ...],
                    }
                }
            }
        """
        res_map = {}
        all_cnt = 0
        all_mAP = 0.
        qq = []
        ss = []
        for targ_attr, res_dict in tqdm.tqdm(rank_json.items()):
            mAP = 0.
            cnt = 0
            for q_id, rank_dict in tqdm.tqdm(res_dict.items()):
                for attr_key, rank_list in rank_dict.items():
                    if attr_key in gt_json:
                        gt_list = gt_json[attr_key]['positive']
                        ap = compute_AP(gt_list, [], rank_list, kappa=kappa)
                        mAP = mAP + ap
                        cnt = cnt + 1
                    else:       # skip if attr_key does not exists in gt.
                        continue;
            all_mAP = all_mAP + mAP
            all_cnt = all_cnt + cnt
            mAP = mAP / cnt
            res_map[targ_attr] = mAP
        res_map['all'] = all_mAP / all_cnt
        return res_map          
    
    @staticmethod
    def compute_top_k_acc(
        gt_json,
        rank_json,
        kappa=5):
        """compute top-k retrieval accuracy.
        we consider a hit if the method finds
        at least one clothing image with exactly
        the same attributes as indicated by the query 
        in top-k result. 
        
        Args:
            gt_json: Ground Truth json object.
            {
                <attr_comb_key>: {
                    'positive': [ pos1, pos2, pos3, ... ],
                }
            }
            rank_json: Prediction json object.
            {
                <targ_attr>: {
                    <query_unique_id>: {
                        <attr_comb_key1>: [rank1, rank2, rank3, ...],
                        <attr_comb_key2>: [rank1, rank2, rank3, ...],
                        <attr_comb_key3>: [rank1, rank2, rank3, ...],
                        <attr_comb_key4>: [rank1, rank2, rank3, ...],
                        <attr_comb_key5>: [rank1, rank2, rank3, ...],
                    }
                }
            }
        """
        res_acc = {}
        all_cnt = 0
        all_hit = 0.
        qq = []
        ss = []
        for targ_attr, res_dict in tqdm.tqdm(rank_json.items()):
            hit = 0.
            cnt = 0
            for q_id, rank_dict in tqdm.tqdm(res_dict.items()):
                for attr_key, rank_list in rank_dict.items():
                    if attr_key in gt_json:
                        gt_list = gt_json[attr_key]['positive']
                        inter_sect = list(set(rank_list[:kappa]).intersection(gt_list))
                        # hit if at least one attribute matched image is found.
                        cnt = cnt + 1
                        if len(inter_sect) > 0:
                            hit = hit + 1
                    else:       # skip if attr_key does not exists in gt.
                        continue;
            all_cnt = all_cnt + cnt
            all_hit = all_hit + hit
            res_acc[targ_attr] = hit/float(cnt)
        res_acc['all'] = all_hit / float(all_cnt)
        
        return res_acc


if __name__ == "__main__":
    gt_json = {
        'shirts.blue.checked': {
            'positive': ['a1','a2','a3','a4','a5','a6']
        },
        'shirts.yellow.checked': {
            'positive': ['b1','b2','b3','b4','b5','b6']
        },
        'shirts.green.checked': {
            'positive': ['c1','c2','c3','c4','c5','c6']
        },
        'coats.blue.checked': {
            'positive': ['d1','d2','d3','d4','d5','d6']
        },
        'onepiece.blue.checked': {
            'positive': ['e1','e2','e3','e4','e5','e6']
        },
        'shirts.blue.flower': {
            'positive': ['f1','f2','f3','f4','f5','f6']
        },
        'shirts.blue.dot': {
            'positive': ['g1','g2','g3','g4','g5','g6']
        },
    }
    rank_json = {
        'color': {
            'q1': {
                'shirts.blue.checked': ['a1','a3','b1','b8','c3','a2','h7'],
                'shirts.yellow.checked': ['g1','u8','b1','a7','j3','e4','p7'],
                'shirts.green.checked': ['a6','a4','c2','n6','d1','h2','a5'],
            }
        },
        'shape': {
            'q1': {
                'shirts.blue.checked': ['e1','a6','f1','b8','f3','a2','h7'],
                'coats.blue.checked': ['g1','u8','b1','d7','j3','d4','e7'],
                'onepiece.blue.checked': ['e6','e4','e2','n6','d1','h2','a5'],
            }
        },
        'pattern': {
            'q1': {
                'shirts.blue.checked': ['a1','a3','b1','b8','a3','a2','h7'],
                'shirts.blue.flower': ['f1','f2','b1','a7','j3','e4','p7'],
                'shirts.blue.dot': ['g5','a4','g2','n6','d1','h2','a5'],
            }
        },
    }
    acc = am_compute_mAP(
        gt_json,
        rank_json)
    print(acc) 




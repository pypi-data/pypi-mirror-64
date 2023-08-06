

import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

import utils.utils as utils
from evals.evaluate import (PureInstanceRetrieval,
                            AttributeManipulation)

__DEBUG__ = True

class EvalHelper(object):
    def __init__(
        self):
        self.rank_dict = dict()
        self.gt_dict = dict()
        pass;
    
    def feed_gt_from_path(
        self,
        path):
        print('load json file from {}'.format(path))
        gt_dict = utils.load_dict_from_path(path)
        self.feed_gt_from_dict(gt_dict)
    
    def feed_rank_from_path(
        self,
        path):
        print('load json file from {}'.format(path))
        rank_dict = utils.load_dict_from_path(path)
        self.feed_rank_from_dict(rank_dict)

    def feed_gt_from_dict(
        self,
        gt_dict):
        assert isinstance(gt_dict, dict), \
            'Invalid gt_dict argument type: {}'.format(type(gt_dict))
        try:
            for k, v in gt_dict.items():
                if not 'positive' in v:
                    raise ValueError('no "positive" field in gt data.')
                break;
            self.gt_dict = gt_dict
        except Exception as e:
            raise ValueError(e)
    
    def feed_rank_from_dict(
        self,
        rank_dict):
        assert isinstance(rank_dict, dict), \
            'Invalid rank_dict argument type: {}'.format(type(rank_dict))
        try:
            for k, v in rank_dict.items():
                if not isinstance(v, list):
                    raise ValueError('Invalid rank dictionary format')
            self.rank_dict = rank_dict
        except Exception as e:
            raise ValueError(e)

    def feed_gt(
        self,
        data):
        '''
        ('<q_id>', [<i_id1>, <i_id2>, ...])
        '''
        assert (isinstance(data, list) or isinstance(data, tuple)), \
            'Argument type data must be tuple or list: {}'.format(type(data))
        new_data = {
            data[0]: {
                'positive': data[1],
                'junk': None
            }
        }
        self.gt_dict.update(new_data)

    def feed_rank(
        self,
        data):
        '''
        ('<q_id>', [<i_id1>, <i_id2>, ...])
        '''
        assert (isinstance(data, list) or isinstance(data, tuple)), \
            'Argument type data must be tuple or list: {}'.format(type(data))
        new_data = {
            data[0]: data[1]
        }
        self.rank_dict.update(new_data)

    def evaluate(
        self,
        metric=['mAP'],
        kappa=None,
        indiv=False):
        '''evaluate
        metric: mAP / Precision / Recall / Top_k_accuracy
        indiv: True will return metric result per each individual query.
        '''
        if __DEBUG__:
            print('--------------------- config ----------------------')
            print('metric: {}'.format(metric))
            print('kappa: {}'.format(kappa))
            print('indiv: {}'.format(indiv))
            print('---------------------------------------------------')
       
        if isinstance(metric, str):
            metric = [ metric ]
        if (kappa is None) or (isinstance(kappa, int)):
            kappa = [ kappa ]
        assert isinstance(kappa, list), \
            'Invalid argument type kappa: {}'.format(type(kappa))
        
        # multi-threading.
        submit_list = []
        thread_pool = ThreadPoolExecutor(max_workers = min(len(kappa), 10))
       
        ret = []
        for m in metric:
            if m.lower() == 'map':
                for k in kappa:
                    s = thread_pool.submit(
                        PureInstanceRetrieval.compute_mAP,
                        self.rank_dict,
                        self.gt_dict,
                        indiv,
                        k)
                    submit_list.append(s)
                
                result = dict()
                completed = concurrent.futures.as_completed(submit_list)
                for x in completed:
                    res = x.result()
                    result.update({str(res[1]):res[0]})
                ret.append(result)
            
            elif m.lower() == 'top_k_acc':
                for k in kappa:
                    s = thread_pool.submit(
                        PureInstanceRetrieval.compute_top_k_acc,
                        self.rank_dict,
                        self.gt_dict,
                        k)
                    submit_list.append(s)
                
                result = dict()
                completed = concurrent.futures.as_completed(submit_list)
                for x in completed:
                    res = x.result()
                    result.update({str(res[1]):res[0]})
                ret.append(result)

        return ret
        
        

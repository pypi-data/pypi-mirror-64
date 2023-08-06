'''utils.py
'''
import os
import sys
import time
import random
import csv
import json
import glob

import pickle
import uuid
import numpy as np

__DEBUG__ = False

def mkdir_p(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_file(path, mode='npy'):
    assert mode in ['npy', 'pickle']
    if mode == 'npy':
        raise ValueError('numpy')
    elif mode == 'pickle':
        raise ValueError('pickle')

def load_pil_image(path):
    with open(path, 'rb') as f:
        return Image.open(f).convert('RGB')

def save_pil_image(path):
    raise NotImplementedError()

def visualize_ransac_match(img1, img2, kp1, kp2):
    raise NotImplementedError()

def visualize_correspondance_match(img1, img2, kp1, kp2):
    raise NotImplementedError()

def read_file(path):
    raise NotImplementedError()

def convert_indices_list_to_ids_list(indices_list, idx_to_iid_fn):
    '''convert indices_list to index_ids_list
    '''
    result_ids_list = []
    if len(indices_list.shape) == 1:
        indices_list = [ indices_list ]
    for i, indices in enumerate(indices_list):
        ids = [ idx_to_iid_fn(x) for x in indices ]
        t = [ x for x in indices ]
        result_ids_list.append(ids)
    return result_ids_list

def save_submission(
    path,
    filename,
    query_id_list,
    rank_ids_list,):
    '''save rank result to submission file format.
    '''
    # make sure path exist.
    mkdir_p(path)
   
    # save submission file.
    f = open(os.path.join(path, filename), 'w', encoding ='utf-8', newline='')
    wr = csv.writer(f, delimiter=' ', escapechar=' ', quoting=csv.QUOTE_NONE)
    for idx, rank_ids in enumerate(rank_ids_list):
        msg = []
        msg.append(query_id_list[idx])
        msg.append(','.join(rank_ids))
        wr.writerow(msg)
    f.close()
    print('saved submission file @ {}'.format(os.path.join(path, filename)))


def load_submission(path):
    '''return json object.
    Input file format:
        <query_unique_id1> <uid11>,<uid12>,<uid13>,...
        <query_unique_id2> <uid21>,<uid22>,<uid23>,...
        <query_unique_id3> <uid31>,<uid32>,<uid33>,...
    Return json format:
        {
            <query_unique_id1>: [ uid11, uid12, uid13, ... ]
            <query_unique_id2>: [ uid21, uid22, uid23, ... ]
            <query_unique_id3>: [ uid31, uid32, uid33, ... ]
        }
    '''
    json_list = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            tmp = line.split(' ')
            if len(tmp) > 1: # skip if no GT positive images found.
                q_id = tmp[0].strip()
                c_ids = tmp[1].strip().split(',')
                json_list[q_id] = c_ids
    return json_list

def load_unique_id_list_from_file(file_path):
    '''load_unique_id_list_from_file
    read list of query and index images form csv file.
    '''
    # query id list
    with open(file_path, 'r', encoding='utf-8') as f:
        rdr = csv.reader(f)
        unique_id_list = [ str(line[0].strip()) for line in rdr ]
        return unique_id_list

def load_unique_id_list_from_path(path):
    '''load_unique_id_list_from_path
    read list of query and index images form csv file.
    '''
    #assert ext is not None, 'ext is not specified'
    image_list = glob.glob(os.path.join(path, '*.npy'))
    unique_id_list = list(set([os.path.splitext(os.path.basename(x))[0] for x in image_list]))
    return unique_id_list

def load_dict_from_path(path):
    with open(path) as json_file:
        return json.load(json_file)
    
def generate_unique_id():
    return str(uuid.uuid4()).replace('-','')

def calculate_avg_prec(lgt, lpred, kappa):
    '''calculate AP given single query.
    Args:
        lgt: list of GT positive unique_ids
        lpred: list of retrieved unique_ids
    Returns:
        ap: average precision
    '''
    # evaluate top_k result only
    num_lgt = 0
    if kappa is None:
        num_lgt =len(lgt)
    else:
        num_lgt = min(kappa, len(lgt))

    ap = 0.
    lpred = lpred[:num_lgt]
    lcorrect = [ x for x in lpred if x in lgt ]
    ap = len(lcorrect) / float(num_lgt)

    if __DEBUG__:
        print('ap:{:.4f} %'.format(ap*100))

    return ap

if __name__ == '__main__':
    pass;
    
    


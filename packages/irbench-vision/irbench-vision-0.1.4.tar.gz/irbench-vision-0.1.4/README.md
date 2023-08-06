# irbench
A library for benchmarking Image Retrieval Performance.

### Principals
+ All features feeded in irbench must be np.ndarray, size=(<feat_dims>)
+ srch_method='cosim' assumes all features are normalized. (if not, the result will collapse)
+ feed_query_from_path / feed_index_from_path uses the filename as unique id for the feature. 

### Get Started
Here is the simple example code to get started.    
Refer to the `FUNCITONS.md` for more detailed use.   
The example code assumes the features were saved in directory with `.npy` format.

~~~python
import pprint
import numpy as np

from irbench.irbench import IRBench

# initialize irbench.
ir_config = {}
ir_config['srch_method'] = 'bf'
ir_config['srch_libs'] = None
ir_config['desc_type'] = 'global'
irbench = IRBench(ir_config)

# feed query from path.
QUERY_PATH = './sample/query'
INDEX_PATH = './sample/index'
irbench.feed_query_from_path(QUERY_PATH, max_num=10)
irbench.feed_index_from_path(INDEX_PATH, max_num=100)

# search (bf, cosim)
res = irbench.search_all(top_k=10)
res = irbench.render_result(res)
pprint.pprint(res)
~~~


### For developers
Editable installation:
~~~
cd <path_to_irbench_repo>
pip install -e .
~~~

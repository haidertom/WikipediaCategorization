#Here we can do some coding

import json
from pprint import pprint
with open('../Baseline/zz_index.json') as f:
    data = json.load(f)
print(data)
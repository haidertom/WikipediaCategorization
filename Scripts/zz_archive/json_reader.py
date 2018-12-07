import json
from pprint import pprint

with open('../DataSnippets/json_splits/0_wiki_part.json') as f:
    data = json.load(f)


print(data[1]['revision']['text'])

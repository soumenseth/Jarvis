import json
import os
import pandas as pd
from datasets import load_dataset
import pyarrow as pa
import pyarrow.dataset as ds
from paths import *
from constants import *

def read_json(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return [] if data == "" else json.loads(data)

def write_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f)

def check_and_create_dir(dir_path):
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
        
def get_dataset(json_file):
    # df = pd.read_json(json_file)
    # train, test = train_test_split(df, test_size=0.2)
    
    # dataset = DatasetDict({
    #     "train": Dataset(pa.Table.from_pandas(train)),
    #     "test": Dataset(pa.Table.from_pandas(test))
    #     })
    dataset = load_dataset("yelp_review_full")
    return dataset

def check_common(list_a, list_b):
    common_elements = set(list_a).intersection(set(list_b))
    return len(common_elements) > 0

### Jarvis utils

def open_terminal(platform):
    return SCRIPT_COMMAND[platform["open_terminal"]]

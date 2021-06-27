# coding=utf8


import json
import time
import os
import random
import numpy as np
import requests
from tqdm import tqdm
from get_detail_score import get_school_score


def run(in_dir, out_path):
    school_list= get_schs(in_dir)
    visited = _get_crawled(out_path)
    print(len(school_list))
    with open(out_path, "a") as out_:
        for sch_info in tqdm(school_list):
            if sch_info["school_id"] not in visited:
                detail_info = get_school_score(sch_info)
                if detail_info is None:
                    print("failed info is:")
                    print(sch_info)
                out_line = json.dumps(detail_info, ensure_ascii=False)
                out_.write(out_line + "\n")
                sep = get_time_sep()
                time.sleep(sep)
            else:
                print("the value is parsed")
                print(sch_info["name"])


def get_time_sep():
    sep = np.random.randint(2, 7)
    sep = sep + random.random()
    return sep


def _get_crawled(f_path):
    res = set()
    if not os.path.exists(f_path):
        return res
    with open(f_path) as in_:
        key = "school_id"
        for line in in_:
            line = line.strip()
            obj = json.loads(line)
            res.add(obj[key])
    return res


def get_schs(in_dir):
    f_list = os.listdir(in_dir)
    res = []
    for f_name in f_list:
        if f_name.startswith("sch_info"):
            f_path = os.path.join(in_dir, f_name)
            with open(f_path) as in_:
                for line in in_:
                    line = line.strip()
                    if len(line) > 2:
                        obj = json.loads(line)
                        res.append(obj)
    return res


if __name__ == "__main__":
    in_dir = "sch_dir"
    out_path = "total_school_score_det.json"
    run(in_dir, out_path)

# coding=utf8

import json
import numpy as np


def analysis(rank_path, query_rank):
    tot_rank_info = _get_all_rank(rank_path)
    save_failed_info(tot_rank_info, "faild_scool.json")
    arr_ = _get_safe_candidates(tot_rank_info, query_rank) 
    save_info(arr_, "save_cand.json")
    arr_ = _get_min_safe_candidate(tot_rank_info, query_rank)
    save_info(arr_, "little_safe_cand.json")
    arr_ = _get_some_chance_candidate(tot_rank_info, query_rank)
    save_info(arr_, "some_chance_can.json")
    sort_and_save(tot_rank_info, "tot_sorted_rank.json")


def sort_and_save(tot_ranks,  f_path):
    res = []
    for rank_info in tot_ranks:
        stat_info = rank_info['stat']
        if stat_info is None:
            continue
        res.append(rank_info)
    s_res = cus_sort(res, rev=False)
    save_info(s_res, f_path)




def _get_safe_candidates(tot_ranks, query_rank):
    res = []
    for rank_info in tot_ranks:
        stat_info = rank_info['stat']
        if stat_info is None:
            continue
        max_, min_, avg, std = stat_info
        if query_rank < min_:
            res.append(rank_info)
        elif query_rank < avg - 1.5 * std:
            res.append(rank_info)
    s_res = cus_sort(res, rev=False)
    return s_res


def _get_min_safe_candidate(tot_ranks, query_rank):
    res = []
    for rank_info in tot_ranks:
        stat_info = rank_info['stat']
        if stat_info is None:
            continue
        max_, min_, avg, std = stat_info
        if query_rank < max_:
            res.append(rank_info)
        elif query_rank < avg + 1.5 * std:
            res.append(rank_info)
    s_res = cus_sort(res, rev=False)
    return s_res


def _get_some_chance_candidate(tot_ranks, query_rank):
    qurey_rank = query_rank - 500
    res =  _get_safe_candidates(tot_ranks, query_rank)
    return res


def cus_sort(rank_arr, rev):
    res = sorted(rank_arr, key=lambda x: x['stat'][2], reverse=rev)
    return res

def save_info(info_arr, f_path):
    with open(f_path, "w") as out_:
        for info in info_arr:
           l = json.dumps(info, ensure_ascii=False)
           out_.write(l + "\n")


def save_failed_info(tot_info, f_path):
    with open(f_path, 'w') as out_:
        for cur_info in tot_info:
            stat = cur_info['stat']
            if stat is None:
                l = json.dumps(cur_info, ensure_ascii=False)
                out_.write(l + "\n")


def _get_all_rank(rank_path):
    res = []
    year_arr = ['2016', '2017', '2018', '2019', '2020']
    with open(rank_path) as in_:
        for line in in_:
            line = line.strip()
            if len(line) > 2:
                obj = json.loads(line)
                tmp_score_arr = []
                for y in year_arr:
                    if y in obj:
                        if obj[y] is not None:
                            score_info = obj[y]
                            if 'min_section' in score_info:
                                if score_info['min_section'] != '0' and score_info['min_section'] != '-':
                                    tmp_score_arr.append(int(score_info['min_section']))
                static_info = _get_static(tmp_score_arr) 
                obj['stat'] = static_info
                res.append(obj)
    return res


def _get_static(score_arr):
    if len(score_arr) == 0:
        return None
    max_ = max(score_arr)
    min_ = min(score_arr)
    avg = sum(score_arr) / len(score_arr)
    std = np.std(score_arr, ddof=1)
    return [max_, min_, avg, std]


if __name__ == '__main__':
    rank_path = 'total_school_score_det.json'
    query_rank = 29250
    analysis(rank_path, query_rank)


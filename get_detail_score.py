# coding=utf8

import time
import random
import numpy as np
import requests


def get_school_score(school_info):
    year_arr = [2016, 2017, 2018, 2019, 2020]
    res = {}
    res.update(school_info)
    for y in year_arr:
        try:
            page_cont = _download_page(y, school_info['school_id'])
        except Exception as e:
            print(e)
            return None
        score_info = _parse_page(page_cont)
        res[y] = score_info
        sep = get_time_sep()
        time.sleep(sep)
    return res


def get_time_sep():
    sep = np.random.randint(1, 4)
    sep = sep + random.random()
    return sep


def _download_page(year, sch_id):
    url = f"https://static-data.eol.cn/www/2.0/schoolprovinceindex/{year}/{sch_id}/42/1/1.json"
    payload = {}
    headers = {
      'Connection': 'keep-alive',
      'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
      'Accept': 'application/json, text/plain, */*',
      'sec-ch-ua-mobile': '?0',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
      'Origin': 'https://gkcx.eol.cn',
      'Sec-Fetch-Site': 'same-site',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Dest': 'empty',
      'Referer': 'https://gkcx.eol.cn/',
      'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()


def _parse_page(page_content):
    page_dict = page_content
    if 'data' not in page_dict:
        print("may failed for the page_content")
        return None
    res = {}
    keys = ["min_section", "min", "average", "local_batch_name", "zslx_name"]
    item = page_dict["data"]["item"][0]
    for key in keys:
        res[key] = item[key]
    return res


if __name__ == "__main__":
    t_y = 2016
    t_id = 76
    t_page_cont = _download_page(t_y, t_id)
    t_info = _parse_page(t_page_cont)
    print(t_info)

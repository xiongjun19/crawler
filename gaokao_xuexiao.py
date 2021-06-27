# coding=utf8


import requests
import json


def get_school_list(file_prefix, page_num=0):
    out_file_name = f'{file_prefix}_{page_num}.json'
    school_list_page = _download_page(page_num)
    res = _parse_page(school_list_page)
    with open(out_file_name, "w") as out_:
        for item in res:
            out_line = json.dumps(item, ensure_ascii=False)
            out_.write(out_line + "\n") 


def _download_page(page_num):
    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'Accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://gkcx.eol.cn',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://gkcx.eol.cn/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    params = (
        ('access_token', ''),
        ('admissions', ''),
        ('central', ''),
        ('department', ''),
        ('dual_class', ''),
        ('f211', ''),
        ('f985', ''),
        ('is_doublehigh', ''),
        ('is_dual_class', ''),
        ('keyword', ''),
        ('nature', ''),
        ('page', f'{page_num}'),
        ('province_id', ''),
        ('ranktype', ''),
        ('request_type', '1'),
        ('school_type', ''),
        ('signsafe', ''),
        ('size', '20'),
        ('sort', 'view_total'),
        ('top_school_id', '/[318/]'),
        ('type', ''),
        ('uri', 'apidata/api/gk/school/lists'),
    )
    data_dict = {"access_token":"","admissions":"","central":"","department":"","dual_class":"","f211":"","f985":"","is_doublehigh":"","is_dual_class":"","keyword":"","nature":"","page":page_num,"province_id":"","ranktype":"","request_type":1,"school_type":"","size":20,"sort":"view_total","top_school_id":"[318]","type":"","uri":"apidata/api/gk/school/lists"}
    data=json.dumps(data_dict)
    response = requests.post('https://api.eol.cn/gkcx/api/', headers=headers, params=params, data=data)
    print(response.json())
    return response.json()


def _parse_page(page_content):
    # page_dict = json.loads(page_content)
    page_dict = page_content
    item_arr = page_dict["data"]["item"]
    res = []
    keys = ['name', 'province_name', 'rank', 'school_id']
    for item in item_arr:
        tmp_res = {}
        for key in keys:
            tmp_res[key] = item[key]
        res.append(tmp_res)
    return res




if __name__ == '__main__':
    file_prefix = 'sch_dir/sch_info'
    get_school_list(file_prefix, 136)



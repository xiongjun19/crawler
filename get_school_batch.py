# coding=utf8


import numpy as np
import random
import time
from gaokao_xuexiao import get_school_list


def get_all_pages(num, prefix):
    for i in range(num):
        get_school_list(prefix, i+1)
        sep = get_time_sep()
        print(sep)
        time.sleep(sep)


def get_time_sep():
    sep = np.random.randint(1, 8)
    sep = sep + random.random()
    return sep


if __name__ == '__main__':
    file_prefix = 'sch_dir/sch_info'
    num = 20
    get_all_pages(num, file_prefix)


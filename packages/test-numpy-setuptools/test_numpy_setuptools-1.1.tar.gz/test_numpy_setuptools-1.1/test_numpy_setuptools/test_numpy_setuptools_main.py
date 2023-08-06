# -*- coding: utf-8 -*-

import numpy as np
import sys
import test_numpy_compile_pyd_multi

def func(a, b):
    say_hello(a)
    ret_list(a, b)
    result = np.sqrt(test_numpy_compile_pyd_multi.multiplication(int(a), int(b)))
    return result


def say_hello(s):
    s = "hello walle 2020! Received: " + str(s)
    print("say_hello: " + s)
    return s


def ret_list(a, b):
    li = [a, b]
    print(li)
    return li


if __name__ == '__main__':
    if len(sys.argv)<3:
        sys.argv = [2, 3, 2]

    print(func(sys.argv[1], sys.argv[2]))
    # print(say_hello(sys.argv[1]))

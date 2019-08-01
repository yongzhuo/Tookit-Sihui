# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/7/30 21:53
# @author   :Mo
# @function :

a1 = {'的':12, '我':1000, '你':199877766}
a2 = {'的':126, '我':10010, '你men':199877766}
a3 = dict(a1, **a2)
gg = 0


x = {'apple':1,'banana':2}
y = {'banana':10,'pear':11, 'apple':100}
def func(dict1,dict2):
    for i,j in dict2.items():
        if i in dict1.keys():
            dict1[i] += j
        else:
            dict1.update({f'{i}' : dict2[i]})
    return dict1
z = func(x, y)
gg = 0
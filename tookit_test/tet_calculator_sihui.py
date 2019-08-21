# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/8/22 0:53
# @author   :Mo
# @function :


from tookit_sihui.task.calculator_sihui.calcultor_sihui import calculator_sihui


if __name__ == '__main__':
    sen = "你知道1加2减3乘以10除以100+3的阶乘-以2为底4的对数+(10-9)*3的立方等于几"
    res = calculator_sihui(sen)
    print(res)
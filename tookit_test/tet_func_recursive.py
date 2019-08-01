# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/7/27 22:15
# @author   :Mo
# @function :test func_recursive

from tookit_sihui.ml_common.func_recursive.func_recursive import gen_syn_sentences


if __name__=="__main__":
    org_data = ["[你][喜欢|喜爱|爱][虾米|啥子|什么]", "[1|11][2|22][3|33][44|444]", "大漠帝国"]
    syn_sentences = gen_syn_sentences(org_data)
    # syn_sentences = sorted(syn_sentences)
    print(syn_sentences)
    gg = 0

# 测试结果
# ['你喜欢虾米', '你喜爱虾米', '你爱虾米', '你喜欢啥子', '你喜爱啥子', '你爱啥子', '你喜欢什么', '你喜爱什么', '你爱什么', '12344', '112344', '122344', '1122344', '123344', '1123344', '1223344', '11223344', '123444', '1123444', '1223444', '11223444', '1233444', '11233444', '12233444', '112233444', '大漠帝国']

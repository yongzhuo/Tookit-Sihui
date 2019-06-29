# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/6/28 15:49
# @author   :Mo
# @function :recursive of recursive of sentence, 模板匹配-递归函数


def FuncRecursive(len_curr=0, sen_odd=[], sen_curr=[]):
    """
      递归函数，将形如 [['1'], ['1', '2'], ['1']] 的list转为 ['111','121']
    :param count: int, recursion times
    :param candidate_list_set: list, eg.[['你'], ['是', '是不是'], ['喜欢', '喜爱', '爱'], ['米饭']]
    :param syn_sentences: list, Storing intermediate variables of syn setnence, eg.['你是喜欢米饭', '你是不是喜欢米饭', '你是不是爱米饭']
    :return: list, result of syn setnence, eg.['你是喜欢米饭', '你是不是喜欢米饭', '你是不是爱米饭']
    """
    syn_sentences = []
    len_curr = len_curr - 1
    if len_curr == -1:
        return sen_curr
    for sen_odd_one in sen_odd[0]:
        for syn_one in sen_curr:
            syn_sentences.append(syn_one + sen_odd_one)
    syn_sentences = FuncRecursive(len_curr=len_curr,
                                  sen_odd=sen_odd[1:],
                                  sen_curr=syn_sentences)
    return syn_sentences


def gen_syn_sentences(org_data):
    """
        同义句生成等
    :param org_data: list, list of rule
    :return: list
    """
    # 获取数据
    sentences_pre = []
    for org_sen in org_data:
        org_sen_sp = org_sen.split("][")
        sentences_add = []
        for words in org_sen_sp:
            words_sp = words.split("|")
            words_sp = [word.replace("]", "").replace("[", "") for word in words_sp]
            sentences_add.append(words_sp)
        sentences_pre.append(sentences_add)

    # 递归生成
    sentences_syn = []
    for sen_rule in sentences_pre:
        len_sen_rule = len(sen_rule)
        if len_sen_rule == 1: # 长度为1不递归
            sentences_syn = sentences_syn + sen_rule[0]
        else:
            sentences_syn = sentences_syn + FuncRecursive(len_curr=len_sen_rule-1,
                                                          sen_odd=sen_rule[1:],
                                                          sen_curr=sen_rule[0])
    return sentences_syn



if __name__=="__main__":
    org_data = ["[你][喜欢|喜爱|爱][虾米|啥子|什么]", "[1|11][2|22][3|33][44|444]", "大漠帝国"]
    syn_sentences = gen_syn_sentences(org_data)
    # syn_sentences = sorted(syn_sentences)
    print(syn_sentences)
    gg = 0

# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/7/27 22:16
# @author   :Mo
# @function :test TrieTree


from tookit_sihui.ml_common.trie_tree.trie_tree import get_trie_tree_class
from tookit_sihui.ml_common.trie_tree.trie_tree import TrieTree


if __name__ == "__main__":
    # 测试1, class实例
    trie = TrieTree()
    keywords = ['英雄', '人在囧途', '那些年,我们一起追过的女孩', '流浪地球', '华娱',
                '犬夜叉', '火影', '名侦探柯南', '约会大作战', '名作之壁', '动漫',
                '乃木坂46', 'akb48', '飘', '最后的武士', '约会', '英雄2', '日娱',
                '2012', '第九区', '星球大战', '侏罗纪公园', '泰坦尼克号', 'Speed']
    keywords = [list(keyword.strip()) for keyword in keywords]
    trie.add_keywords_from_list(keywords) # 创建树
    keyword = trie.find_keyword('我想看2012和第九区')
    print(keyword)

    # 测试2, get树
    trie_tree = get_trie_tree_class(keywords) # 创建树并返回实例化class
    while True:
        print("sihui请你输入:")
        input_ques = input()
        keywords = trie_tree.find_keyword(input_ques)
        print(keywords)

# 测试结果
# ['2012', '第九区']
# sihui请你输入:
# 你不知道我喜欢的是星球大战么
# ['星球大战']
# sihui请你输入:
# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/6/20 11:39
# @author   :Mo
# @function :utils of file tools


import logging as logger
import json


def txt_read(file_path, encode_type='utf-8'):
    """
      读取txt文件，默认utf8格式
    :param file_path: str, 文件路径
    :param encode_type: str, 编码格式
    :return: list
    """
    list_line = []
    try:
        file = open(file_path, 'r', encoding=encode_type)
        while True:
            line = file.readline()
            if not line:
                break
            list_line.append(line)
        file.close()
    except Exception as e:
        logger.info(str(e))
    finally:
        return list_line


def txt_write(list_line, file_path, type='w', encode_type='utf-8'):
    """
      txt写入list文件
    :param listLine:list, list文件，写入要带"\n" 
    :param filePath:str, 写入文件的路径
    :param type: str, 写入类型, w, a, a+等
    :param encode_type: 
    :return: None
    """
    try:
        file = open(file_path, type, encoding=encode_type)
        file.writelines(list_line)
        file.close()

    except Exception as e:
        logger.info(str(e))


def save_json(res, path_json):
    """
        保存lsit[json]
    :param res: 
    :param path_json: 
    :return: 
    """
    with open(path_json, mode='w+', encoding='utf-8') as fpj:
        json.dump(res, fpj, ensure_ascii=False)
        fpj.close()


def load_json(path_json):
    """
        下载lsit[json]
    :param path_json: 
    :return: 
    """
    with open(path_json, mode='r', encoding='utf-8') as fpj:
        list_json = json.load(fpj)
        fpj.close()
    return list_json


def load_float_from_txt(path):
    """
    # 从txt下载词-数据    
    :param path: 
    :return: 
    """
    term_score_dict = {}
    terms_score = txt_read(path)
    for term_score in terms_score:
        term_score_sp = term_score.split('\t')
        term_score_dict[term_score_sp[0]] = float(term_score_dict[1].strip())
    return term_score_dict


def load_float_from_json(path):
    """
        # 从json下载词-数据
    :param path: 
    :return: 
    """
    term_score_dict = {}
    terms_score = txt_read(path)
    for term_score in terms_score:
        term_score_sp = term_score.split('\t')
        term_score_dict[term_score_sp[0]] = float(term_score_dict[1].strip())
    return term_score_dict


if __name__ == '__main__':
    # list_json = load_json('list_json.json')
    data = {}
    data["100"]=1000
    list_json = [{"你好":10, "我i是谁":1000000}]
    json_str = json.dumps(data)
    save_json(list_json, 'list_json.json')

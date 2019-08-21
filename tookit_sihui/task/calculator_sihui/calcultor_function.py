# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/8/21 23:36
# @author   :Mo
# @function :function of some basic Extraction Scientific Computing


from tookit_sihui.task.calculator_sihui.calcultor_number import extract_number
from tookit_sihui.conf.logger_config import get_logger_root
import math


logger = get_logger_root()


def reagan(words, wordsminus):
    """
        求平方根，立方根，n次方根
    :param words: str, 原句
    :param wordsminus:str , 处理后的句子
    :return: 
    """
    try:
        if '根号' in words:
            reagan = wordsminus.replace("开", "").replace("根号", "").replace("的", "")
            radicalaa = float(extract_number(reagan)[0])
            if radicalaa < 0.0:
                return 'illegal math'
            radicalbb = math.sqrt(radicalaa)
            results = str(radicalbb)
        elif "平方根" in words:
            reagan = wordsminus.replace("开", "").replace("平方根", "").replace("平方", "").replace("的", "")
            reagan = extract_number(reagan)[0]
            squarerootaa = float(reagan)
            if squarerootaa < 0.0:
                return 'illegal math'
            squarerootbb = math.sqrt(squarerootaa)
            results = str(squarerootbb)
        elif "立方根" in words:
            reagan = wordsminus.replace("开", "").replace("立方根", "").replace("立方", "").replace("的", "")
            reagan = extract_number(reagan)[0]
            squarerootaa = float(reagan)
            squarerootbb = math.pow(squarerootaa, 1.0 / 3)
            results = str(squarerootbb)
        elif "次方根" in words:
            reagan = wordsminus.replace("开", "").replace("次方根", "").replace("次方", "")
            squareroot = reagan.split("的")
            squarerootaa = float(extract_number(squareroot[0])[0])
            squarerootbb = float(extract_number(squareroot[1])[0])
            if squarerootaa % 2 == 0 and squarerootbb < 0.0:
                return 'illegal math'
            squarerootcc = math.pow(squarerootaa, 1.0 / squarerootbb)
            results = str(squarerootcc)
        else:
            results = words
        return results
    except Exception as e:
        logger.info(str(e))
        return words


def power(words, wordsminus):
    """
        求指数，求平方
    :param words: 
    :param wordsminus: 
    :return: 
    """
    try:
        if "平方根" not in words and "平方" in words:
            reagan = wordsminus.replace("平方", "").replace("开", "").replace("的", "")
            reagan = extract_number(reagan)[0]
            square = float(reagan)
            radicalbb = math.pow(square, 2)
            results = str(radicalbb)
        elif "立方根" not in words and "立方" in words:
            reagan = wordsminus.replace("立方", "").replace("开", "").replace("的", "")
            reagan = extract_number(reagan)[0]
            square = float(reagan)
            radicalbb = math.pow(square, 3)
            results = str(radicalbb)
        elif (("次方" in words or "次幂" in words) and "次方根" not in words and "次幂根" not in words):
            reagan = wordsminus.replace("次方", "").replace("开", "").replace("次幂", "")
            squareroot = reagan.split("的")
            squarerootaa = float(extract_number(squareroot[0])[0])
            squarerootbb = float(extract_number(squareroot[1])[0])
            squarerootcc = math.pow(squarerootaa, squarerootbb)
            results = str(squarerootcc)
        else:
            results = words
        return results
    except Exception as e:
        logger.info(str(e))
        return words


def logarithm(words, wordsminus):
    """
        求对数
    :param words: 
    :param wordsminus: 
    :return: 
    """
    try:
        if "LG" in words or "LOG" in words:
            Lg = wordsminus.replace("LOG", "").replace("LG", "").replace(" ", "").replace("的", "")
            Lg = float(extract_number(Lg)[0])
            if Lg <= 0.0:
                return 'illegal math'
            lgbb = math.log(Lg)
            results = str(lgbb)
        elif "对数" in words:
            Logg = wordsminus.replace("以", "").replace("对数", "").replace("的对数", "").replace(" ", "").replace("的", "")
            root = Logg.split("为底")
            rootaa = float(extract_number(root[0])[0])
            rootbb = float(extract_number(root[1])[0])
            if rootaa <= 0.0 or rootbb <= 0.0:
                return 'illegal math'
            rootcc = math.log(rootbb) / math.log(rootaa)
            results = str(rootcc)
        else:
            results = words
        return results
    except Exception as e:
        logger.info(str(e))
        return words


def fraction(words, wordsminus):
    """
        求分数
    :param words: 
    :param wordsminus: 
    :return: 
    """
    try:
        if "fenzhi" in words:
            fenzhi = wordsminus.replace("fenzhi", "/").replace(" ", "").replace("的", "")
            root = fenzhi.split("/")
            rootaa = float(extract_number(root[0])[0])
            rootbb = float(extract_number(root[1])[0])
            rootcc = rootbb / rootaa
            results = str(rootcc)
        else:
            results = words
        return results
    except Exception as e:
        logger.info(str(e))
        return words


def fractiontwo(words, wordsminus):
    """
        取分数
    :param words: 
    :param wordsminus: 
    :return: 
    """
    try:
        if "fenzhi" in words:
            fenzhi = wordsminus.replace("fenzhi", "/").replace(" ", "").replace("的", "")
            root = fenzhi.split("/")
            rootaa = float(extract_number(root[0])[0])
            rootbb = float(extract_number(root[1])[0])
            results = str(rootaa) + "/" + str(rootbb)
        else:
            results = words
        return results
    except Exception as e:
        logger.info(str(e))
        return words


def factorial(words, wordsminus):
    """
        求阶乘
    :param words: 
    :param wordsminus: 
    :return: 
    """
    results = words
    try:
        if "jiecheng的" in words:
            factory = wordsminus.replace("jiecheng的", "").replace("的", "").replace(" ", "")
            fact = float(extract_number(factory)[0])
            if fact <= 10000:
                results = str(math.factorial(fact))
            else:
                results = words
        return results
    except Exception as e:
        logger.info(str(e))
        return words


if __name__ == '__main__':
    res = reagan("根号4", "根号4")
    print(res)
    res = reagan("27的3次方根是多少", "27的3次方根")
    print(res)
    res = power("9的平方", "9的平方")
    print(res)
    res = power("27的立方是几", "9的立方")
    print(res)
    res = power("3的3次方是几", "3的3次方实")
    print(res)
    res = logarithm("LG8", "LG8")
    print(res)
    res = logarithm("以2为底64的对数", "以2为底64的对数")
    print(res)
    res = fraction("1fenzhi6是多少", "1fenzhi6")
    print(res)
    res = factorial("10jiecheng的", "10jiecheng的")
    print(res)

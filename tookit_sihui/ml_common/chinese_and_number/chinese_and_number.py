# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/5/17 15:17
# @author   :Mo
# @function :change chinese digit to Arab or reversed

import random


def is_total_num(text):
    """
      判断是否是数字的
    :param text: str
    :return: boolean, True or false
    """
    try:
        text_clear = text.replace(" ", "").strip()
        number = 0
        for one in text_clear:
            if one.isdigit():
                number += 1
        if number == len(text_clear):
            return True
        else:
            return False
    except:
        return False


# chinese_to_number, 单位-数字
unit_dict = {"十": 10, "百": 100, "千": 1000, "万": 10000, "亿": 100000000,
             "拾":10, "佰":100, "陌":100, "仟":1000, "阡":1000, "萬":10000, "億":100000000}
unit_dict_keys = unit_dict.keys()
digit_dict = {"零": 0, "一": 1, "二": 2, "两": 2, "俩": 2, "三": 3,
             "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9,
             "壹":1, "贰":2, "叁":3, "肆":4, "伍":5, "陆":6, "柒":7, "捌":8, "玖":9, "弌":1, "弍":2, "弎":3,
             "貳":2, "陸":6, "0":0, "1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9}

# number_to_chinese, 单位-数字
num_dict = { 0: "零", 1: "一", 2: "二", 3: "三", 4: "四",
             5: "五", 6: "六", 7: "七", 8: "八", 9: "九" }
unit_map = [ ["", "十", "百", "千"],       ["万", "十万", "百万", "千万"],
             ["亿", "十亿", "百亿", "千亿"], ["兆", "十兆", "百兆", "千兆"] ]
unit_step = ["万", "亿", "兆"]


class chinese_to_number():
    def __init__(self):
        self.result = 0.0
        self.result_last = 0.0
        # 字符串分离
        self.str_billion = ""  # 亿
        self.str_billion_hundred = ""  # 亿万
        self.str_billion_one = ""
        self.str_thousand_ten = ""  # 万
        self.str_single = ""  # one

    def free_zero_and_split_three_parts(self, text):
        """
           去零切分成三部分
        :param text:str 
        :return: 
        """
        assert type(text) == str
        # if "零" in text:
        #     text = text.replace("零", "")
        # 分切成三部分
        index = 0
        flag_billion = True # 亿
        flag_billion_hundred = True # 万亿
        flag_thousand_ten = True #万
        len_text = len(text)
        for i in range(len_text):
            if "亿" == text[i]:
                # 存在亿前面也有万的情况，小分节
                self.str_billion = text[0:i]
                if text.find("亿") > text.find("万"):
                    for j in range(len(self.str_billion)):
                        if "万" == self.str_billion[j]:
                            flag_billion_hundred = False
                            self.str_billion_hundred = self.str_billion[0:j]
                            self.str_billion_one = self.str_billion[j+1:]
                # 如何亿字节中没有万，直接赋值
                if flag_billion_hundred:
                    self.str_billion_one = self.str_billion
                index = i + 1
                flag_billion = False
                # 分节完毕
                self.str_single = text[i + 1:]
            if "万" == text[i] and text.find("亿") < text.find("万"):
                self.str_thousand_ten = text[index:i]
                self.str_single = text[i+1:]
                flag_thousand_ten = False
        if flag_billion and flag_thousand_ten:
            self.str_single = text

    def str_to_number(self, text):
        """
           string change to number
        :param text: str
        :return: 
        """
        assert type(text) == str
        number_res = 0
        number_1 = 0
        number_2 = 0
        number_3 = 0
        if not text:
            return 0
        len_text = len(text)

        # 规范语,
        for i in range(len_text):
            # 数字
            if text[i] in digit_dict:
                number_1 = digit_dict[text[i]]
                if i == len_text - 1: # 最后一个数字
                    if len_text > 2:  # 口语化的情形, 如一万五
                        if text[len_text - 1] in digit_dict and text[len_text - 2] in unit_dict:
                            number_res += number_1 * number_2 * 0.1
                            break
                    number_res += number_1
            # 单位
            elif text[i] in unit_dict:
                number_2 = unit_dict[text[i]]
                if number_1==0 and number_2==10:
                    number_3 = number_2
                else:
                    number_3 = number_1 * number_2
                    # 清零避免重复读取
                    number_1 = 0
                number_res += number_3
            # 处理形如 "二点13亿", "1.56万" 这样的情况
            else:
                try:
                    text_else_str = [str(digit_dict[tet]) if tet in digit_dict else tet for tet in text]
                    number_res = float("".join(text_else_str))
                except:
                    number_res = 0
                break
        return number_res

    def compose_integer(self, text):
        """
            整数转数字, 合并
        :param text:str, input of chinese, eg.["一百", "三千零七十八亿三千零十五万零三百一十二"] 
        :return: float, result of change chinese to digit
        """
        assert type(text) == str
        self.result = 0.0
        self.result_last = 0.0
        if not text.strip():
            return self.result_last
        text = text.replace("兆", "万亿").replace("点", ".").strip(".").strip()
        len_text = len(text)
        # 判断十百千万在不在text里边，在的话就走第二个
        flag_pos = True
        for unit_dict_key in unit_dict_keys:
            if unit_dict_key in text:
                flag_pos = False
                break
        # 分三种情况，全数字返回原值，有中文unit_dict_keys就组合， 没有中文unit_dict_keys整合
        if is_total_num(text):
            digit_float = float(text)
            return digit_float
        elif flag_pos:
            result_pos = ""
            for i in range(len_text):
                if "."!=text[i] and not text[i].isdigit():
                    result_pos += str(digit_dict[text[i]])
                else:
                    result_pos += text[i]
            self.result_last = float(result_pos)
        else:
            self.free_zero_and_split_three_parts(text)
            float_billion_hundred = self.str_to_number(self.str_billion_hundred)
            float_billion_one = self.str_to_number(self.str_billion_one)
            float_thousand_ten = self.str_to_number(self.str_thousand_ten)
            float_single = self.str_to_number(self.str_single)

            self.result = float((float_billion_hundred * 10000 + float_billion_one) * 100000000 + float_thousand_ten * 10000 + float_single)
            self.result_last = self.result
            # 重置
            self.str_billion = ""  # 亿
            self.str_billion_hundred = ""  # 亿万
            self.str_billion_one = ""
            self.str_thousand_ten = ""  # 万
            self.str_single = ""  # one
        return self.result_last

    def compose_decimal(self, text):
        """
            中文小数转数字
        :param text:str, input of chinese, eg.["一百", "三千零七十八亿三千零十五万零三百一十二"] 
        :return: float, result of change chinese to digit
        """
        assert type(text) == str
        self.result = 0.0
        self.result_last = 0.0
        self.result_start = 0.0

        text = text.replace("兆", "万亿").replace("点", ".").strip()
        if "." in text:
            # 判断十百千万在不在.号后边，在的话就走compose_integer()，并且返回
            pos_point = text.find(".")
            for unit_dict_key in unit_dict_keys:
                if unit_dict_key in text:
                   if pos_point < text.find(unit_dict_key):
                       return  self.compose_integer(text)
            # 否则就是有小数
            texts = text.split(".")
            text_start = texts[0]
            text_end = texts[1]

            # 处理整数部分
            if "0"==text_start or "零"==text_start:
                self.result_start = "0."
            else:
                self.result_start = str(int(self.compose_integer(text_start))) + "."
            # 处理尾部，就是后边小数部分
            result_pos = ""
            len_text = len(text_end)
            for i in range(len_text):
                if "."!=text_end[i] and not text_end[i].isdigit():
                    result_pos += str(digit_dict[text_end[i]])
                else:
                    result_pos += text_end[i]
            # 拼接
            self.result_last = float(self.result_start + result_pos) if result_pos.isdigit() else self.result_start
        else:
            self.result_last = self.compose_integer(text)

        return self.result_last


class number_to_chinese():
    """
       codes reference: https://github.com/tyong920/a2c
    """
    def __init__(self):
        self.result = ""

    def number_to_str_10000(self, data_str):
        """一万以内的数转成大写"""
        res = []
        count = 0
        # 倒转
        str_rev = reversed(data_str)  # seq -- 要转换的序列，可以是 tuple, string, list 或 range。返回一个反转的迭代器。
        for i in str_rev:
            if i is not "0":
                count_cos = count // 4  # 行
                count_col = count % 4   # 列
                res.append(unit_map[count_cos][count_col])
                res.append(num_dict[int(i)])
                count += 1
            else:
                count += 1
                if not res:
                    res.append("零")
                elif res[-1] is not "零":
                    res.append("零")
        # 再次倒序，这次变为正序了
        res.reverse()
        # 去掉"一十零"这样整数的“零”
        if res[-1] is "零" and len(res) is not 1:
            res.pop()

        return "".join(res)

    def number_to_str(self, data):
        """分段转化"""
        assert type(data) == float or int
        data_str = str(data)
        len_data = len(str(data_str))
        count_cos = len_data // 4  # 行
        count_col = len_data-count_cos*4  # 列
        if count_col > 0: count_cos += 1

        res = ""
        for i in range(count_cos):
            if i==0:
                data_in = data_str[-4:]
            elif i==count_cos-1 and count_col>0:
                data_in = data_str[:count_col]
            else:
                data_in = data_str[-(i+1)*4:-(i*4)]
            res_ = self.number_to_str_10000(data_in)
            if "0000"==data_in: continue  # 防止零万, 零亿的情况出现
            res = res_ + unit_map[i][0] + res
        # if len(res) > 1 and res.endswith("零"): res = res[:-1]
        return res

    def decimal_chinese(self, data):
        assert type(data) == float or int
        data_str = str(data)
        if "." not in data_str:
            res = self.number_to_str(data_str)
        else:
            data_str_split = data_str.split(".")
            if len(data_str_split) is 2:
                res_start = self.number_to_str(data_str_split[0])
                res_end = "".join([num_dict[int(number)] for number in data_str_split[1]])
                res = res_start + random.sample(["点", "."], 1)[0] + res_end
            else:
                res = str(data)
        return res


def judge_compose_decimal(data_json):
    """测试小数"""
    ctn = chinese_to_number()
    for data in data_json.keys():
        res_dec = ctn.compose_decimal(data)
        if res_dec != data_json[data]:
            print("dec：\ttrain:" + data + "\ttrue:"+str(data_json[data])+ "\tpred:"+str(res_dec))


def judge_compose_integer(data_json):
    """测试整数"""
    ctn = chinese_to_number()
    for data in data_json.keys():
        res_dec = ctn.compose_integer(data)
        if res_dec != data_json[data]:
            print("int：\ttrain:" + data + "\ttrue:"+str(data_json[data])+ "\tpred:"+str(res_dec))


if __name__=="__main__":
    ctn = chinese_to_number()
    ques = "点二八"
    print(ctn.compose_decimal(ques))

    ######  1.测试阿拉伯数字转中文  ######################################################
    ntc = number_to_chinese()
    print(ntc.decimal_chinese(230000))

    # for i in range(1945, 2100):
    #     # print(ntc.decimal_chinese(i))
    #     print(ntc.decimal_chinese(0.112354))
    #     print(ntc.decimal_chinese(1024.112354))

    # ######  2.测试中文转阿拉伯   ########################################################
    # # 测试是小数（总接口,包含小数）
    # tet_decimal = {"1.3":1.3, "一.12":1.12, "三千零七十八亿三千零十五万零三百一十二":307830150312.0, "二点13亿":213000000.0, "1.56万": 15600.0,
    #                "十8.12":18.12, "一十八点九一":18.91, "零点一":0.1, "零点123":0.123, "十八点一":18.1, "零":0, "一千零九十九点六六":1099.66}
    # judge_compose_decimal(tet_decimal)
    #
    # # 测试是整数(只是整数接口)
    # ctn = chinese_to_number()
    # tet_base = {"一":1, "一十五":15, "十五":15, "二十":20, "二十三":23, "一百":100, "一百零一":101,
    #             "一百一十":110, "一百一十一":111, "一千":1000, "一千零一":1001, "一千零三十一":1031,
    #             "一万零二十一":10021.0, "一万零三百二十一":10321.0, "一万一千三百二十一":11321.0, "三千零十五万":30150000.0,
    #             "三千零一十五万":30150000.0, "三千五百六十八万零一百零一":35680101.0, "五十亿三千零七十五万零六百二十二":5030750622.0,
    #             "十三亿三千零十五万零三百一十二":1330150312.0, "一千二百五十八亿":125800000000.0, "三千零十五万零三百一十二":30150312.0,
    #             "一千二百五十八万亿":1258000000000000.0, "三千三百二十一":3321.0, "三百三十一":331.0, "二十一":21, "三百二十一":321,
    #             "一千二百五十八亿零三千三百二十一":125800003321.0, "两百":200, "两千两百二十二":2222, "两亿两千万两百万两百二十二":222000222.0,
    #             "三千零七十八亿三千零十五万零三百一十二":307830150312.0}
    # judge_compose_integer(tet_base)
    #
    #
    # print(ctn.compose_decimal("三千零七十八亿三千零十五万零三百一十二"))
    # print(ctn.compose_integer("三万亿"))
    # print(ctn.compose_integer("十 "))
    # print(ctn.compose_integer("百"))
    # print(ctn.compose_integer("千"))
    # print(ctn.compose_integer("万"))
    # print(ctn.compose_integer("十万"))
    # print(ctn.compose_integer("百万"))
    # print(ctn.compose_integer("千万"))
    # print(ctn.compose_integer("亿万"))
    # print(ctn.compose_integer("一二一二 "))
    # print(ctn.compose_integer("007"))
    # print(ctn.compose_integer("一百"))
    #
    #
    # ctn = chinese_to_number()
    # # 测试异常中文数字
    # cn_num = {"二":2, "三千零七十八亿三千零十五万零三百一十二":307830150312.0, '一千零五':1005, '两':2, '十':10, '一千五':1500,
    #           '1000':1000, '贰千伍':2500, '123.05亿万':12305000000.0}
    # judge_compose_decimal(cn_num)
    # while True:
    #     print("请输入:")
    #     ques = input()
    #     print(ctn.compose_decimal(ques))
    #     print(ctn.compose_integer(ques))


    print(ctn.compose_decimal("三千零七十八亿三千零十五万零三百一十二"))
    print(ctn.compose_integer("三万亿"))
    print(ctn.compose_integer("十 "))
    print(ctn.compose_integer("百"))
    print(ctn.compose_integer("千"))
    print(ctn.compose_integer("万"))
    print(ctn.compose_integer("十万"))
    print(ctn.compose_integer("百万"))
    print(ctn.compose_integer("千万"))
    print(ctn.compose_integer("亿万"))
    print(ctn.compose_integer("一二一二 "))
    print(ctn.compose_integer("007"))
    print(ctn.compose_integer("一百"))


    ctn = chinese_to_number()
    # 测试异常中文数字
    cn_num = {"二":2, "三千零七十八亿三千零十五万零三百一十二":307830150312.0, '一千零五':1005, '两':2, '十':10, '一千五':1500,
              '1000':1000, '贰千伍':2500, '123.05亿万':12305000000.0}
    judge_compose_decimal(cn_num)
    while True:
        print("请输入:")
        ques = input()
        print(ctn.compose_decimal(ques))
        print(ctn.compose_integer(ques))
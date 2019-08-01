# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/7/27 22:13
# @author   :Mo
# @function :test chinese_and_number


from tookit_sihui.ml_common.chinese_and_number.chinese_and_number import number_to_chinese
from tookit_sihui.ml_common.chinese_and_number.chinese_and_number import chinese_to_number


if __name__=="__main__":
    ######  1.测试阿拉伯数字转中文  ######################################################
    ntc = number_to_chinese()
    for i in range(1945, 2100):
        print(ntc.decimal_chinese(i))
    print(ntc.decimal_chinese(0.112354))
    print(ntc.decimal_chinese(1024.112354))

    ######  2.测试中文转阿拉伯   ########################################################
    ctn = chinese_to_number()
    tet_base = [ "一", "一十五", "十五", "二十", "二十三", "一百","一百零一",
                 "一百一十", "一百一十一", "一千", "一千零一","一千零三十一",
                 "一万零二十一", "一万零三百二十一", "一万一千三百二十一", "三千零十五万",
                 "三千零一十五万", "三千五百六十八万零一百零一", "五十亿三千零七十五万零六百二十二",
                 "十三亿三千零十五万零三百一十二", "一千二百五十八亿","三千零十五万零三百一十二",
                 "一千二百五十八万亿", "三千三百二十一", "三百三十一", "二十一", "三百二十一",
                 "一千二百五十八亿零三千三百二十一", "两百", "两千两百二十二", "两亿两千万两百万两百二十二",
                 "三千零七十八亿三千零十五万零三百一十二"]

    tet_decimal = ["二点13亿", "1.56万", "十八.12", "一十八点九一", "零点一", "零点123", "十八点一", "零", "一千零九十九点六六"]
    # 测试是小数
    for tet_d in tet_decimal:
        print(ctn.compose_decimal(tet_d))
    # 测试是整数
    for tet_b in tet_base:
        print(ctn.compose_integer(tet_b))

# 测试结果,截取部分
# 一千九百四十五
# 一千九百四十六
# 一千九百四十七
# 一千九百四十八
# 一千九百四十九
# 213000000.0
# 15600.0
# 18.12
# 18.91
# 0.1
# 0.123
# 18.1
# coding=utf-8
from __future__ import unicode_literals

from faker import Faker
from faker.providers import BaseProvider
import matplotlib.pyplot as plt
import string

localized = True


class InsurProvider(BaseProvider):
    license_plate_provinces = ("京")  # 这里添加不同省份，原项目需要，生成的大部分为一个地区的车

    license_plate_last = ("学", "警", "使", "领")  # 添加特殊车辆的尾字。

    license_plate_num = ("A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L",
                         "M", "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
                         "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                         "0")

    def license_plate(self):
        """ 传统车牌 """
        plate = "{0}{1}{2}".format(
            self.random_element(self.license_plate_provinces),
            self.random_uppercase_letter(), "".join(
                self.random_choices(elements=self.license_plate_num,
                                    length=5)))
        return plate

    def special_license_plate(self):
        """ 特种车牌 """
        plate = "{0}{1}{2}{3}".format(
            self.random_element(self.license_plate_provinces),
            self.random_uppercase_letter(), "".join(
                self.random_choices(elements=self.license_plate_num,
                                    length=4)),
            self.random_element(self.license_plate_last))
        return plate

    def custom_license_plate(self, prov, org, last=None):
        """
        prov: 省简称
        org: 发牌机关简称字母
        last: 特种车汉字字符
        """
        if last is None:
            plate = "{0}{1}{2}".format(
                prov, org, "".join(
                    self.random_choices(elements=self.license_plate_num,
                                        length=5)))
        else:
            plate = "{0}{1}{2}{3}".format(
                prov, org, "".join(
                    self.random_choices(elements=self.license_plate_num,
                                        length=4)), last)

        return plate

    def new_energy_license_plate(self, car_model=1):
        """ 
        新能源车牌 
        car_model: 车型，0-小型车，1-大型车
        """
        plate = ""
        if car_model == 0:
            # 小型车
            plate = "{0}{1}{2}{3}{4}".format(
                self.random_element(self.license_plate_provinces),
                self.random_uppercase_letter(),
                self.random_element(elements=("D", "F")),
                self.random_element(elements=self.license_plate_num),
                self.random_int(1000, 9999))
        else:
            # 大型车
            plate = "{0}{1}{2}{3}".format(
                self.random_element(self.license_plate_provinces),
                self.random_uppercase_letter(), self.random_int(10000, 99999),
                self.random_element(elements=("D", "F")))

        return plate

    def test_print(self):
        print(self.new_energy_license_plate())


if __name__ == "__main__":
    k = Faker()
    p = InsurProvider(k)
    content = []
    import random
    import pandas as pd
    import math
    flow = random.randint(125, 175)  # 这里控制生成的车辆数目

    # 控制各种车辆的权重
    normal_num = math.floor(flow * 0.7)  # 普通内燃汽车
    ele_normal_num = math.floor(flow * 0.19)  # 电动汽车
    special_num = math.floor(flow * 0.04)  # 特殊车辆
    outside_num = math.floor(flow * 0.07)  # 外省车辆
    for i in range(0, normal_num):
        content.append([p.license_plate()])
    for i in range(0, ele_normal_num):
        content.append([p.new_energy_license_plate(0)])
    for i in range(0, special_num):
        content.append([p.special_license_plate()])
    license_plate_provinces = ("沪", "浙", "苏", "粤", "鲁", "晋", "冀", "豫", "川",
                               "渝", "辽", "吉", "黑", "皖", "鄂", "津", "贵", "云",
                               "桂", "琼", "青", "新", "藏", "蒙", "宁", "甘", "陕",
                               "闽", "赣", "湘")
    license_plate_num = ("A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L",
                         "M", "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
                         "Y", "Z")
    for i in range(0, outside_num):
        index1 = random.randint(0, 20)
        index2 = random.randint(0, 15)
        # print(license_plate_num[index1])
        content.append([
            p.custom_license_plate(license_plate_provinces[index1],
                                   license_plate_num[index2])
        ])
    import radar
    import datetime
    from random import shuffle
    shuffle(content)  # 车牌的乱序
    for x in content:
        starttime = radar.random_datetime()  # 随机时间生成
        stop = starttime.strftime('%Y-%m-%d')
        stop = stop + ' 23:59:59'
        endtime = radar.random_datetime(
            start=starttime, stop=stop)  # 要求进入时间早于出来时间
        # 这里的时间格式决定最后的输出形式（为了简化这里使用c++int能读的）
        x.append(starttime.strftime('%H%M%S'))
        x.append(endtime.strftime('%H%M%S'))
    content = sorted(content, key=lambda x: x[1])  # 根据进入时间排序
    # print(content)
    count = 0
    # 为了调整每个时段车辆的权重，这里flow乘的系数可以更改。
    # 这里生成了每个时段车辆数的一个列表
    count_list = [
        math.floor(flow * 1 / 32.9),
        math.floor(flow * 1 / 32.9),
        math.floor(flow * 1 / 32.9),
        math.floor(flow * 1 / 32.9),
        math.floor(flow * 1 / 32.9),
        math.floor(flow * 1 / 32.9),
        math.floor(flow * 1 / 32.9),
        math.floor(flow * 1.1 / 32.9),
        math.floor(flow * 1.2 / 32.9),
        math.floor(flow * 1.4 / 32.9),
        math.floor(flow * 1.5 / 32.9),
        math.floor(flow * 1.6 / 32.9),
        math.floor(flow * 1.7 / 32.9),
        math.floor(flow * 1.6 / 32.9),
        math.floor(flow * 1.6 / 32.9),
        math.floor(flow * 1.6 / 32.9),
        math.floor(flow * 1.6 / 32.9),
        math.floor(flow * 1.6 / 32.9),
        math.floor(flow * 1.7 / 32.9),
        math.floor(flow * 2 / 32.9),
        math.floor(flow * 1.8 / 32.9),
        math.floor(flow * 1.5 / 32.9),
        math.floor(flow * 1.3 / 32.9),
        math.floor(flow * 1.1 / 32.9),
    ]
    # print(count_list)

    # 小时的列表
    hour_list = [
        '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11',
        '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'
    ]
    # print(content[2][1])
    # print(content[2][1][0:2])
    hour_num = []
    hour_index = 0
    num = 0

    # 根据hour——list生成上方数据在每个小时实际的车数量
    for x in content:
        hour = hour_list[hour_index]
        if x[1][0:2] == hour:
            num += 1
        else:
            hour_num.append(num)
            num = 1
            if (hour_index < 23):
                hour_index += 1
    hour_num.append(len(content) - sum(hour_num))
    #
    # print(hour_num)

    # 做加权处理
    # 原则是多与标准删去，少于标准不变
    count = 0
    new_content = []
    before = 0
    total = 0
    for i, x in enumerate(hour_num):
        before = total
        count = total + count_list[i]
        if (count_list[i] < x):
            new_content.extend(content[before:count])
            total += hour_num[i]
        else:
            new_content.extend(content[before:count])
            total += hour_num[i]
    # print(new_content)

    # 打印一下分布
    plt.figure(figsize=(20, 15))
    plt.bar(range(len(count_list)),
            count_list,
            color='r',
            tick_label=hour_list,
            facecolor='#9999ff',
            edgecolor='white')

    plt.xticks(rotation=45, fontsize=20)
    plt.yticks(fontsize=20)

    # plt.legend()
    plt.title('''num of car flow changes with time''', fontsize=24)
    plt.savefig('./bar_result.png')
    plt.show()

    print(new_content)
    name = ['label', 'in', 'out']
    test = pd.DataFrame(columns=name, data=new_content)
    # test['in'] = '\t' + test['in']#用于excel显示时有开头的0
    # test['out'] = '\t' + test['out']#用于excel显示时有开头的0
    test.to_csv('./fakedata.csv', index=False, encoding='GB18030')
    # 最后的编码方法适用于c++的csv读取且在vs2019，GBK下不会乱码

    # 可选的功能列表
# 随机生成普通车牌
# print(p.license_plate())

# 随机生成特种车牌
# print(p.special_license_plate())

# 自定义普通车牌
#print(p.custom_license_plate("京", "A"))

# 自定义特种车牌
#print(p.custom_license_plate("京", "B"))

# 随机生成新能源小型车车牌
# print(p.new_energy_license_plate(0))

# 随机生成新能源大型车车牌
# print(p.new_energy_license_plate(1))

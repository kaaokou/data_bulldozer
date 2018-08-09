# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-12 下午7:43
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import csv
import json


def json_to_csv():
    # 创建json,csv文件对象
    json_file = open("position.json", "r")
    csv_file = open("position.csv", "w")

    # 将json数据加载为python类型
    item_list = json.load(json_file)
    # 第一步：写表格的表头信息
    sheet_head = item_list[0].keys()
    # 第二步：写表格的详细记录
    sheet_data = [item.values() for item in item_list]

    # 写入数据
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(sheet_head)
    csv_writer.writerows(sheet_data)

    # 关闭文件对象
    csv_file.close()
    json_file.close()


if __name__ == '__main__':
    json_to_csv()

#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8

import requests

from manic_time_api_client.util import *
from configparser import ConfigParser

class WeekMarkDown:
    def __init__(self):
        self.type_time = {}
        self.count = 0;

    def check_tags(self, tmp_str):
        if tmp_str.find('，') > 0:
            return False
        return True

    def add_tags(self,tags_str,duration):
        tag_list = tags_str.split(',')
        if tag_list[-1] .find(':billable') > -1:
            self.count += 1
            if tag_list[0].find("生活") > -1:
                print("tag_list:", tag_list)
        # print("tag_list0:", tag_list[0])
        # print('find_result', tag_list[0].find("生活"))
        # print(self.count)
        first_type,second_type = tag_list[0:2]
        self.add_type_time(tags_str.strip(),duration)
        self.add_type_time(first_type.strip(),duration)
        self.add_type_time(second_type.strip(),duration)

    def add_type_time(self,tag_type,duration):
        # print("add_type_time tag_type:",tag_type)
        # print("add_type_time duration:", duration)
        self.type_time[tag_type] = self.type_time.get(tag_type,0) + duration

    def get_type_time(self,tag_type):
        # print("get_type_time self.type_time:", self.type_time)
        # print("get_type_time tag_type:",tag_type)
        duration = self.type_time.get(tag_type,0)
        # print("get_type_time duration:", duration)
        return duration

    def get_table(self, title, datas):
        alignment = [':---'] * len(title)
        md_string = [' | '.join(title), ' | '.join(alignment), ]
        for data in datas:
            data_string = ' | '.join(data)
            md_string.append(data_string)
        md_table = '\n'.join(md_string)
        print(md_table)
        return md_table

def WriteDayMarkDown():
    cfg = ConfigParser()
    cfg.read('cfg.ini',encoding='utf-8')
    api_url = cfg['manic_time']['api_url']
    token = cfg['manic_time']['token']
    week_start, week_end = getWeekStartAndEnd()
    week_start, week_end = '2020-04-04','2020-04-07'
    print(week_start, week_end)
    url = "{}/activities?fromTime={}&toTime={}".format(api_url,week_start,week_end)
    payload = {}
    headers = {
        'Accept': 'application/vnd.manictime.v2+json',
        'Authorization': 'Bearer {}'.format(token)
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    datas = response.json()
    activities = datas['activities']
    print(activities)

    week_md = WeekMarkDown()
    for activity in activities:
        print(activity)
        tags_str = '{}\n'.format(activity['displayName'])
        if not week_md.check_tags(tags_str):
            print("error tags_str:", tags_str)
            return
        duration = get_duration_sec(activity['startTime'], activity['endTime']) / 3600
        week_md.add_tags(tags_str,duration)

    title = ['大类', '总用时','平均每天用时']
    day_num = 3
    datas = [
        ['生活', "{:.1f}".format(week_md.get_type_time('生活')),"{:.1f}".format(week_md.get_type_time('生活')/day_num)],
        ['自由', "{:.1f}".format(week_md.get_type_time('自由')),"{:.1f}".format(week_md.get_type_time('自由')/day_num)],
        ['自由 - 计划零', "{:.1f}".format(week_md.get_type_time('计划零')),"{:.1f}".format(week_md.get_type_time('计划零')/day_num)],
        ['自由 - 计划一', "{:.1f}".format(week_md.get_type_time('计划一')),"{:.1f}".format(week_md.get_type_time('计划一')/day_num)],
        ['自由 - 计划二', "{:.1f}".format(week_md.get_type_time('计划二')),"{:.1f}".format(week_md.get_type_time('计划二')/day_num)],
        ['自由 - 计划三', "{:.1f}".format(week_md.get_type_time('计划三')),"{:.1f}".format(week_md.get_type_time('计划三')/day_num)],
        ['娱乐', "{:.1f}".format(week_md.get_type_time('娱乐')), "{:.1f}".format(week_md.get_type_time('娱乐') / day_num)],
    ]
    time_table = week_md.get_table(title, datas)
    f = open("manictime_day.md", "w",encoding="utf-8")
    time_range = "## {} -- {}  \n\n".format(week_start,week_end)
    f.write(time_range)
    f.write(time_table)
    f.write('\n')
    # title = [
    #     '<div style="width:60px">类型</div>',
    #     '<div style="text-align:center"><font color=red>预期[实际]</font></div>',
    #     '<div style="width:60px;text-align:center">结果</div>',
    #     '<div style="width:200px;text-align:center">总结</div>',
    # ]

    # f.write("### 工作")
    # f.write('\n')
    # work_datas = [
    #     ['bug修复','状态恢复相关处理','ko','后续回顾一下笔记'],
    # ]
    # work_table = week_md.get_table(title, work_datas)
    # f.write(work_table)
    # f.write('\n')
    #
    # f.write("### 业余学习")
    # f.write('\n')
    # free_datas = [
    #     ['bug修复', '状态恢复相关处理', 'ko', '后续回顾一下笔记'],
    # ]
    # free_table = week_md.get_table(title, free_datas)
    # f.write(free_table)
    # f.write('\n')
    #
    # f.write("### 生活")
    # f.write('\n')
    # life_datas = [
    #     ['bug修复', '状态恢复相关处理', 'ko', '后续回顾一下笔记'],
    # ]
    # life_table = week_md.get_table(title, life_datas)
    # f.write(life_table)
    # f.write('\n')
    #
    # f.write("### 健康")
    # f.write('\n')
    # health_datas = [
    #     ['bug修复', '状态恢复相关处理', 'ko', '后续回顾一下笔记'],
    # ]
    # health_table = week_md.get_table(title, health_datas)
    # f.write(health_table)
    # f.write('\n')
    #
    # f.write("### 人际交往")
    # f.write('\n')
    # communication_datas = [
    #     ['bug修复', '状态恢复相关处理', 'ko', '后续回顾一下笔记'],
    # ]
    # communication_datas = week_md.get_table(title, communication_datas)
    # f.write(communication_datas)
    # f.write('\n')

    f.close()


if __name__ == '__main__':
    WriteDayMarkDown()

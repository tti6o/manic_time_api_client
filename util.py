#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
import datetime
import time

def get_duration_sec(startTimeStr,endTimeStr,time_format = '%Y-%m-%dT%H:%M:%S+08:00'):
    start_tt = time.strptime(startTimeStr, time_format)
    start_tick = int(time.mktime(start_tt))
    end_tt = time.strptime(endTimeStr, time_format)
    end_tick = int(time.mktime(end_tt))
    last_sec = (end_tick - start_tick)
    return last_sec

def getWeekStartAndEnd():
    today = datetime.date.today()
    print("today:",today)
    week_start = today - datetime.timedelta(days=today.weekday())
    print("week_start:",week_start)
    work_day = 7
    week_end = week_start + datetime.timedelta(days=work_day - 1)
    print("week_end:",week_end)
    return week_start,week_end
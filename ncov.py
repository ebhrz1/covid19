#!/usr/bin/python3
#by hrz
import requests
from pyquery import PyQuery as pq
import sys
import json
import re
import pymysql
import time

#数据库连接
conn=pymysql.connect(host='localhost',user='root',password='123',database='ncov',charset='utf8')
cur=conn.cursor()


url='http://ncov.dxy.cn/ncovh5/view/pneumonia'
page=requests.get(url)
page.encoding='utf-8'
if page.ok:
	content=pq(page.text)
else:
	print('network error')
	sys.exit()
date=time.strftime("%Y-%m-%d",time.localtime())
# getStatisticsService 统计数据
'''
总计与新增数据
'currentConfirmedCount'当前确诊
'confirmedCount'总计确诊数
'suspectedCount'疑似
'curedCount'治愈
'deadCount'死亡
'seriousCount'病危
'suspectedIncr'疑似新增
'currentConfirmedIncr'现存确诊增量
'confirmedIncr'确诊增量
'curedIncr'治愈增量
'deadIncr'死亡增量
'seriousIncr'病危增量
'''


jstr=re.match('.*?=(.*)\}catch\(e\)',content('#getStatisticsService').text()).group(1)
summary=json.loads(jstr)

sql="insert into `summary`(`date`, `currentConfirmedCount`, `confirmedCount`, `suspectedCount`, `curedCount`, `deadCount`, `seriousCount`, `suspectedIncr`, `currentConfirmedIncr`, `confirmedIncr`, `curedIncr`, `deadIncr`, `seriousIncr`) \
values('%s',%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d)" % (date,summary['currentConfirmedCount'],summary['confirmedCount'],summary['suspectedCount'],summary['curedCount'],summary['deadCount'],summary['seriousCount'],summary['suspectedIncr'],summary['currentConfirmedIncr'],summary['confirmedIncr'],summary['curedIncr'],summary['deadIncr'],summary['seriousIncr'])
#print(sql)
try:
	res=cur.execute(sql)
	conn.commit()
except:
	conn.rollback()

#getListByCountryTypeService2 国际数据
'''
`continents`大洲
`provinceName`国家名 
`currentConfirmedCount`当前确诊 
`confirmedCount`总计确诊
`suspectedCount`疑似数
`curedCount`治愈数
`deadCount`死亡数
'''

jstr=re.match('.*?=(.*)\}catch\(e\)',content('#getListByCountryTypeService2').text()).group(1)
internation=json.loads(jstr)
for i in internation:
	sql="INSERT INTO `internation` ( `date`, `continents`, `provinceName`, `currentConfirmedCount`, `confirmedCount`, `suspectedCount`, `curedCount`, `deadCount`) VALUES ( '%s', '%s', '%s', %d, %d, %d, %d, %d)" % (date,i['continents'],i['provinceName'],i['currentConfirmedCount'],i['confirmedCount'],i['suspectedCount'],i['curedCount'],i['deadCount'])
	try:
		res=cur.execute(sql)
		conn.commit()
	except Exception as e:
		print(e)
		conn.rollback()

'''
getAreaStat 国内省市

provicne
provinceName`国家名 
`currentConfirmedCount`当前确诊 
`confirmedCount`总计确诊
`suspectedCount`疑似数
`curedCount`治愈数
`deadCount`死亡数

city
provinceName`国家名 
cityname 市名
`currentConfirmedCount`当前确诊 
`confirmedCount`总计确诊
`suspectedCount`疑似数
`curedCount`治愈数
`deadCount`死亡数

'''
jstr=re.match('.*?=(.*)\}catch\(e\)',content('#getAreaStat').text()).group(1)
nation=json.loads(jstr)
for n in nation:
	sql="INSERT INTO `province` ( `date`, `provinceName`, `currentConfirmedCount`, `confirmedCount`, `suspectedCount`, `curedCount`, `deadCount`) VALUES ( '%s', '%s', %d, %d, %d, %d, %d)" % (date,n['provinceName'],n['currentConfirmedCount'],n['confirmedCount'],n['suspectedCount'],n['curedCount'],n['deadCount'])
	try:
		res=cur.execute(sql)
		conn.commit()
	except Exception as e:
		print(e)
		conn.rollback()
	for c in n['cities']:
			sql="INSERT INTO `city` ( `date`, `provinceName`, `cityName`,`currentConfirmedCount`, `confirmedCount`, `suspectedCount`, `curedCount`, `deadCount`) VALUES ( '%s', '%s', '%s' ,%d, %d, %d, %d, %d)" % (date,n['provinceName'],c['cityName'],c['currentConfirmedCount'],c['confirmedCount'],c['suspectedCount'],c['curedCount'],c['deadCount'])
			try:
				res=cur.execute(sql)
				conn.commit()
			except Exception as e:
				print(e)



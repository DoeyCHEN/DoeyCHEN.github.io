# -*- coding: utf-8 -*-
import requests
from lxml import html
from datetime import *

# 编辑此处
stuNum = '1450126'
stuPwd = 'aa156199y'
# 编辑此处
if __name__ == '__main__':
    #   建立会话
    s = requests.Session()
    s.get('http://4m3.tongji.edu.cn/eams/login.action')
    res = s.get('http://4m3.tongji.edu.cn/eams/samlCheck').text
    SAMLRequest = html.fromstring(res).findall('.//meta')[0].get('content')[6:]
    s.cookies['oiosaml-fragment'] = ''
    s.get(SAMLRequest)
    s.post('https://ids.tongji.edu.cn:8443/nidp/saml2/sso?sid=0',
        data = {
        'option':'credential',
        'Ecom_User_ID': stuNum,
        'Ecom_Password': stuPwd,
        # 'submit': '登陆'
        })
    res = s.post('https://ids.tongji.edu.cn:8443/nidp/saml2/sso?sid=0').text
    hidden = html.fromstring(res).findall('.//input')
    data = {}
    for x in hidden:
        data[x.get('name')] = x.get('value')
    s.post('http://4m3.tongji.edu.cn/eams/saml/SAMLAssertionConsumer', data = data)

    # 登陆进入4m3首页
    #  res = s.get('http://4m3.tongji.edu.cn/eams/home.action').content


    # 学期
    semester = date.today().year-2017+103
    if date.today().month < 9 and date.today().month > 2:
        semester+=1
    # 学生id
    # res = s.get('http://4m3.tongji.edu.cn/eams/courseTableForStd.action?_=1488195754548').text.encode('utf-8')
    # open('b.html','w').write(res)
    # id = html.fromstring(res).find()
    # 我的课表信息
    res = s.post('http://4m3.tongji.edu.cn/eams/courseTableForStd!courseTable.action',
                 data={
                   'ignoreHead': '1',
                   'setting.kind': 'std',
                   'startWeek': '1',
                   'semester.id': semester,
                   'ids': 845950194
               }
               ).text.encode('utf-8')
    open('a.html', 'w').write(res)
    # 课程名称
    course = html.fromstring(res).findall('.//div/table/tbody/tr/td[3]')
    # 查找课程教材信息
    textbooks = html.fromstring(res).findall('.//a')

    # 写入文件
    result = open('result.txt', 'w')

    for i in range(0,len(course)):
        result.writelines(course[i].text.strip().encode('utf-8')+'\n')
        # 获取教材详情
        res = s.get('http://4m3.tongji.edu.cn/eams/courseTableForStd!searchTextbook.action?'+textbooks[1+2*i].get('href')[45::]).text
        a = html.fromstring(res).findall('.//td')
        for detail in a:
            if detail.text == None:
                continue
            else:
                result.write('\t'+detail.text.strip('').encode('utf-8'))
        result.writelines('\n')
    result.close()

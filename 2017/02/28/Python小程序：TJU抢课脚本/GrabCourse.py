# -*- coding: utf-8 -*-
import os
import time
import requests
import urllib2
from lxml import html

import sys
reload(sys)
sys.setdefaultencoding('utf8')


header = {
    'Accept':'text/html, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection':'keep-alive',
    'Host':'4m3.tongji.edu.cn',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest'
}

class STU(object):
    def __init__(self):
        self.coding = 'utf-8'
        self.elect = []
        self.withdraw = {}
        print u'====================================================================\n'
        print u'               Copyright (C) 2017 chendy'
        print u'               All rights reserved'
        print u'               Contact: whyemailme@163.com\n'
        print u'====================================================================\n'
        print u'----------------运行过程中按Ctrl C退出或直接关闭窗口----------------'
        print u'--------------点击窗口左上角的白色按钮-->编辑可进行粘贴-------------\n'

        self.stuNum = raw_input('请输入学号: '.strip())
        self.stuPwd = raw_input('请输入密码: '.strip())

    def login(self):
        #   建立会话
        self.s = requests.Session()
        self.s.headers = header
        self.s.get('http://4m3.tongji.edu.cn/eams/login.action')
        res = self.s.get('http://4m3.tongji.edu.cn/eams/samlCheck').text
        SAMLRequest = html.fromstring(res).findall('.//meta')[0].get('content')[6:]
        self.s.cookies['oiosaml-fragment'] = ''
        self.s.get(SAMLRequest)
        self.s.post('https://ids.tongji.edu.cn:8443/nidp/saml2/sso?sid=0',
               data={
                   'option': 'credential',
                   'Ecom_User_ID': self.stuNum,
                   'Ecom_Password': self.stuPwd,
                   # 'submit': '登陆'
               })
        res = self.s.post('https://ids.tongji.edu.cn:8443/nidp/saml2/sso?sid=0').text
        hidden = html.fromstring(res).findall('.//input')
        print hidden
        data = {}
        for x in hidden:
            data[x.get('name')] = x.get('value')
        self.s.post('http://4m3.tongji.edu.cn/eams/saml/SAMLAssertionConsumer', data=data)

    def inputCourse(self):
        print '''输入字母代号后回车
        q : 抢课(指定的一门课有空位时直接选课)
        h : 换课(BBB有空位时,退掉AAA换BBB)
        qh: 抢课 + 换课
        '''
        wanted = raw_input(u'请输入您想要的操作: '.encode(self.coding)).strip()
        while wanted not in ['q', 'h', 'qh']:
            wanted = raw_input(u'请重新输入： '.encode(self.coding)).strip()

        if 'q' in wanted:
            self.Elect()
        if 'h' in wanted:
            self.ElectAndWithdraw()

    def Elect(self):
        flag = 'y'
        while flag == 'y':
            course = raw_input(u'请输入要抢的一门课的教学班号: '.encode(self.coding)).strip()
            self.elect.append(course)
            flag = raw_input(u'是否继续输入(y or n): '.encode(self.coding)).strip()

    def ElectAndWithdraw(self):
        print u'当B课程有空位时退掉A课程选择B课程'
        flag = 'y'
        while flag == 'y':
            courseA = raw_input('请输入当有空位时，要退的一门课的教学班号：'.encode(self.coding).strip())
            courseB = raw_input('请输入要抢的一门课的教学班号：'.encode(self.coding).strip())
            self.withdraw[courseA] = courseB
            flag = raw_input('是否继续输入(y or n)：'.encode(self.coding).strip())

    def run(self):
        ct = 1
        while (self.elect != [] or self.withdraw != []):
            print  u'---------------第%d次刷课--------------' % ct
            ct = ct + 1

            for course in self.elect:
                if self.select(course) == True:
                    self.elect.remove(course)

            if self.withdraw != {}:
                for withCourse in self.withdraw.key:
                    if self.unselect(course):
                        if self.select(self.withdraw[withCourse]) == True:
                            del self.withdraw[withCourse]
                        else:
                            self.select(withCourse)

            time.sleep(0.1)
        print u'本次抢课目标已完成!!!请登录选课系统查看结果\a\a'

    def select(self,course):
        res = self.s.get('http://4m3.tongji.edu.cn/eams/doorOfStdElectCourse.action').text
        profileid = html.fromstring(res).find('.//a').get('href')[-1:-5:-1]
        res = self.s.get(
            'http://4m3.tongji.edu.cn/eams/tJStdElectCourse!defaultPage.action?electionProfile.id=' + profileid).text
        res = self.s.get('http://4m3.tongji.edu.cn/eams/tJStdElectCourse!batchOperator.action?electLessonIds='+course+'%2C&withdrawLessonIds=&exchangeLessonPairs=&_=1488208495866').text

        # print res
        result = html.fromstring(res).find('.//div').text
        print result.strip()
        if "成功".decode('utf-8') in result.strip().decode('utf-8'):
            return True
        else:
            return False

    def unselect(self,withCourse):
        res = self.s.get('http://4m3.tongji.edu.cn/eams/doorOfStdElectCourse.action').text
        profileid = html.fromstring(res).find('.//a').get('href')[-1:-5:-1]
        res = self.s.get(
            'http://4m3.tongji.edu.cn/eams/tJStdElectCourse!defaultPage.action?electionProfile.id=' + profileid).text
        res = self.s.get(
            'http://4m3.tongji.edu.cn/eams/tJStdElectCourse!batchOperator.action?withdrawLessonIds='+withCourse+'&_=1488208495866').text

        print res
        result = html.fromstring(res).find('.//div').text
        print result
        if "成功".decode('utf-8') in result.strip().decode('utf-8'):
            return True
        else:
            return False

if __name__ == '__main__':
    stu = STU()
    stu.login()
    stu.inputCourse()

    while True:
        try:
            stu.run()
            break
        except urllib2.HTTPError, e:
            print u'连接已断开,重新登录...'
            stu.login()
        except urllib2.URLError, e:
            print u'网络出现问题,连接超时,请重新运行'
            stu.login()

    # case: 111111112161303

    # http://4m3.tongji.edu.cn/eams/tJStdElectCourse!batchOperator.action?electLessonIds=111111112161793%2C&withdrawLessonIds=&exchangeLessonPairs=&_=1488208495866
    # http://4m3.tongji.edu.cn/eams/tJStdElectCourse!batchOperator.action?withdrawLessonIds=111111112161793&_=1488208437676
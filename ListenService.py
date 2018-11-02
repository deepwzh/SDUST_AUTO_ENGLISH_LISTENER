from UserModel import UserModel
import urllib
import http
from Tool import *
import time
import re
from functools import reduce

class ListenService(object):
    domain = "192.168.100.117"
    urls = {
        "update_time": "http://192.168.100.117/npels/Student/LogTime.aspx?logType=updatestattime&nocache=0.5459331257488433",
        "index":"http://192.168.100.117/npels/student/index.aspx"
    }

    def __init__(self):
        self.base_url = "http://%s/npels/" % ListenService.domain
        useragent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
        Referer = 'http://192.168.100.117/npels/studentdefault.aspx'  #确保正常挂时长的关键请求头
        self.headers = {'User-Agent' : useragent, 'Referer' : Referer}
        self.cookie = http.cookiejar.CookieJar()
        self.opener = None

    def request_url(self, url, postdata = None):
        """
        请求一个地址
        :param url: 请求的url
        :param postdata: POST请求数据（如果存在的话）
        :return: 接收到的response内容
        """
        # print(url)
        if postdata:
            request = urllib.request.Request(url, postdata, headers = self.headers)
        else:
            request = urllib.request.Request(url, headers = self.headers)

        response = self.opener.open(request)
        return response.read().decode()

    def update_time(self):
        """
        更新时长
        :return: 
        """
        self.request_url(ListenService.urls["update_time"])

    def __login(self, username, password):
        """
                用户登录
                :param username: 登录用户名 
                :param password: 登录密码
                :return: 
                """
        url = self.base_url + "login.aspx"
        values = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '/wEPDwULLTE2NTQ5MDE2NTlkZPkrSJpx1q4rg6p87qlrVoTz4rnR',
            'tbName': username,
            'tbPwd': password,
            'btnLogin': "登录"
        }
        postdata = urllib.parse.urlencode(values).encode()
        handler = urllib.request.HTTPCookieProcessor(self.cookie)
        self.opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(self.opener)
        data = self.request_url(url, postdata=postdata)
        data = self.request_url(ListenService.urls["index"])
        re1 = re.compile(r'CourseIndex.aspx\?c=(.*)&m=(.*)\'')
        re2 = re.compile(r'<span id=\"ctl00_lblName\">(.*?)</')
        re3 = re.compile(r'班级：([^0-9]*)([0-9-]*)')
        try:
            self.user.stu_realname = re2.search(data).groups()[0] #设置真实姓名
            info = re3.search(data).groups()
            self.user.set_class_info(info[0], info[1])
            for m in re1.finditer(data):

                if username == "201601060934":
                    self.user.set_class_id("2017-0001-0424")
                else:
                    self.user.set_class_id(str(m.groups()[0]))
                break
            self.cookie.set_cookie(make_cookie('ctoken', '%7Bf3ef099e-397c-4894-9c2e-77f2e4a7b817%7D'))
            self.cookie.set_cookie(make_cookie('TimeRecordEnabled', 'true'))
            return True
        except:
            return False

        # url = "http://192.168.100.117/npels/student/CourseIndex.aspx?c=%s&m=%s" % (self.user.class_id, lesson)
        # self.request_url(url)

    def __get_class_id(self):
        pass

    def __get_read_name(self):
        pass

    def login(self):
        if self.user is None:
            raise "Please login Frist~"
        user = self.user
        stu_id = user.stu_id
        stu_pw = user.stu_pw
        return self.__login(stu_id, stu_pw)

    def get_next_unit(self):
        status = self.user.get_status_info()
        for units in status.values():
            if not len(self.user.lessons) or units["lesson"] in self.user.lessons:
                for unit in units["units"]:
                    if not self.is_unit_finish(units["lesson"], unit["id"]):
                        return (units["lesson"], unit['id'])
        return (-1, -1)

    def switch_unit(self, lesson, unit):
        """
        选择单元
        :param unit: 指示第几个单元
        :return: 
        """
        # 设置当前单元和章节
        self.user.set_current_unit(unit)
        self.user.set_current_lesson(lesson)
        # unit_info = self.user.get_status_info()[lesson]["units"][unit - 1]
        print("%s：正在挂%s:%s同学的%s-Unit%s" % (
            time.ctime(),
            self.user.stu_id,
            self.user.stu_realname,
            lesson,
            unit))
        # print("Time： %s, User: %s, Lesson: %s, Unit : %d %d-%d" % (time.ctime(), self.user.stu_id, lesson,unit, unit_info["start_time"], unit_info["end_time"]) )
        classNo = self.user.class_id
        url1 = "http://192.168.100.117/npels/student/CourseStudy.aspx?t=studyunit&c=%s&m=%s&u=Unit_%02d&nocache=0.43957470136475796" % (classNo, lesson, unit)
        self.request_url(url1)
        url2 = "http://192.168.100.117/npels/student/LogTime.aspx?logType=checkneedauthorize&material=%s&nocache=0.6224367641918263" % (lesson)
        self.request_url(url2)
        url3 = "http://192.168.100.117/npels/Student/LogTime.aspx?logType=startnewstattime&stattype=1&material=%s&unit=Unit_%02d&nocache=0.43957470136475796&class=%s&nocache=0.7444460168559175" % (lesson, unit, classNo)
        self.request_url(url3)
        self.cookie.set_cookie(make_cookie('Material', lesson))
        self.cookie.set_cookie(make_cookie('ClassNo', classNo))
        #self.cookie.set_cookie(make_cookie('StudyStart','2017/10/2%2022%3A00%3A35'))

    def get_units_list(self, lesson):
        url = "http://192.168.100.117/npels/student/CourseIndex.aspx?c=%s&m=%s" % (self.user.class_id, lesson)
        data = self.request_url(url)
        re1 = re.compile(r'<div class="tagText">([0-9:]*)/([0-9:]*)</div>')
        units = []
        cnt = 1
        for m in re1.finditer(data):
            item = dict()
            item["id"] = cnt
            item["start_time"] = reduce(lambda x, y: int(x) * 60 + int(y), str(m.groups()[0]).split(':'))
            item["end_time"] = reduce(lambda x, y: int(x) * 60 + int(y), str(m.groups()[1]).split(':'))
            units.append(item)
            cnt = cnt + 1
        return units

    def get_status_info(self, rule = None):
        # location.href='CourseIndex.*>
        url = "http://192.168.100.117/npels/student/index.aspx"
        data = self.request_url(url)
        re1 = re.compile(r'CourseIndex.aspx\?c=(.*)&m=(.*)\'')
        status = dict()
        cnt = 1
        try:
            for m in re1.finditer(data):
                unit = dict()
                unit["lesson"] = str(m.groups()[1])
                unit["units"] = self.get_units_list(unit["lesson"])
                status[unit["lesson"]] = unit
                # classNo, lesson = self.user.class_id, self.user.get_current_lesson()
                # print(class_no, lesson)
            return status
        except:
            print("%s login again" % self.user.stu_id)
            self.login()
            self.get_status_info()

    def set_user(self, user):
        self.user = user

    def update_status_info(self):
        """
        
        :return: 
        """
        status = self.get_status_info()
        self.user.set_status_info(status)

    def is_unit_finish(self, lesson, unit_id):
        units = self.user.get_status_info()[lesson]["units"]
        if unit_id > len(units):
            raise "unit Error"
        # print(units[unit_id - 1])
        length = self.user.unit_length
        if length != -1:
            return units[unit_id - 1]["start_time"]  > length
        else:
            return units[unit_id - 1]["start_time"]  > units[unit_id - 1]["end_time"]

    def update_finish_flag(self, flag = 0):
        data = read_list()
        for user in data["users"]:
            if user["stu_id"] == self.user.stu_id:
                user["status"] = flag
                break
        write_list(data)
        self.user.set_finish_flag(flag)

    def load_config(self):
        pass

    def listen(self, sec):
        # lesson = self.user.get_current_lesson()
        # unit = self.user.get_current_unit()
        if not self.login():
            return False
        # for data in self.user.get_stu_info():
        #     lesson = data["lesson"]
        #     unit = 1
        #     self.update_status_info() #更新进度列表
        #     self.switch_unit(lesson, unit)
        self.update_status_info()
        lesson, unit = self.get_next_unit()
        if unit != -1:
            self.switch_unit(lesson, unit)
            while True:
                self.update_time()
                self.update_status_info()
                if self.is_unit_finish(lesson, unit):
                    lesson, unit = self.get_next_unit()
                    if unit == -1:
                        print("挂完了%s" % self.user.get_current_lesson())
                        break
                    self.switch_unit(lesson, unit)
                time.sleep(sec)
            self.update_finish_flag(0)
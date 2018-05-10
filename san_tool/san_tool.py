# -*- coding=utf-8 -*-

import glob
from configparser import ConfigParser
import telnetlib
import os
import sys
import time
import threading
import datetime
import re
import subprocess

reload(sys)
sys.setdefaultencoding("utf-8")


# 读取交换机相关配置信息
def read_cfg():
    global sw_ip
    global sw_user
    global sw_password
    cfg = ConfigParser()
    cfg_file = 'swinfo.ini'
    cfg.read(cfg_file)
    sw_ip = cfg.get('switch', 'sw_ip')
    sw_user = cfg.get('account', 'sw_user')
    sw_password = cfg.get('account', 'sw_password')


# 检查交换机是否能ping通
class CheckConnect(object):
    def __init__(self, ip):
        self.ip = ip

    def checkping(self, avaiable_ip, unavaiable_ip):
        self.avaiable_ip = avaiable_ip
        self.unavaiable_ip = unavaiable_ip
        ping = subprocess.Popen('ping -n 1 ' + self.ip, stdout=subprocess.PIPE)
        result = ping.stdout.read().decode("GBK")
        word = "已接收 = 0"
        if word in result:
            self.unavaiable_ip = self.unavaiable_ip.append(self.ip)  # 不可用IP列表
        else:
            self.avaiable_ip = self.avaiable_ip.append(self.ip)  # 可用IP列表


class TelnetSwitch(object):
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password

    def tn_command(self, command):
        self.command = command

    def checklogin(self, maxlogin_ip):
        self.maxlogin_ip = maxlogin_ip
        tn_open = telnetlib.Telnet()
        tn_open.open(self.ip)
        # tn_open.set_debuglevel(2)
        tn_open.read_until(b"login: ")
        tn_open.write(self.username.encode('ascii') + b"\n")
        tn_open.read_until(b"Password: ")
        tn_open.write(self.password.encode('ascii') + b"\n")
        error = 'Sorry!'
        time.sleep(1)
        if error in tn_open.read_very_eager():  # 判断是否有最大登录数限制
            self.maxlogin_ip = self.maxlogin_ip.append(self.ip)
            # print "%-30s%-50s" % (self.ip, "< Max remote sessions for login:admin is 2 >")
        tn_open.close()

    def tn_login(self):
        global result
        tn_open = telnetlib.Telnet()
        tn_open.open(self.ip)
        tn_open.read_until(b"login: ")
        tn_open.write(self.username.encode('ascii') + b"\n")
        tn_open.read_until(b"Password: ")
        tn_open.write(self.password.encode('ascii') + b"\n")
        tn_open.write(self.command.encode('ascii') + b"\n")
        tn_open.write(b"exit\n")
        result = tn_open.read_all()
        tn_open.close()


class ShowMenu(object):
    def __init__(self, sw_name, sw_ip, port):
        self.sw_ip = sw_ip
        self.sw_name = sw_name
        self.sw_port = port

    def result_menu(self):
        sw_name = "交换机名:"
        sw_ip = "交换机IP:"
        sw_port = "端口号:"
        title4 = "查询结果"
        max = 56
        print("\n")
        print("+" + "-" * ((max / 2) - (int(len(title4.encode('GBK'))) / 2) - 3) + " " * 3 + title4.encode(
            'GBK') + " " * 3 + "-" * (
                  (
                      max - ((max / 2) - (int(len(title4.encode('GBK'))) / 2)) - int(
                          len(title4.encode('GBK')))) - 3) + "+")
        print("\n")
        print "%-24s%-22s%-16s" % (sw_name.encode('GBK'), sw_ip.encode('GBK'),
                                   sw_port.encode('GBK'))
        print "-" * 58
        print "%-24s%-22s%-16s" % (self.sw_name.encode('GBK'), self.sw_ip.encode('GBK'),
                                   self.sw_port.encode('GBK'))


def check_telnet_menu():
    max = 56
    title = "SAN交换机端口搜索工具"
    print("+" + "-" * max + "+")
    print("|" + " " * ((max / 2) - (int(len(title.encode('GBK'))) / 2)) + title.encode('GBK') + " " * (
        (max - ((max / 2) - (int(len(title.encode('GBK'))) / 2)) - int(len(title.encode('GBK'))))) + "|")
    print("+" + "-" * max + "+")
    print('< 支持格式: "10000090FA5AE006","10:00:00:90:fa:5a:e0:06" >'.encode('GBK'))
    print("\n交换机连通性检测:".encode('GBK'))
    title1 = "网络可达: " + str(len(avaiable_ip))
    print(
        "+" + "-" * ((max / 2) - (int(len(title1.encode('GBK'))) / 2) - 3) + " " * 3 + title1.encode(
            'GBK') + " " * 3 + "-" * (
            (max - ((max / 2) - (int(len(title1.encode('GBK'))) / 2)) - int(len(title1.encode('GBK')))) - 3) + "+")
    for i in avaiable_ip:
        print i

    title2 = "网络不可达: " + str(len(unavaiable_ip))
    print(
        "+" + "-" * ((max / 2) - (int(len(title2.encode('GBK'))) / 2) - 3) + " " * 3 + title2.encode(
            'GBK') + " " * 3 + "-" * (
            (max - ((max / 2) - (int(len(title2.encode('GBK'))) / 2)) - int(len(title2.encode('GBK')))) - 3) + "+")
    for i in unavaiable_ip:
        print i

    title3 = "超过最大连接数: " + str(len(maxlogin_ip))
    print(
        "+" + "-" * ((max / 2) - (int(len(title3.encode('GBK'))) / 2) - 3) + " " * 3 + title3.encode(
            'GBK') + " " * 3 + "-" * (
            (max - ((max / 2) - (int(len(title3.encode('GBK'))) / 2)) - int(len(title3.encode('GBK')))) - 3) + "+")
    for i in maxlogin_ip:
        print i


def check_all_ip():
    global avaiable_ip
    global unavaiable_ip
    global maxlogin_ip
    read_cfg()
    avaiable_ip = []
    unavaiable_ip = []
    maxlogin_ip = []
    threads1 = []
    for ip in sw_ip.split(","):
        check_ip = CheckConnect(ip)
        t1 = threading.Thread(target=check_ip.checkping, args=(avaiable_ip, unavaiable_ip,))
        threads1.append(t1)
    for th in threads1:
        th.setDaemon(True)
        th.start()
    th.join()

    threads2 = []
    for ip in avaiable_ip:
        check_max_login = TelnetSwitch(ip, sw_user, sw_password)
        t2 = threading.Thread(target=check_max_login.checklogin, args=(maxlogin_ip,))
        threads2.append(t2)

    for th in threads2:
        th.setDaemon(True)
        th.start()
    th.join()


def exec_qeury(ip):
    sw_ip = ip
    t1 = TelnetSwitch(sw_ip, sw_user, sw_password)
    t1.tn_command("switchshow\nswitchname")
    t1.tn_login()
    sw_name = result.split("\n")[-2].split(":")[0]  # 取最后第二行，再截取出switchname
    for i in enumerate(result.split("\n")):
        if str(query_wwn) in i[1]:
            menu = ShowMenu(sw_name, sw_ip, (i[1].split()[0]))
            menu.result_menu()


def thread_query():
    threads = []
    for i in range(len(avaiable_ip)):
        t = threading.Thread(target=exec_qeury, args=(avaiable_ip[i],))
        threads.append(t)
    for i in range(len(avaiable_ip)):
        threads[i].setDaemon(True)
        threads[i].start()
        # print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "  " + threading.current_thread().name
    for i in range(len(avaiable_ip)):
        threads[i].join()


if __name__ == '__main__':
    os.system("cls")
    read_cfg()
    check_all_ip()
    check_telnet_menu()
    while True:
        input_wwn = raw_input(unicode('\n输入需要查询的wwn: ', 'utf-8').encode("GBK"))
        if len(input_wwn) == 16:
            query_wwn = ':'.join(re.findall('..', input_wwn)).lower()
            break
        elif len(input_wwn) == 23:
            query_wwn = input_wwn.lower()
            break
        else:
            propmt = raw_input(unicode('\n非法格式的wwn.\n重新查询:[y]，退出查询:[n] (y/n)? ', 'utf-8').encode("GBK"))
            if propmt == 'Y' or propmt == 'y':
                continue
            elif propmt == 'N' or propmt == 'n':
                exit()
    start = time.time()
    thread_query()
    end = time.time()
    elapsed = float('%.2f' % (end - start))
    print("\n查询时间: ".encode('GBK') + str(elapsed) + "秒".encode('GBK'))
    raw_input(unicode('\n回车退出！ ', 'utf-8').encode("GBK"))

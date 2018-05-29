# -*- coding=utf-8 -*-

import glob
from configparser import ConfigParser
import telnetlib
import time
import datetime
import re
import sys
import os
import xlwt

reload(sys)
sys.setdefaultencoding("utf-8")


def read_cfg():
    """ 读取交换机配置信息 """
    global sw_ip
    global sw_user
    global sw_password
    cfg = ConfigParser()
    cfg_file = 'swinfo.ini'
    cfg.read(cfg_file)
    sw_ip = cfg.get('switch', 'sw_ip')
    sw_user = cfg.get('account', 'sw_user')
    sw_password = cfg.get('account', 'sw_password')


def head_style():
    """
    颜色值:
　　0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue,
　　5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon,
　　17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow ,
　　20 = Dark Magenta, 21 = Teal,
　　22 = Light Gray, 23 = Dark Gray
　　"""
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.bold = False
    font.height = 11 * 20
    font.colour_index = 1
    font.underline = False
    font.italic = True
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 17
    style.pattern = pattern
    style.font = font
    style.alignment = alignment
    return style


def xls_style():
    alignment = xlwt.Alignment()
    alignment.vert = xlwt.Alignment.VERT_CENTER
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.underline = False
    font.italic = True
    style.font = font
    style.alignment = alignment
    return style


def error_style():
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.bold = False
    font.underline = False
    font.italic = True
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 5
    style.pattern = pattern
    style.font = font
    style.alignment = alignment
    return style


def successful_style():
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.bold = False
    font.underline = False
    font.italic = True
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 3
    style.pattern = pattern
    style.font = font
    style.alignment = alignment
    return style


def npiv_style():
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.bold = False
    font.underline = False
    font.italic = True
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 3
    style.pattern = pattern
    style.font = font
    style.alignment = alignment
    return style


class TelnetSwitch(object):
    def __init__(self, ip, username, password):
        """ telnet交换机 """
        self.ip = ip
        self.username = username
        self.password = password
        self.tn_open = telnetlib.Telnet()
        self.tn_open.open(host=self.ip, timeout=2)
        self.tn_open.read_until(b"login: ")
        self.tn_open.write(self.username.encode('ascii') + b"\n")
        self.tn_open.read_until(b"Password: ")
        self.tn_open.write(self.password.encode('ascii') + b"\n")


class CollectInfo(TelnetSwitch):
    def __init__(self, ip):
        """
        1、调用父类：TelnetSwitch
        2、判断密码是否正确，抛出异常AuthenticationError
        3、判断是否超过最大连接数，抛出异常MaxLoginError
        """
        self.ip = ip
        # TelnetSwitch.__init__(self, self.ip, sw_user, sw_password)
        super(CollectInfo, self).__init__(self.ip, sw_user, sw_password)
        time.sleep(3)
        body = self.tn_open.read_very_eager()
        if 'incorrect' in body:
            raise AuthenticationError("AuthenticationError")
        elif 'Sorry!' in body:
            raise MaxLoginError("MaxLoginError")

    def collect(self, command):
        """
        1、执行chassisshow命令，过滤出型号、序列号；
        2、执行switchshow命令，过滤出交换机名、端口wwn、端口总数、未激活端口数;
        3、执行version命令，过滤出OS版本;
        4、创建sw_hardware_info列表：[序列号,型号,交换机名,OS版本,端口总数,未激活端口数]
        5、创建port_wwn_map列表：[(端口号,wwn),(端口号,wwn)]
        """
        global sw_hardware_info
        global port_wwn_map
        self.tn_open.write(command.encode('ascii') + b"\n")
        self.tn_open.write(b"exit\n")
        rs = self.tn_open.read_all()
        port_wwn_map = []
        port_count = 0
        port_unlicense = 0
        sw_hardware_info = []
        for i in range(len(rs.split('\n'))):
            if re.findall(r'switchName:', rs.split('\n')[i]):
                switch_name = rs.split('\n')[i].split()[-1]
                sw_hardware_info.append(switch_name)
            elif re.findall(r'^Part Num:', rs.split('\n')[i]):
                model_number = rs.split('\n')[i].split()[-1]
                sw_hardware_info.append(model_number)
            elif re.findall(r'^Factory Serial Num:', rs.split('\n')[i]):
                serial_number = rs.split('\n')[i].split()[-1]
                sw_hardware_info.append(serial_number)
            elif re.findall(r'^Fabric OS:', rs.split('\n')[i]):
                os_version = rs.split('\n')[i].split()[-1]
                sw_hardware_info.append(os_version)
            elif re.findall(r'\sFC', rs.split('\n')[i]):
                port_count += 1
                if re.findall(r'Online      FC', rs.split('\n')[i]):
                    # 判断端口是否为NPIV
                    if str(rs.split('\n')[i].split()[8]) == '1':
                        npiv_port = rs.split('\n')[i].split()[0]
                        port_show = 'portshow ' + npiv_port
                        super(CollectInfo, self).__init__(self.ip, sw_user, sw_password)
                        time.sleep(3)
                        self.tn_open.write(port_show.encode('ascii') + b"\n")
                        self.tn_open.write(b"exit\n")
                        rs_port_show = self.tn_open.read_all()
                        npiv_ports = rs_port_show.splitlines()[
                                     int(rs_port_show.splitlines().index('portWwn of device(s) connected:') + 1):int(
                                         rs_port_show.splitlines().index('Distance:  normal'))]
                        for x in range(len(npiv_ports)):
                            port_wwn_map.append((npiv_port, npiv_ports[x].strip(), 'npiv'))
                    else:
                        port_wwn_map.append((rs.split('\n')[i].split()[0], rs.split('\n')[i].split()[8]))
            elif re.findall(r'No POD License', rs.split('\n')[i]):
                port_unlicense += 1
        sw_hardware_info.append(port_count)
        sw_hardware_info.append(port_unlicense)

    def logout(self):
        self.tn_open.close()


class MaxLoginError(Exception):
    """ 自定义异常 """
    pass


class AuthenticationError(Exception):
    """ 自定义异常 """
    pass


class OperateExcel(object):
    """
    1、创建Excel文件；
    2、创建汇总sheet，记录收集是否成功；（四种状态：成功、无法连接、密码错误、超过最大连接数）
    3、按IP地址创建配置信息sheet。
    """

    def __init__(self):
        self.filename = u'SAN交换机设备配置信息_' + time.strftime('%Y%m%d') + u'.xls'
        if os.path.exists(self.filename):
            os.remove(self.filename)
        self.f = xlwt.Workbook(encoding='utf-8')

    def add_sheet1(self):
        global sheet1
        sheet1 = self.f.add_sheet(u'Summary', cell_overwrite_ok=True)

    def add_sheet2(self, ip):
        global sheet2
        self.ip = ip
        sheet2 = self.f.add_sheet(self.ip, cell_overwrite_ok=True)
        row0 = [u'Switch Name', u'Switch IP', u'Model', u'Serial Number', u'OS Version', u'Ports(Total)',
                u'Ports(NO POD)',
                u'Port Number', u'WWN']
        for i in range(len(row0)):
            sheet2.write(0, i, row0[i], head_style())

        begin_row = 1
        if port_wwn_map:
            # 读取port_wwn_map列表（区分端口没有任何设备连接）
            for i in port_wwn_map:
                if len(i) > 2:
                    sheet2.write(begin_row, 7, i[0], xls_style())
                    sheet2.write(begin_row, 8, i[1], npiv_style())
                    begin_row += 1
                else:
                    sheet2.write(begin_row, 7, i[0], xls_style())
                    sheet2.write(begin_row, 8, i[1], xls_style())
                    begin_row += 1

            # 读取sw_hardware_info列表
            bottom_row = len(port_wwn_map)
            sheet2.write_merge(1, bottom_row, 0, 0, sw_hardware_info[2], xls_style())
            sheet2.write_merge(1, bottom_row, 1, 1, ip, xls_style())
            sheet2.write_merge(1, bottom_row, 2, 2, sw_hardware_info[1], xls_style())
            sheet2.write_merge(1, bottom_row, 3, 3, sw_hardware_info[0], xls_style())
            sheet2.write_merge(1, bottom_row, 4, 4, sw_hardware_info[3], xls_style())
            sheet2.write_merge(1, bottom_row, 5, 5, sw_hardware_info[4], xls_style())
            sheet2.write_merge(1, bottom_row, 6, 6, sw_hardware_info[5], xls_style())
        else:
            # 读取sw_hardware_info列表
            sheet2.write(1, 0, sw_hardware_info[2])
            sheet2.write(1, 1, ip)
            sheet2.write(1, 2, sw_hardware_info[1])
            sheet2.write(1, 3, sw_hardware_info[0])
            sheet2.write(1, 4, sw_hardware_info[3])
            sheet2.write(1, 5, sw_hardware_info[4])
            sheet2.write(1, 6, sw_hardware_info[5])

    def save_xls(self):
        self.f.save(self.filename)


def exec_cmd():
    for i in range(len(sw_ip.split(","))):
        ip = sw_ip.split(",")[i]
        try:
            start_time = time.time()
            collectinfo = CollectInfo(ip)
            collectinfo.collect(u'chassisshow\nswitchshow\nversion\n')
            collectinfo.logout()
            operateexcel.add_sheet2(ip)
        except MaxLoginError:
            print "[" + str(ip) + "]  " + "Max remote sessions!"
            sheet1.write(i, 0, ip, error_style())
            sheet1.write(i, 1, 'Max remote sessions!', error_style())
        except AuthenticationError:
            print "[" + str(ip) + "]  " + "Login incorrect!"
            sheet1.write(i, 0, ip, error_style())
            sheet1.write(i, 1, 'Login incorrect!', error_style())
        except Exception as err:
            print "[" + str(ip) + "]  " + "Unable to connect!"
            sheet1.write(i, 0, ip, error_style())
            sheet1.write(i, 1, 'Unable to connect!', error_style())
        else:
            print "[" + str(ip) + "]  " + "Successful and time elapsed: " + str(
                round((time.time() - start_time), 2)) + "s"
            sheet1.write(i, 0, ip, successful_style())
            sheet1.write(i, 1, 'Successful!', successful_style())


if __name__ == '__main__':
    start_time = time.time()
    print('\nInformation is being collected ... \n')
    read_cfg()
    operateexcel = OperateExcel()
    operateexcel.add_sheet1()
    exec_cmd()
    operateexcel.save_xls()
    print "\nComplete and time elapsed: {0}s".format(float('%.2f' % (time.time() - start_time)))

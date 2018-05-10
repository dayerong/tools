# -*- coding=utf-8 -*-

import time
import os
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException
import sys
import getpass
import datetime
import threading
import xlwt


class CiscoDevice(object):
    def __init__(self, username, password, ip, enablepass):
        self.ip = ip
        self.username = username
        self.password = password
        self.enablepass = enablepass
        self.cisco = {
            'device_type': 'cisco_ios_telnet',  # telnet
            # 'device_type': 'cisco_ios',   # ssh
            'username': username,
            'password': password,
            'ip': ip,
            'port': 23,
            'secret': enablepass
        }
        self.net_connect = ConnectHandler(**self.cisco)
        self.net_connect.enable()
        self.hostname = self.net_connect.find_prompt().replace("#", "")

    def device_output(self):
        timestr = time.strftime('%Y%m%d', time.localtime(time.time()))
        for cmds in open(r'command_list.txt', 'r'):
            cmd = cmds.replace('\n', '')
            filename = os.getcwd() + '\\' + output_dir + '\\' + (
                u'{0}_{1}_{2}.txt'.format(self.ip, self.hostname, timestr))
            output_list[self.ip] = (self.hostname, filename)
            save = open(filename, 'a')
            output = self.net_connect.send_command(cmd)
            time.sleep(1)
            separate = self.hostname + "# " + cmd
            save.write(separate)
            save.write("\n")
            save.write(output)
            save.write("\n")
            save.close()

    def switch_info(self):
        serial_number = self.net_connect.send_command('show version | in Processor board ID').split('ID')[1].strip()
        model_number = self.net_connect.send_command('show version | in Model number').split('\n')[0].split(':')[
            1].strip()
        info_list[self.ip] = (self.hostname, model_number, serial_number)

    def router_info(self):
        serial_number = self.net_connect.send_command('show version | in Processor board ID').split('ID')[1].strip()
        model_number = ' '.join(self.net_connect.send_command('show version | in memory').split(' ')[:2])
        info_list[self.ip] = (self.hostname, model_number, serial_number)


def exec_cmd(ip, row):
    try:
        ciscodevice = CiscoDevice(username, password, ip, enablepass)
    except (EOFError, NetMikoTimeoutException):
        sheet1.write(row, 0, ip)
        sheet1.write(row, 1, 'Unable to connect!')
    except (EOFError, NetMikoAuthenticationException):
        sheet1.write(row, 0, ip)
        sheet1.write(row, 1, 'Username or password is wrong!')
    except (ValueError, NetMikoAuthenticationException):
        sheet1.write(row, 0, ip)
        sheet1.write(row, 1, 'The enable password is wrong!')
    except Exception as err:
        sheet1.write(row, 0, ip)
        sheet1.write(row, 1, 'Unable to connect!')
    else:
        ciscodevice.device_output()
        try:
            ciscodevice.switch_info()
            sheet1.write(row, 0, ip)
            sheet1.write(row, 1, 'Successful.')
        except IndexError:
            ciscodevice.router_info()
            sheet1.write(row, 0, ip)
            sheet1.write(row, 1, 'Successful.')
        ciscodevice.net_connect.disconnect()


def thread_cmd():
    threads = []
    for i in range(len(open('cisco_ip_list.txt', 'r').readlines())):
        f = open('cisco_ip_list.txt', 'r')
        ips = f.readlines()[i].replace('\n', '')
        t = threading.Thread(target=exec_cmd, args=(ips, i,))
        threads.append(t)
    for i in range(len(open('cisco_ip_list.txt', 'r').readlines())):
        threads[i].setDaemon(True)
        threads[i].start()
    for i in range(len(open('cisco_ip_list.txt', 'r').readlines())):
        threads[i].join()


def xls_style():
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.colour_index = 4
    font.underline = True
    font.italic = True
    style.font = font
    return style


def add_output_dir():
    global output_dir
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)


def add_xls():
    global f
    global sheet1
    global sheet2
    global sheet3
    filename = u'Cisco设备配置信息_' + time.strftime('%Y%m%d') + '.xls'
    if os.path.exists(filename):
        os.remove(filename)
    f = xlwt.Workbook(encoding='utf-8')
    sheet1 = f.add_sheet(u'Summary', cell_overwrite_ok=True)
    sheet2 = f.add_sheet(u'Output Detail', cell_overwrite_ok=True)
    sheet3 = f.add_sheet(u'Device Info', cell_overwrite_ok=True)


def output_to_xls():
    # sheet2
    begin_row = 0
    for k, v in output_list.items():  # 读字典
        row = (k, v[0], v[1])
        for i in range(len(row)):
            if i == 2:
                link = str(row[i])
                sheet2.write(begin_row, i, xlwt.Formula('HYPERLINK("%s") ' % link), xls_style())
            else:
                sheet2.write(begin_row, i, row[i])
        begin_row += 1

    # sheet3
    row0 = ['No.', 'Hostname', 'IP', 'Model Number', 'Serial Number']
    for i in range(len(row0)):
        sheet3.write(0, i, row0[i])
    begin_row = 1
    for k, v in info_list.items():  # 读字典
        row = (begin_row, v[0], k, v[1], v[2])
        for i in range(len(row)):
            sheet3.write(begin_row, i, str(row[i]).strip())
        begin_row += 1
    filename = u'Cisco设备配置信息_' + time.strftime('%Y%m%d') + '.xls'
    f.save(filename)


if __name__ == '__main__':
    info_list = {}
    output_list = {}
    print('User Access Verification\n')
    username = raw_input('Username:')
    password = getpass.getpass('Password:')
    enablepass = getpass.getpass('Enable Password:')
    start_time = time.time()
    print('\nInformation is being collected ... ')
    add_output_dir()
    add_xls()
    thread_cmd()
    output_to_xls()
    print "Complete and time elapsed: {0}s".format(float('%.2f' % (time.time() - start_time)))

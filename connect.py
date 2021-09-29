# -*- coding:utf-8 -*-

import requests
import configparser
import getopt
import sys

from lxml import etree

TYP_DICT = {
    "0": "1教育网出口(国际,仅用教育网访问,适合看文献)",
    "1": "2电信网出口(国际,到教育网走教育网)",
    "2": "3联通网出口(国际,到教育网走教育网)",
    "3": "4电信网出口2(国际,到教育网免费地址走教育网",
    "4": "5联通网出口2(国际,到教育网免费地址走教育网)",
    "5": "6电信网出口3(国际,默认电信,其他分流)",
    "6": "7联通网出口3(国际,默认联通,其他分流)",
    "7": "8教育网出口2(国际,默认教育网,其他分流)",
    "8": "9移动网出口(国际,无P2P或带宽限制)"
}

EXP_DICT = {
    "3600": "1小时",
    "14400": "4小时",
    "39600": "11小时",
    "50400": "14小时",
    "0": "永久",
}

CONF_DICT = {
    "0": "在线配置",
    "1": "本地配置"
}


def get_wlt_ip():
    r = requests.get("http://wlt.ustc.edu.cn/cgi-bin/ip")
    if r.status_code != 200:
        print("Error in getting ip, please check your internet connection.")
        exit(0)
    ip = etree.HTML(r.text).xpath("//input[@name='ip']/@value")
    return ip[0]


def print_dict(dic: dict, padding: str):
    for k in dic.keys():
        print(padding + str(k) + ": " + str(dic[k]))


def online_conf(name: str, password: str):
    data = {
        "cmd": "login",
        "name": name,
        "password": password,
        "ip": get_wlt_ip(),
        "url": "URL",
        "set": "%D2%BB%BC%FC%C9%CF%CD%F8"
    }
    online_request = requests.post("http://wlt.ustc.edu.cn/cgi-bin/ip", data=data)
    if online_request.status_code != 200:
        return "Error in online config mode, please check your internet connection."
    online_request.encoding = "gbk"
    online_text = online_request.text
    if "信息：网络设置成功" in online_text:
        index1 = online_text.index("出口: ")
        index2 = online_text.index("权限: ")
        return "设置成功\t" + online_text[index1: index2 - 5] + "\t" + online_text[index2: index2 + 6]
    else:
        return "设置失败，请重试"


def local_conf(name: str, password: str, typ: str, exp: str):
    data = {
        "cmd": "login",
        "name": name,
        "password": password,
        "ip": get_wlt_ip(),
        "url": "URL",
        "go": "%B5%C7%C2%BC%D5%CA%BB%A7"
    }
    login_request = requests.post("http://wlt.ustc.edu.cn/cgi-bin/ip", data=data)
    if login_request.status_code != 200:
        return "Error in local config mode, please check your internet connection."
    cookie = login_request.headers.get("Set-Cookie")
    cookie = {"rn": cookie[3:]}
    set_request = requests.get(
        "http://wlt.ustc.edu.cn/cgi-bin/ip?cmd=set&url=URL&type=" + typ + "&exp=" + exp + "&go=+%BF%AA%CD%A8%CD%F8%C2%E7+",
        cookies=cookie)
    if login_request.status_code != 200:
        return "Error in setting network, please check your internet connection."
    set_request.encoding = "gbk"
    set_text = set_request.text
    if "信息：网络设置成功" in set_text:
        index1 = set_text.index("出口: ")
        index2 = set_text.index("权限: ")
        return "设置成功\t" + set_text[index1: index2 - 5] + "\t" + set_text[index2: index2 + 6] + "\t" + "时间：" + EXP_DICT[
            exp]
    else:
        return "设置失败，请重试"


if __name__ == "__main__":
    ini_file = "connect.ini"
    opts, args = getopt.getopt(sys.argv[1:], "hlu:p:t:d:c:i:",
                               ["help", "list", "username=", "password=" "type=", "duration=", "config=", "ini="])
    for opt, arg in opts:
        if opt == "-i" or opt == "-ini":
            ini_file = arg
    cp = configparser.ConfigParser()
    cp.read(ini_file)
    try:
        name = cp.get("user", "name")
        password = cp.get("user", "password")
        conf = cp.get("set", "conf")
        typ = cp.get("set", "type")
        exp = cp.get("set", "duration")
    except configparser.NoSectionError:
        print("Error in config file")
        exit(0)


    for opt, arg in opts:
        if opt == "-h" or opt == "--help":
            print("python connect.py")
            print("-u\t--username\n\t当前配置: " + name)
            print("-p\t--password\n\t当前配置: " + password)
            print("-t\t--type\n"
                  "\t当前配置：" + typ + "\n\t可选：")
            print_dict(TYP_DICT, "\t\t")
            print("-d\t--duration\n"
                  "\t当前配置：" + exp + "\n\t可选：")
            print_dict(EXP_DICT, "\t\t")
            print("-c\t--config\n"
                  "\t当前配置：" + conf + "\n\t可选：")
            print_dict(CONF_DICT, "\t\t")
            print("\t*在线配置会忽略本地type和duration配置")
            exit(0)
        if opt == "-l" or opt == "--list":
            print("当前配置：")
            print("\tusername: " + name)
            print("\tpassword: " + password)
            try:
                print("\tconf: " + CONF_DICT[conf])
            except KeyError:
                print("\tError in [set].conf: " + conf)
            try:
                print("\ttype: " + TYP_DICT[typ])
            except KeyError:
                print("\tError in [set].type: " + typ)
            try:
                print("\tduration: " + EXP_DICT[exp])
            except KeyError:
                print("\tError in [set].duration: " + exp)
            exit(0)
        if opt == "-u" or opt == "--username":
            name = arg
        if opt == "-p" or opt == "--password":
            password = arg
        if opt == "-t" or opt == "--type":
            typ = arg
        if opt == "-d" or opt == "--duration":
            exp = arg
        if opt == "-c" or opt == "--config":
            conf = arg

    if conf not in CONF_DICT.keys():
        print("Error in configuring [set].conf")
        exit(0)
    if conf == "0":
        print(online_conf(name, password))
        exit(0)

    if typ not in TYP_DICT.keys():
        print("Error in configuring [set].type. Reset to default value 0")
        typ = "0"
    if exp not in EXP_DICT.keys():
        print("Error in configuring [set].duration. Reset to default value 0")
        exp = "0"

    print(local_conf(name, password, typ, exp))

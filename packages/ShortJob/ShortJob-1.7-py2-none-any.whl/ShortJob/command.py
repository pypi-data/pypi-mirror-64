#!/usr/bin/env python3
# encoding: utf-8
# coding style: pep8
# ====================================================
#   Copyright (C)2020 All rights reserved.
#
#   Author        : Xin-Xin MA
#   Email         : xxmawhu@163.com
#   File Name     : command.py
#   Create Time   : 2020-03-14 14:50
#   Last Modified : 2020-03-14 14:50
#   Describe      :
#
# ====================================================
import os
import ConfigParser

"""
dir: default, the default execute commands associated with one special type.
@key: file type, "C", "cxx", "cc", "cpp", "c++", "py", "sh", "csh"
@value: the execute commands, "root -l -b -q", "bash"
list: rootType
You can modify the command free in the file ~/.ShortJob/command
we define those type file belong to "ROOT"
["cxx", "C", "cc", "c++", "c"]
* in python3 the module "ConfigParser" is named as "configparser"
"""


class MyConfigParser(ConfigParser.ConfigParser):
    """set ConfigParser options for case sensitive."""
    def __init__(self, defaults=None):
        ConfigParser.ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr


default = {
    "cxx": "root -l -b -q",
    "C": "root -l -b -q",
    "c": "root -l -b -q",
    "cc": "root -l -b -q",
    "cpp": "root -l -b -q",
    "c++": "root -l -b -q",
    "py": "python",
    "sh": "bash",
    "csh": "tcsh",
}
localConfigFile = os.path.expanduser("~/.ShortJob/command")


def initConfig(execommand):
    """init the ConfigParser file, the commands is stored in ~/.ShortJob/command
    Args:
       execommand(dir): take the file type as key and the command as value
    Returns:
        void
    """
    local_config = MyConfigParser()
    local_config.add_section('command')
    for k in execommand:
        local_config.set('command', k, execommand[k])
    if not os.path.exists(os.path.expanduser("~/.ShortJob")):
        os.mkdir(os.path.expanduser("~/.ShortJob"))
    localFile = os.path.expanduser(localConfigFile)
    with open(localFile, 'w') as configFile:
        local_config.write(configFile)


def init(configfile):
    if not os.path.exists(configfile):
        initConfig(default)


def ReadConfig(configfile):
    init(configfile)
    local_config = MyConfigParser()
    local_config.read(configfile)
    d = {}
    for item in local_config.items("command"):
        d[item[0]] = item[1]
    return d


exe = ReadConfig(localConfigFile)
rootType = ["cxx", "C", "cc", "c++", "c"]

if __name__ == "__main__":
    for i in exe:
        print("{} --> {}".format(i, exe[i]))

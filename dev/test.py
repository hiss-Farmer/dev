# coding=utf-8
import sys
import os
"""创建用户"""
USER = ""
USER_PASS = ""

USER_GREP = os.system('cat /etc/passwd | grep USER')
print(USER_GREP)

if USER == USER_GREP:
    print("error.....:", USER_GREP)
    try:
        








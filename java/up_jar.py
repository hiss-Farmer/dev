# _*_ codinf:utf-8 _*_
import os
from shutil import copyfile

dir = "/opt/mall_jar"
cp_dir = "/opt/back_jar"
def InPut():
    print("-*" * 20)
    print("\n 1 注释 \n 2 注释 \n 3 注释 \n 4 注释")
    print("_*" * 20)
    xuanxian = int(input("请要操作选项："))


# print("-*" * 20)
# print("1 注释 \n\t 2 注释 \n\t 3 注释")


# 删除项目jar
while InPut == 1:
    # if xuanxian == 1:

    def rm_file():
        print("开始删除项目jar包")
        os.system('rm -rf /opt/mall_jar')
        file_jar = int(os.system("ls -a /opt/mall_jar"))
        file_jar == 0

    try:
        print("删除成功......")


    except Exception as opt:
        print("删除失败.....")


# 上传项目jar
while InPut() == 2:

    def up_file():
        os.system()
        print("*" *10)


# 备份项目jar
# dir = "/opt/mall_jar"
# cp_dir = "/opt/back_jar"

while InPut() == 3:
    def back_file():
        os.mkdir(cp_dir)
        copyfile(dir, cp_dir)
        print("目录:%s" % cp_dir)


    try:
        print("备份完成.....")
        break
    except EnvironmentError as back:
        print("错误信息为： %s" % back)


# 重启所有jar项目
while InPut() == 4:

    def resatrt():
        print("重启服务器上jar项目")


    try:

        os.system("ps -ef | grep jar| grep -v grep ")
        break
    except OSError as resat:
        print("重启错误信息：%s" % resat)


# 停止所有jar项目
while True:
    if InPut() == 5:
        def stop():
            print("停止所有jar项目")


        try:
            os.system("")
            continue
        except EnvironmentError as sto:
            print("停止报错：%s" % sto)

InPut()


import os
import time


def WgEt():
    os.system(' yum install -y yum-utils device-mapper-persistent-data lvm2')
    time.sleep(2)
    os.system('yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo')
    os.system("yum list docker-ce --showduplicates,
                yum install -y --setopt=obsoletes=0,
                docker-ce-17.03.2.ce-1.el7.centos.x86_64,
                docker-ce-selinux-17.03.2.ce-1.el7.centos.noarch")



def  GitHub():
    os.get_exec_path('https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG-1.8.md#v183')


os.system('systemctl restart  kuberctl')

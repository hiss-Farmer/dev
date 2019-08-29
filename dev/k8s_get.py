# -*- coding: utf-8 -*-
import os

S_registry = 'registry.cn-beijing.aliyuncs.com//'
D_registry = 'k8s.gcr.io/'

master_image = ['kube-apiserver:v1.15.1','kube-controller-manager:v1.15.1',
                'kube-scheduler:v1.15.1','kube-proxy:v1.15.1','pause:3.1','etcd:3.2.24','coredns:1.2.6','flannel:v0.10.0-amd64']

def PullImage(registry,images):
    print("一共%s个镜像" % (len(images),))
    index = 1
    for image in images:
        print("开始下载第【%d】个镜像----->>[%s]" %(index, image))
        cmd = "docker pull" + registry + image
        os.system(cmd)
        print("done!")
        index += 1

def TagImage(sregistry,dregistry,images):
    print("一共%s个镜像" %(len(images),))
    index = 1
    for image in images:
        print("开始tag第【%s】个镜像----->>【%s】-----[%s]" % (index,sregistry+image,dregistry+image))
        cmd = "docker tag" + sregistry + image + " " + dregistry + image
        os.system(cmd)
        print("done!")
        index += 1



if __name__ == '__main__':
    PullImage(S_registry,master_image)
    TagImage(S_registry,D_registry,master_image)

 # **Rockchip Linux Docker** 编译镜像用户指南

 

 前言

 概述

 Rockchip Linux Docker 编译镜像介绍以及使用指南。

 产品版本

  |芯片名称 |  内核版本|
  |----------| ------------|
  RK3588  |   Linux 5.10
  RK356X   |  Linux 4.19

 读者对象

 本文档（本指南）主要适用于以下工程师： 技术支持工程师

 软件开发工程师



 

## 1. 介绍


 Docker 是一个用于开发，交付和运行应用程序的开放平台,
 能够将应用程序与基础架构分开，从而可以快速交付软件。

 已验证系统：
| 系统版本 | 加载镜像 | 编译固件 |
| --- | --- | --- |
| ubuntu 14.04 | pass | pass |
| ubuntu 16.04 | pass | pass |
| ubuntu 18.04 | pass | pass |
| fedora21 | pass | pass |
| centos 7.6 | pass | pass |
| centos 7.5 | pass | pass |
| centos 7.4 | pass | pass |
| centos 7.2 | pass | pass |
| centos 6.0 | fail | fail |
+--------------+------------+------------+

## 2. 安装
1.  ubuntu
```bash
sudo apt-get install docker.io
```
2.  centos
```bash
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
```
3.  fedora
   ```bash
    dnf install docker-ce
```
## 3. 获取镜像
   参考`Rockchip\_Developer\_Guide\_Linux\_Software\_CN.`文档通用软件包获取方法章节。

## 4. 导入镜像

1.  加载固件
```bash
sudo docker import docker-image-build-rk3588-v1.0-21-11-08.tar buildrk3588:v1.0-21-11-08
rk@ubuntu:~/samba$ sudo docker import docker-image-build-rk3588-v1.0-21-11-08.tar
build-rk3588:v1.0-21-11-08
sha256:9bd0828dcb608eaf4d082c2deb94f4601e504341078f7e850e63ceab2e6008e4
```
2.  查看固件
   ```bash
sudo docker images
rk@ubuntu:~/samba$ sudo docker images
REPOSITORY TAG IMAGE ID CREATED SIZE
build-rk3588 v1.0-21-11-08 9bd0828dcb60 23 seconds ago 860MB
sudo docker run --rm --mount
type=bind,source=/home/rk/samba/rk3588_lite_sdk,target=/tmp/rk3588 -
   ```

3.  启动固件并mount源码到docker
```bash
sudo docker run --rm --mount
type=bind,source=/home/rk/samba/rk3588_lite_sdk,target=/tmp/rk3588 -i -t buildrk3588:v1.0-21-11-08 /bin/bash
source=/home/rk/samba/rk3588_lite_sdk //sdk源码路径
target=/tmp/rk3588 //docker镜像mount路径
rk@ubuntu:~/samba$ sudo docker run --rm --mount
type=bind,source=/home/rk/samba/rk3588_lite_sdk,target=/tmp/rk3588 -i -t buildrk3588:v1.0-21-11-08 /bin/bash
root@0979c9ebace9:/#
```
4.  编译sdk
```bash
cd /tmp/rk3588 //这里的/tmp/rk3588 目录就是上条指令mount的target目录
./build_emmc.sh //编译emmc固件
```
 注**:docker**镜像只有编译环境，
 所以需要加载**sdk**源码到**docker内编译。

### 5.  **FAQ**

1.  centos加载镜像报错：Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running

 需要关闭selinux才能加载镜像
 ```bash
 在/etc/sysconfig/docker中
将OPTIONS=’–selinux-enabled –log-driver=journald –signature-verification=false’
改为OPTIONS=’–selinux-enabled=false –log-driver=journald –signatureverification=false’
然后执行sudo systemctl start docker
 ```

2.  fedora21需要关闭系统selinux
```bash
1. 关闭selinux
编辑/etc/selinux/config, 找到SELINUX行修改为：SELINUX=disbabled;
2. reboot
3. systemctl restart docker
docker -d -D 前面3条指令不行的话再加上这个
```
3.  ubuntu 14.04导入镜像失败

 ubuntu14 不能直接用docker import 需要使用下面的方式导入：
 ```bash
  1.安装
sudo apt-get install docker.io
2.导入 ：
cat docker-image-build-rk3588-v1.0-21-11-08.tar | sudo docker import -
build-rk3588:v1.0-21-11-08
 ```

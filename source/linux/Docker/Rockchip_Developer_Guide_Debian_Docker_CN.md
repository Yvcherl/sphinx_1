# **Debian Docker**开发指南


前⾔概述

本⽂档介绍如何搭建Docker环境，在Ubuntu系统PC上编译libmali、gstreamer、mpp、xserver、libdrm等第
三仓库编译成deb包，然后安装到Debian系统中。

读者对象

本⽂档（本指南）主要适⽤于以下⼯程师： 技术⽀持⼯程师

软件开发⼯程师

各芯⽚系统⽀持状态

| 仓库         | 版本               | 系统   |
|------------------|--------------------|--------|
| glmark2          | 2021.02            | Debian |
| gst-plugins-base | 1.14.4/1.18.5      | Debian |
| gstreamer-rockchip | 1.14.4           | Debian |
| libdrm           | 2.4.97/2.4.104     | Debian |
| libdrm-cursor    | 1.4.0              | Debian |
| libmali          | 1.9.0              | Debian |
| mpp              | 1.5.0              | Debian |
| libv4l-rkmp     | 1.5.0              | Debian |
| openbox          | 3.6.1              | Debian |
| pcmanfm          | 1.2.5              | Debian |
| rga              | 2.1.0/2.2.0        | Debian |
| rkisp            | 2.2.0              | Debian |
| rkaiq            | 5.0                | Debian |
| xserver          | 1.20.4/1.20.11     | Debian |
| wifibt           | 1.0.0              | Debian |
| rktoolkit        | 1.0.0              | Debian |





##  1 **Rockchip Docker**

[Docker](https://github.com/docker/docker)是⼀个旨在让使⽤容器更轻松地创建、部署和运⾏应⽤程序的⼯具。Docker
容器允许开发⼈员将应⽤程序及其所需的所有部分打包在⼀起，例如库和其他依赖项，并将其作为⼀个包发送出去。通过这
样做，开发⼈员可以放⼼，该应⽤程序将在任何其他 Linux设备上运⾏，而不管该设备可能具有的⽤于与编写和测试代码的机器不同的任何⾃定义设置。

在某种程度上，Docker 有点像虚拟机。但与虚拟机不同的是，Docker
不是创建⼀个完整的虚拟操作系统，而是允许应⽤程序使⽤与它们运⾏的系统相同的
Linux内核，并且只需要应⽤程序附带尚未在主机上运⾏的组件。这显着提⾼了性能并减小了应⽤程序的⼤小。

重要的是，Docker 是[开源](https://opensource.com/resources/what-open-source)的。这意味着任何⼈都可以为
Docker 做出贡献并扩展它以满⾜⾃⼰的需求。

RockchipDocker可以参考第三⽅⽹站[docker-rockchip](https://github.com/Fruit-Pi/docker-rockchip)。

## 2 操作系统要求


要安装 Docker，您需要以下任⼀版本的 64 位Ubuntu 系统：

 - Jammy 22.04 (LTS)

 - Focal 20.04 (LTS)

 - Bionic 18.04 (LTS)

 - Xenial 16.04 (LTS)

-  Trusty 14.04 (LTS)

注意：dockerfile 默认⽤于 ARM 64位芯⽚。以下⽤于ARM 32位芯⽚：

### 2.1 安装 **Docker**

- 使⽤此命令安装最新版本的 Docker(在 ubuntu 14.04 中将 docker替换为 docker.io)：
  ```bash
    sudo apt-get install docker qemu-user-static binfmt-support
  ```
-  开始运⾏ Docker 守护进程：
  ```bass
  sudo service docker start
  ```

- 通过 dockerfile 构建 Docker 镜像：
 ```bash
 sudo docker build -t rockchip
 ```

即可得到⼀个名为"rockchip"的 Docker 镜像，其中包含⼀个 Debian多架构交叉编译环境。

### 2.2  构建应⽤

- 进⼊Docker环境：
  ```bash
  sudo docker run -it -v <package_dir>:/home/rk/packages rockchip /bin/bash
  ```

- 开始构建：

  对于 ARM 32位芯⽚：
  ```bash
    cd /home/rk/packages/<pkg_dev>
    DEB_BUILD_OPTIONS=nocheck dpkg-buildpackage -rfakeroot -b -d -uc -us -aarmhf
    ls ../ | grep *.deb
  ```

  对于 ARM 64位芯⽚：
  ```bash
    cd /home/rk/packages/<pkg_dev>
    DEB_BUILD_OPTIONS=nocheck dpkg-buildpackage -rfakeroot -b -d -uc -us -aarm64
    ls ../ | grep *.deb
  ```

### 2.3 修改**Docker**镜像

如果您想要修改 Docker 镜像，可以通过下⾯的命令：
```bash
sudo docker run -it rockchip /bin/bash
```

从容器退出后，使⽤如下的命令来保存你的更改。
```bash
sudo docker commit <container_id> rockchip
```
## 3.其他

要获取有关 docker的更多信息，请查看以下链接：[https://docs.docker.com](https://docs.docker.com/)

## 4.实例


 如何在 [libmali](https://github.com/Fruit-Pi/libmali)上⽣成libmali-bifrost-g52-g2p0-x11\_1.9-1\_arm64.deb
```bash
~/work/docker/docker-rockchip$sudo service docker start
~/work/docker/docker-rockchip$sudo docker build -t rockchip 。
~/work/docker/docker-rockchip$sudo docker run -it -v
/home/wxt/work:/home/rk/packages rockchip /bin/bash
rk@2888134f9c12：/$ cd /home/rk/packages/docker/libmali
rk@2888134f9c12:~/packages/docker/libmali$ DEB_BUILD_OPTIONS=nocheck dpkgbuildpackage -rfakeroot -b -d -uc -us -aarm64
```
上述步骤将获得 \~/packages/docker/ 的 debs

- 可获取⼀些第三⽅仓库编译⽣成 deb 包，⽐如：

[glmark2](https://salsa.debian.org/games-team/glmark2)
[libmali](https://github.com/Fruit-Pi/libmali)

[mpp](https://github.com/Fruit-Pi/mpp)

[rga](https://github.com/Fruit-Pi/linux-rga)

[rkwifbt](https://github.com/Fruit-Pi/rkwifibt)

[gstreamer-rockchip](https://github.com/Fruit-Pi/gstreamer-rockchip)

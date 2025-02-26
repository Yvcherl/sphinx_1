 # **Rockchip**第三⽅系统适配开发指南

 
 前⾔概述

 本⽂描述了第三⽅类Debian系统适配的开发流程。

 产品版本

  芯⽚名称  | 内核版本
  ---------- |------------
  RK3568    | Linux 4.19
  RK3588     |Linux 5.10

 读者对象

 本⽂档（本指南）主要适⽤于以下⼯程师： 技术⽀持⼯程师

 软件开发⼯程师

 






## 1. **RK**平台主要需要适配的硬件


 GPU：图形处理器（英语：graphics processingunit，缩写：GPU），⼜称显⽰核⼼、视觉处理器，主要⽤于加速⼏何转换和光照处理、⽴⽅环境材质贴图和顶点混合、纹理压缩和凹凸映射贴图、双重纹理四像素256位渲染引擎等，⽬前RK平台GPU硬件已经集成到SOC中。

 RGA：2D图形加速器，⽤于加速2D图形的旋转，裁剪，缩放等操作。⽬前RK平台RGA硬件已经集成到SOC中。

 VPU：视频编解码模块，⽤于加速视频编解码，⽀持多种格式。⽬前RK平台VPU硬件已经集成到SO中。

 ISP：ISP主要作⽤是对前端图像传感器输出的信号做后期处理等。⽬前RK平台ISP硬件已经集成到SOC中。

 NPU：嵌⼊式神经⽹络处理器（NPU）采⽤"数据驱动并⾏计算"的架构，特别擅⻓处理视频、图像类的
 海量多媒体数据。NPU处理器专⻔为物联⽹⼈⼯智能⽽设计，⽤于加速神经⽹络的运算，解决传统芯⽚在神经⽹络运算时效率低下的问题。⽬前RK平台NPU硬件已经集成到SOC中。

 Wi-Fi/BT：开发板上适配的短距通信模块。

## 2 **RK**平台主要适配软件介绍

| 源码位置 | 说明 |
| --- | --- |
| SDK/external/libmali | RK平台目前提供的针对硬件gpu的用户态函数接口,主要是opengl es通用接口，目前主流的类Debian的显示框架有xserver和wayland,对于适配系统的APP使用的软件接口也要做相应的修改。 |
| SDK/external/xserver | RK平台目前对xserver硬件加速的补丁，如果您的第三方系统显示框架走的是xserver,请参考这个仓库的补丁适配。 |
| SDK/external/linux-rga | RK平台目前提供的针对硬件RGA的用户态函数接口。 |
| SDK/external/mpp | RK平台目前提供的针对硬件VPU用户态函数接口。 |
| SDK/external/rknpu2 | RK平台目前提供的针对硬件NPU用户态函数接口。 |
| SDK/external/camera_engine_rkaiq | RK平台目前提供的针对硬件ISP用户态函数接口。 |
| SDK/external/drm-cursor | RK平台目前提供的针对硬件鼠标层用户态函数接口。 |


## 3. 软件开发适配特别说明

 因为软件适配的时候，类debian系统可能存在许多版本依赖，如果下述的包安装失败，需要您重新部署源码到您的⽬标机器去编译。

 编译命令：
 ```bash
 cd 源码⽬录
sudo apt build-dep .
sudo DEB_BUILD_OPTIONS=nocheck dpkg-buildpackage -rfakeroot -b -d -us
 ```

## 4. 显⽰服务的适配

 ### 4.1 概述

 类debian系统上的显⽰服务可以由下⾯⼏个部分组成：

 显⽰应⽤ + 图形显⽰框架 + 图形显⽰接⼝ + 处理图形显⽰的硬件

 显⽰应⽤⽬前主流的有x11, gnome,kde,
 xfce4,sdl2等等，图形显⽰框架主要包含wayland, xserver, gbm这三种,
 对于rockchip来说，图形显⽰接⼝⽬前只⽀持opengl，处理图形显⽰的硬件⾃然就是GPU。下⾯列举⼏种显⽰框架的组合情况：(注意本⽂档的写作时间，具体⽀持情况可以到各⾃的官⽅⽹站去确认)

| 显⽰应⽤ |  ⽀持的图形显⽰框架 |  ⽀持的图形显⽰接⼝ |
----------|----------------------|----------------------|
| x11      |  xserver            |  opengles/gbm       |
| gnome    |  xserver/wayland    |  opengles/gbm       |
| kde      |  xserver/wayland    |  opengles/gbm       |
| xfce4    |  xserver            |  opengles/gbm       |
| sdl2     |  xserver/wayland    |  opengles/gbm       |

 根据上⾯的表格，在适配类debian系统的时候，要先知道前端（即显⽰应⽤是什么），然后要了解图形显⽰框架⾛的是xserver还是wayland去，做针对性的适配。
### 4.2   **GPU**适配

 先确定您系统上使⽤的显⽰框架，是xserver还是wayland，(⽬前只⽀持这两种框架)
 然后安装

 SDK/debian/packages/\"ARCH\"/libmali/libmali-\*\*\*.deb

 ⽐如，系统在rk3588平台上使⽤x11，rk3588平台使⽤的gpu型号是valhall-g610-g6p0，那么，需要安装
 ```bash
 SDK/debian/packages/arm64/libmali/libmali-valhall-g610-g6p0-x11_1.9-1_arm64.deb
 ```

### 4.3 **RGA**适配

 安装包：
 ```bash
 SDK/debian/packages/'ARCH'/rga/*.deb
 ```

### 4.4  **drm-cursor**适配

 安装包：
 ```bash
 SDK/debian/packages/arm64/libdrm-cursor/*.deb
 ```

### 4.5  **xserver**适配

 因为xserver版本众多，您先确定您系统版本使⽤的xserver版本，然后基于我们的源码补丁，移植到您版
 本的xserver，然后再重新编译。

 ⽣成补丁：
 ```bash
 cd 源码⽬录
git format-patch e4f4521ca
 ```

 下⾯是编译好的1.20.11版本的安装包：
 ```bash
 SDK/debian/packages/'ARCH'/xserver/xserver-common_1.20.11-1_all.deb
SDK/debian/packages/'ARCH'/xserver/xserver-xorg-core_1.20.11-1_'ARCH'.deb
SDK/debian/packages/'ARCH'/xserver/xserver-xorg-legacy_1.20.11-1_'ARCH'.deb
 ```

 xserver还需要⼀个启动脚本做⼀些初始化操作，如果是类debian系统，可以尝试复制启动脚本进系统，如果不是, 请参考脚本⾃⾏配置：
 ```bash
 SDK/debian/overlay/etc/X11
 ```

### 4.6 如何验证是否适配成功

 显⽰服务加速使⽤opengles的标准接⼝，如果你的系统使⽤opengl，请移植成opengles，如果适配成功，当渲染画⾯或者拖动窗⼝的时候，去查看平台相关的gpu节点，会有gpu利⽤的变化，⽐如RK3588平台：
```bash
cat /sys/devices/platform/fb000000.gpu/utilisation
```
 注意：不同平台的gpu节点是不⼀样的。

## 5.  编解码服务的适配

### 5.1 概述

 编解码服务，由下⾯⼏个部分组成：

 上层的多媒体框架软件 + 中间层mpp + 硬件编解码器

 上层编解码框架在开源社区常⽤的有gstreamer等，下⽂中都是以gstreamer作为例⼦演⽰的,
 中间层mpp
 库，是作为通⽤第三⽅软件（如gstreamer）和硬件编解码器的中间层。

### 5.2  **mpp**适配

 安装包：
 `SDK/debian/packages/'ARCH'/mpp/*.deb`

 注意：⼀些节点的权限设置，需要参考:
 `SDK/debian/overlay/etc/udev/rules.d/99-rockchip-permissions.rules`

 验证mpp是否配置成功：
 ```bash
 # mpi_enc_test -w 1920 -h 1080 -t 7 -o /tmp/test.h264
# mpi_dec_test -w 1920 -h 1080 -t 7 -i /tmp/test.h264
 ```

### 5.3多媒体软件适配

 ⽤⼾的多媒体框架有许多，这⾥⽐较推荐的是⽤⼾的播放器直接调⽤mpp的接⼝去进⾏视频编解码的适
 配，具体请查看mpp的接⼝⽂档《Rockchip\_Developer\_Guide\_MPP\_CN.pdf》

### 5.4 **gstreamer**适配

 RK平台⽬前有适配⼀个gst-base的预编译包：
```bash
SDK/debian/packages/'ARCH'/gst-plugins-base1.0/*.deb
SDK/debian/packages/'ARCH'/gst-plugins-bad1.0/*.deb
SDK/debian/packages/'ARCH'/gst-plugins-good1.0/*.deb
```
 RK平台还⽀持gstreamer通⽤多媒体框架，需要您提前安装官⽅gstreamer组件（也可以安装上述的gst-base的预编译包，如果您的系统版本相兼容），然后再安装gst-rockchip插件：
```bash
SDK/debian/packages/'ARCH'/gst-rkmpp/*.deb
```
### 5.5 如何验证是否适配成功
```bash
sudo GST_DEBUG=2 gst-launch-1.0 playbin uri=file视频绝对路径 video-sink=“显⽰
sink” audio-sink=fakesink
```
 如果有mpp调⽤的字样，说明硬件解码成功适配。

## 6  **camera**服务适配

### 6.1 camera\_engine\_rkaiq适配
        -------------------------

 安装包：
 ```bash
 SDK/debian/packages/'ARCH'/rkaiq/camera_engine_rkaiq_'ARCH'.deb
 ```

### 6.2 如何验证是否适配成功 {#如何验证是否适配成功}

 可以使⽤v4l2命令查看是否抓图成功，并且查看抓出来的图是否正确：（注意：不同平台不同camera的
 节点，格式，分辨率等可能有所不同，请根据具体情况更换命令）
 ```bash
 v4l2-ctl -d /dev/video0 --set-fmtvideo=width=1920,height=1080,pixelformat=NV12 --stream-mmap=4 --stream-skip=3
--stream-to=/tmp/0.yuv --stream-count=1 --stream-poll
 ```

## 7.  **NPU**服务适配

### 7.1 rknn\_runtime适配
        -----------------

 rknn\_runtime主要是⽤⼾态的库，只要拷⻉它到客⼾的⽂件系统中即可。
```bash
SDK/external/rknpu2/Linux/librknn_api/'ARCH'/librknn_api.so
SDK/external/rknpu2/Linux/librknn_api/'ARCH'/librknnrt.so
```
### 7.2 rknn\_server适配

 rknn\_server主要是pc上使⽤rknntool2⼯具时候，要求板上通信所⽤的服务，如果在pc上训练好模型，转化为rknn后在导⼊板⼦上，是不需要这个服务的。
```bash
SDK/external/rknpu2/Linux/rknn_server/'ARCH'/usr/bin/*
```
### 7.3 rknn demo

 请参考
 ```bash
 SDK/external/rknpu2/examples
 ```

## 8 **Wi-Fi/BT** 服务适配

 详情请参考
 《Rockchip\_Developer\_Guide\_Linux\_WIFI\_BT\_CN.pdf》在SDK中有预编译包：
 ```bash
 SDK\debian\packages\'ARCH'\rkwifibt\*.deb
 ```

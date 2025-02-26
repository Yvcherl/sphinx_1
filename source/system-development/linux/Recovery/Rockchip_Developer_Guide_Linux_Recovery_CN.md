 # **Rockchip Linux Recovery**升级开发指南

 

 前言概述

 本文档主要介绍 Rockchip 处理器在 OTA 升级时的 recovery
 开发流程以及技术细节。 本文中详细介绍了

 该方案的开发过程以及注意事项。产品版本


|  芯片名称                                        |  内核版本  |
| -|-|
|  RK3308、RK3226、RK3399、RK3288、RK3326、PX30 等 |  Linux 4.4 |


 读者对象

 本文档（本指南）主要适用于以下工程师： 技术支持工程师

 软件开发工程师

 
## 1. **OTA**升级
### 1.1  概述
        ----
 OTA（Over-the-Air）即空间下载技术。 OTA 升级是 Android
 系统提供的标准软件升级方式。它功能强大，可以无损失升级系统，主要通过网络，例如
 WIFI、3G/4G 自动下载 OTA 升级包、自动升级，也支持通过下载 OTA 升级包到
 SD 卡/U 盘升级，OTA 的升级包非常的小，一般几 MB 到十几 MB。

 本文主要介绍了使用 OTA 技术升级时，本地升级程序 recovery
 执行升级的流程及技术细节，以便用户在开发过程中了解升级的过程及注意事项。

### 1.2 编译


 - **rootfs** 主系统

 rootfs 需要打开update 的支持，configs 文件配置
 BR2\_PACKAGE\_UPDATE=y。
 ```bash
 source envsetup.sh
#choose a combo number to build rootfs according to platform chip
make menuconfig
 ```
 具体配置如下：
```bash
Target packages --->
     [*] Rockchip BSP packages --->
          [*] Rockchip OTA update for linux
```

-  **Recovery**

 `buildroot/configs/rockchip/recovery.config`
 中已经将不同平台的recovery配置抽取出来了。

 只需系统根目录下执行：
 ```bash
 ./build.sh recovery
 ```

 成功后，会生成文件
 buildroot/output/rockchip\_rkxxxx\_recovery/images/recovery.img 。

 rkxxxx为 具体某一芯片名称。执行：
 ```bash
 ./mkfirmware.sh 
 ```

 会将生成的固件拷贝至 rockdev/目录下。与 recovery 相关的主要源码路径：

`external/recovery/` ：主要生成 recovery 二进制 bin 程序，recovery 模式下的关键程序。

 `external/rkupdate/` ：主要生成 rkupdate 二进制 bin 程序，解析update.img
 固件中各个分区数据，并执行对各分区执行升级的关键程序，该程序被recovery二进制bin程序内部调用。

 若有修改以上两个目录中的源码文件之后的编译方法：

1. `source envsetup.sh`
2. `选择某一平台的 recovery 配置
3. `make recovery-dirclean && make recovery`
4. `make rkupdate-dirclean && make rkupdate`
5. `./build.sh recovery`
6. `./mkfirmware.sh`
7. 烧写 recovery.img

### 1.3 升级流程


#### 1.3.1 升级固件准备
```bash
./build.sh updateimg
```

 修改`tools/linux/Linux\_Pack\_Firmware/rockdev/package-file]`
 ，根据需要升级的分区配置，修改该文件。

 根目录下执行命令：
 ```bash
 ./build.sh updateimg
 ```

 命令执行成功后，会将package-file指定的分区镜像打包生成update.img
 升级固件，放在 rockdev/目录下。使用该update.img 升级。

如果升级过程中遇到错误"Error！imageHead.uiTag
 !=0x57464B52"，该错误表明固件打包有错误，请按照上述操作，重新生成
 update.img 重试。

 ![](Rockchip_Developer_Guide_Linux_Recovery_CN_pic/media/image1.jpeg)
#### 1.3.2 升级过程

* 将升级固件 update.img 放在 SD 卡或 U 盘根目录或者设备的/userdata 目录下。
* Normal 系统下执行升级程序 `update ota /xxx/update.img`，设备将会进入 recovery 模式，并进行升级。
  可用的路径如下：
    * U 盘的挂载路径：/udisk
    * sdcard 的挂载路径：/mnt/sdcard/ 或 /sdcard
    * flash 的挂载路径：/userdata/
* 升级成功后会 reboot 到正常的 normal 系统。

 升级流程图如下：

![](Rockchip_Developer_Guide_Linux_Recovery_CN_pic/media/image2.jpeg){

### 1.4 恢复出厂模式

我们可以把可读写的配置文件保存在 userdata 分区，出厂固件会默认一些配置参数，用户使用一段时间后会生成或修改配置文件，有时用户需要清除这些数据，我们就需要恢复到出厂配置。直接运行 update 后面不加任何参数或者加 factory/reset 参数均可进入 recovery 后恢复出厂配置。

### 1.5 注意事项

- 打包 update.img 固件时需要注意，升级固件不一定要全分区升级，可修改 package-file 文件，将不要升级的分区去掉，这样可以减少升级包（update.img）的大小。
- package-file 中 recovery.img 如果打包进去的话，不会在 Recovery 模式中升级，为了预防升级 recovery.img 过程中掉电导致后面其他分区无法正常升级的问题，该分区升级放在 normal 系统下升级，即，执行 update 命令时会先检测 update.img 升级包中是否有打包 recovery.img，若有则升级 recovery 分区，再进入 Recovery 模式升级其他分区固件。
- misc 分区不建议打包进 update.img 中，即使有打包进去，也会在升级程序中加载判断到而忽略该分区，即使升级了 misc 分区，升级成功后 recovery 程序仍会清空 misc 分区中所有的命令及参数，从而导致达不到预想的结果。
- 如果将 update.img 升级包放置在 flash 中的 userdata 分区，则需要保证 package-file 中括不包括 userdata.img 被打包进去，原因是可能会导致文件系统的损坏，升级成功后可能使 oem 或 userdata 分区 mount 不成功。若从 SD 卡或 U 盘升级时，可以打包 userdata.img，从而对 userdata 分区进行升级。升级完成后会对 userdata 分区重新 resize 操作。
## 2. 运行调试

### 2.1 Recovery 模式中 log 的查看

在 `buildroot/output/rockchip_rkxxxx_recovery/target` 目录下创建一个隐藏文件，

```bash
touch .rkdebug
```
 可将Recovery 模式中升级的 log 在串口中打印出来。

![](Rockchip_Developer_Guide_Linux_Recovery_CN_pic/media/image3.jpeg){width="6.198377077865267in"
height="4.275103893263342in"}

 另外一种是通过查看 userdata/recovery/Log 文件

 升级之后，在设备 userdata/recovery 目录中查看 log 文件。
 ```bash
 cat userdata/recovery/log
 ```

### 2.2 带屏设备与不带屏设备

 Recovery 执行过程中如果失败，且提示如下 log 信息：
```bash
failed to read font: res=-1, fall back to the compiled-in font
cannot find/open a drm device: No such file or directory
```
 从log 可知，找不到或者打不开一个 drm
 设备，此时如果开发的是带屏的设备，需要接上显示屏，如果是开发不带屏的设备需要进行如下配置。

 默认 SDK 代码 recovery 配置中为不带屏设备。
```bash
cd Path_to_SDK/buildroot/package/rockchip/recovery
vim recovery.mk
```
 打开 中的 recovery Makefile 文件如下图所示：

![](Rockchip_Developer_Guide_Linux_Recovery_CN_pic/media/image4.png){width="6.20838801399825in"
height="4.6275in"}

 上图中，若配置了BR2\_PACKAGE\_RECOVERY\_NO\_UI，则定义RecoveryNoUi的宏定义为true。否则会
 链接显示相关的库。
 ```bash
ifeq ($(BR2_PACKAGE_RECOVERY_NO_UI),y)
TARGET_MAKE_ENV += RecoveryNoUi=true
else
RECOVERY_BUILD_OPTS += -lz -lpng -ldrm
RECOVERY_DEPENDENCIES += libzlib libpng libdrm
endif
 ```
若不带屏设备需要在 Recovery 配置中打开 `BR2_PACKAGE_RECOVERY_NO_UI` 的配置。

修改后的编译：
1. `source envsetup.sh rockchip_xxxx_recovery` (xxxx 为具体芯片平台)
2. `make menuconfig`，打开配置 No UI for recovery。
3. `make recovery-dirclean && make recovery`
4. `./build.sh recovery`
5. `./mkimage.sh`
6. 烧录 rockdev/recovery.img

#### 2.2.1 带屏设备的旋转与显示

- 若需要将 Recovery 升级过程中显示的界面根据显示设备的方向做一些旋转操作，可按如下说明操作。
  1. 更新 Recovery 代码到最新。
  2. 修改 `minui/graphics.c` 中 `gr_init` 函数调用的 `gr_rotate` 接口函数的参数。旋转参数说明：
     - `ROTATION_NONE` 默认不做旋转
     - `ROTATION_RIGHT` 顺时针旋转 90°
     - `ROTATION_DOWN` 顺时针旋转 180°
     - `ROTATION_LEFT` 顺时针旋转 270°
  3. 重新编译 Recovery，生成 Recovery 分区固件，烧录。
- 若需要调整 UI 显示的亮度，可修改 `gr_color` 接口中最后一个参数 alpha 透明度。最大值 255 为不透明，最小值 0 表示全透明。
- 更换 Recovery 中 UI 显示的背景图片。可自行更换 `external/recovery/res/images` 目录下的图片文件，保持文件名不变。

## 2.3 Debian 与 Ubuntu 系统的升级

与 Buildroot recovery 升级一样，该 Recovery OTA 升级方案也支持 Debian 或 Ubuntu 系统下的升级。由于 Recovery 模式下升级需要通过设备各个分区节点来识别并写入不同设备分区节点的固件数据，Buildroot 系统是通过 udev 中的别名方式（by-name）来对设备分区节点做了通用的易识别的处理。Debian 或 Ubuntu 系统中因为缺少这样的方式，导致了实际中不 Recovery 不能正常运行的情况，所以只需要将 Debian 或 Ubuntu 系统中设备分区的节点也跟 Buildroot 系统下可通过 by-name 别名方式标识出来，Recovery 即可正常工作。

具体修改方式如下：

`buildroot/output/rockchip_rkxxxxx/target/lib/udev/rules.d/61-partition-init.rules`，或者 `buildroot/output/rockchip_rkxxxxx_recovery/target/lib/udev/rules.d/61-partition-init.rules`

拷贝到 Debian 或 Ubuntu 系统下相关的位置，如 `rootfs/overlay-debug/lib/udev/rules.d/` 下。此处 rkxxxxx 为具体某一 rk 芯片平台（RK3308、RK3328、RK3399、RK3326 等）。修改的目的就是开机启动后可以将 Debian 系统或 Ubuntu 系统中各个分区节点形如 `/dev/mmcblk0p0`、`/dev/mmcblk0p1`、`/dev/mmcblk0p2`、`/dev/mmcblk0p3`... 修改为 `/dev/block/by-name/uboot`、`/dev/block/by-name/misc`、`/dev/block/by-name/boot`、`/dev/block/by-name/rootfs`... 等。
 若还是出现如下类似设备节点：
```bash
root@linaro-alip:~# ls /dev/block/
179:0 179:3 179:5 179:7 179:96 7:0 7:3 7:6
179:1 179:32 179:6 179:8 1:0 7:1 7:4 7:7
179:2 179:4 179:64 179:9 254:0 7:2 7:5
```
 可尝试将 61-partition-init.rules放在 Debian 或 Ubuntu

## 3.  **SD** 卡制作启动盘升级

 本章节主要为了解决使用 SD 卡启动，进行裸片升级的需求，详细描述 SD
 卡启动盘的制作及相关升级的问题。

 使用工程目录中`tools\windows\SDDiskTool`

 中的 SD 卡启动盘升级制作工具制作 SD卡启动盘。

 ![](Rockchip_Developer_Guide_Linux_Recovery_CN_pic/media/image5.jpeg)
 选择固件中选择打包好的 update.img 文件。

 所有准备工作完成后，点击开始创建按钮，如果创建成功，会弹窗提示。

 此时 SD 卡中根目录会存在两个文件，其中选择升级的固件
 update.img，会被命名为 sdupdate.img.

 所有准备工作做好后，设备中插入 SD 卡，并重新上电。

 Log 中如果出现下面内容，说明 SD 卡启动设备成功：
 ```bash
 U-Boot 2017.09-g1bee468 (Oct 11 2018 - 16:53:06 +0800) V1.000
Model: USM-110 a102-1
Board:Advantech usm110_rk3288 Board,HW version:0
DRAM: 2 GiB
Relocation Offset is: 7ff5a000
PMIC: RK808
vdd_arm 1100000 uV
vdd_gpu 1100000 uV
vcc_io 3300000 uV
regulator(LDO_REG2) init 3300000 uV
regulator(LDO_REG3) init 1100000 uV
regulator(LDO_REG4) init 1800000 uV
regulator(LDO_REG5) init 3300000 uV
regulator(LDO_REG6) init 1100000 uV
regulator(LDO_REG7) init 1800000 uV
regulator(LDO_REG8) init 1800000 uV
MMC: dwmmc@ff0c0000: 1, dwmmc@ff0f0000: 0
SF: Detected w25q32bv with page size 256 Bytes, erase size 4 KiB, total 4
MiB
*** Warning - bad CRC, using default environment
In: serial
Out: serial
Err: serial
switch to partitions #0, OK
mmc1 is current device
do_rkimg_test found IDB in SDcard
Boot from SDcard
enter Recovery mode!
SF: Detected w25q32bv with page size 256 Bytes, erase size 4 KiB, total 4
MiB
Skipped ethaddr assignment due to invalid,using default!
Net: No ethernet found.
Hit any key to stop autoboot: 0
ANDROID: reboot reason: "recovery"
FDT load addr 0x10f00000 size 263 KiB
Booting kernel at 0x3575c70 with fdt at 42cf470...
 ```

 若串口 log 中打印如下的 log，说明 SD 卡启动进入了 recovery
 固件对裸片设备的升级过程。
```bash
firmware update will from SDCARD.
is_sdcard_update out
sdupdate_package = /mnt/sdcard/sdupdate.img
Command: "/usr/bin/recovery"
sdboot update will update from /mnt/sdcard/sdupdate.img
start with main.
```
## 4. 附录
### 4.1 分区说明

 misc 其实是英文 miscellaneous 的前四个字母，杂项、混合体、大杂烩的意思。
misc 分区的概念来源于 Android 系统，Linux 系统中常用来作为系统升级时或者恢复出厂设置时使用。
misc 分区的读写：misc 分区在以下情况下会被读写。
1) Uboot：设备加电启动时，首先启动 Uboot，在 Uboot 中会读取 misc 分区的内容。根据 misc分区中
command 命令内容决定是进入正常系统还是 recovery 模式。
Command 为 boot-recovery，则进入 recovery 模式。
Command 为空，则进入正常系统。
2) Recovery：在设备进入 recovery 模式中，可以读取 misc 分区中 recovery 部分的内容，从而执行不同的
动作，或升级分区固件，或擦除用户分区数据，或其他操作等等。
misc 分区的结构及内容：
misc 分区的结构组成详见下图。。

![](Rockchip_Developer_Guide_Linux_Recovery_CN_pic/media/image6.png){width="6.121101268591426in"
height="2.37in"}

 下面以 RK3308 平台使用的 misc 分区为例，使用 winhex 或 ultraEdit
 等工具，以二进制形式打开misc.img 文件，在距文件开始位置偏移 16K（16384
 Byte）字节位置处开始，存放 BootLoader Msg结构体的内

 容。

![](Rockchip_Developer_Guide_Linux_Recovery_CN_pic/media/image7.jpeg)

 Recovery 中支持的命令部分，可参考 external/recovery/recovery.c 中
 OPTIONS 结构中内容。

#### 4.1.1  misc.img 选择

 SDK `device/rockchip/rockimg`根目录

 置选择拷贝哪一个 misc.img 的文件。
```bash
.
├ ── blank-misc.img #空白的 misc 分区文件
├── pcba_small_misc.img #不常用
├── pcba_whole_misc.img #不常用
└── wipe_all-misc.img #格式化用户分区使用的 misc 分区文件
```
 目录下是经常使用的 misc.img 文件。生成固件的时候根据配

 常用的两种 misc.img 文件是 blank-misc.img 与 wipe\_all-misc.img。

 打开具体芯片平台的 BoardConfig.mk 文件， 可配置 misc.img 的具体使用。
 ```bash
 cd device/rockchip/rkxxxx
vim BoardConfig.mk
 ```

![](Rockchip_Developer_Guide_Linux_Recovery_CN_pic/media/image8.jpeg)
从上图中可看到，默认使用 `wipe_all-misc.img` 作为 misc 分区的固件，使用该 misc 固件，烧写后会格式化用户（/userdata 或 /data）分区与客制（/oem）分区的数据。若希望开机不进入 recovery 模式，而进入正常系统，可以修改 `BoardConfig.mk` 这里 misc image 的具体文件为 `blank-misc.img`。然后重新编译，生成新的固件。
### 4.2 **Recovery** 不同场景下的使用

  ####  4.2.1    第一次开机

 烧写过 misc.img、recovery.img
 的设备会进入第一次开机流程。串口log打印如下内容：
```bash
oot command: boot-recovery
Got arguments from boot message
Command: "recovery" "--wipe_all"
format '/dev/block/by-name/userdata' to ext2 filesystem
executing '/sbin/mke2fs'
executed '/sbin/mke2fs' done
executed '/sbin/mke2fs' return 0
executing '/sbin/e2fsck'
e2fsck 1.43.9 (8-Feb-2018)
Pass 1: Checking inodes, blocks, and sizes
Pass 2: Checking directory structure
Pass 3: Checking directory connectivity
Pass 4: Checking reference counts
Pass 5: Checking group summary information
/dev/block/by-name/userdata: 11/2304 files (0.0% non-contiguous), 82/2299
blocks
executed '/sbin/e2fsck' done
executed '/sbin/e2fsck' return 0
executing '/usr/sbin/e2fsck'
e2fsck 1.43.9 (8-Feb-2018)
Pass 1: Checking inodes, blocks, and sizes
Pass 2: Checking directory structure
Pass 3: Checking directory connectivity
Pass 4: Checking reference counts
Pass 5: Checking group summary information
/dev/block/by-name/oem: 18/2448 files (0.0% non-contiguous), 513/16384
blocks
executed '/usr/sbin/e2fsck' done
executed '/usr/sbin/e2fsck' return 1
executing '/usr/sbin/resize2fs'
resize2fs 1.43.9 (8-Feb-2018)
The filesystem is already 16384 (1k) blocks long. Nothing to do!
executed '/usr/sbin/resize2fs' done
executed '/usr/sbin/resize2fs' return 0
```
#### 4.2.2 恢复出厂设置

 命令行运行update 程序，设备会进入recovery，并进行格式化，格式化完成之后会自动进入 normal 系统。
``` bash
update （或 update reset）
```
 串口log打印如下内容：
 ```bash
 I:Boot command: boot-recovery
I:Got arguments from boot message
Command: "recovery" "--wipe_data"
format '/dev/block/by-name/userdata' to ext2 filesystem
executing '/sbin/mke2fs'
[ 4.692437] vendor storage:20160801 ret = -1
[ 6.030842] phy phy-ff008000.syscon:usb2-phy@100.0: charger =
USB_SDP_CHARGER
[ 10.891460] random: nonblocking pool is initialized
 ```

#### 4.2.3 升级

 执行update ota /xxx/update.img ，设备会进入 recovery，并进行升级。
```bash
update ota /udisk/update.img
```
 以从 U 盘升级为例，串口可能打印的 log 如下：
```bash
I:Boot command: boot-recovery
I:Got arguments from boot message
Command: "recovery" "--update_package=/udisk/update.img"
。。。。
librkupdate_ui_print = parameter writing....
########### RKA_Gpt_Download #########
librkupdate_###### Download trust ... #######
```
### 4.3 常见问题汇总

 #### 4.3.1  "cannot find/open a drm device "

 常见在非 RK3308 平台，进入 recovery 模式后串口打印如下 log：
 ```bash
 we are in recovery, skip init oem/userdata
start debug recovery...
Starting recovery on Fri Jan 18 09:19:51 2013
failed to read font: res=-1, fall back to the compiled-in font
Starting network: cannot find/open a drm device: No such file or directory
 ```

 遇到此情况时，解决方法是：接上设备支持的显示屏，或者 HDMI 设备。

 原因分析：从提示的 log 看是找不到或者打开drm 设备失败。因为，默认非
 RK3308 平台 recovery程序的编译是打开支持 UI 显示的，如果进入 recovery
 模式之后，打开显示设备失败，则会导致 recovery执行失败。

 解决方式：
1 `source envsetup.sh`

 2、现在使用平台的recovery配置编号，回车

 3、 `make menuconfig `，打开`No UI for recovery` 的配置
 ```bash
 > Target packages --->
     [*] Rockchip BSP packages --->
     [*] Rockchip recovery for linux
     [*] No UI for recovery
     [ ] Linux AB bool control
          Linux A/B bringup features. (successful_boot) --->
          choice the update bin of recovery. (rkupdate) --->
     -*- recovery bin
     [ ] updateEngine bin
 ```

`external/recovery/Makefile` 中就不会编译与显示相关的代码。

 ![](Rockchip_Developer_Guide_Linux_Recovery_CN_pic/media/image9.jpeg)
 4、重新编译 recovery包
```bash
make recovery-dirclean && make recovery
```
 5、重新生成 recovery 固件
```bash
./build.sh recovery
```
 6、生成固件。
 ```bash
 ./mkfirmware.sh
 ```

#### 4.3.2  **misc** 分区固件修改默认命令

 如果想修改 misc 固件中打包不同的 recovery 命令，或者使用空白的 misc
 分区固件。可按如下方式修改：

 工程根目录下：修改 mkfirmware.sh。

 ![](Rockchip_Developer_Guide_Linux_Recovery_CN_pic/media/image10.jpeg)
#### 4.3.2 **userdata** 分区设置为 **vfat** 文件系统

 SDK 中默认 userdata 分区为 ext2/ext4 文件系统，若想修改为 vfat32
 文件系统，可按如下修改：

1.  修改
`board/rockchip/rkxxxx/fs-overlay-recovery/etc/fstab`
 修改前：
 ```bash
/dev/block/by-name/userdata /userdata ext2 defaults0
 ```

 修改后：
```bash
/dev/block/by-name/userdata /userdata vfat defaults0 0
```
2.  修改`configs/rockchip_rkxxxx_release_defconfig`

 增加以下配置：
 ```bash
BR2_PACKAGE_DOSFSTOOLS=y
BR2_PACKAGE_DOSFSTOOLS_FATLABEL=y
BR2_PACKAGE_DOSFSTOOLS_FSCK_FAT=y
BR2_PACKAGE_DOSFSTOOLS_MKFS_FAT=y
 ```

3.  修改`package/rockchip/usbdevice/S50usbdevice`
```bash
start)
mkdir /dev/usb-ffs -m 0770
mkdir /dev/usb-ffs/adb -m 0770
mount -t configfs none /sys/kernel/config
mkdir /sys/kernel/config/usb_gadget/rockchip -m 0770
echo 0x2207 > /sys/kernel/config/usb_gadget/rockchip/idVendor
echo "ums_adb" >
/sys/kernel/config/usb_gadget/rockchip/configs/b.1/strings/0x409/configu
ration
mount -t functionfs adb /dev/usb-ffs/adb
mount -t vfat /dev/disk/by-partlabel/userdata /media/usb0
export service_adb_tcp_port=5555
adbd &
sleep 1
```
4.  确保已更新以下补丁

 0001-common-mk-userdata-Fix-wrong-FS\_TYPE-check.patch
```bash
case $FS_TYPE in
ext[2-4])
$COMMON_DIR/mke2img.sh $USERDATA_DIR $USERDATA_IMG
;;
fat|vfat)
SIZE=$(du -h -BM --max-depth=1 $USERDATA_DIR|awk '{print int($1)}')
# echo "create image size=${SIZE}M"
dd if=/dev/zero of=$USERDATA_IMG bs=1M count=$SIZE >/dev/null 2>&1
mkfs.vfat $USERDATA_IMG >/dev/null 2>&1
mcopy -i $USERDATA_IMG $USERDATA_DIR/* ::/ >/dev/null 2>&1
;;
*)
echo "file system: $FS_TYPE not support."
exit 1
;;
Esac
```
5.  修改`common/mk-userdata.sh`

6.  修改 rk3308/BoardConfig.mk

 ~~export RK\_USERDATA\_FS\_TYPE=ext2~~
```bash
# Set userdata partition type, including ext2, fat
export RK_USERDATA_FS_TYPE=vfat
```
#### 4.3.4 **userdata** （或**/data** ）分区不格式化
BoardConfig.mk 中配置了` wipe_all-misc.img `，却不希望格式化用户或客制（userdata 或 oem）分区，
此时需要修改 recovery 的代码。修改` external/recovery/reocvery.c` ： main 函数中如下图的代码，
将下图红框中的代码注释掉后，重新编译 recovery 分区固件，烧写 recovery 分区固件即可。

 ![](Rockchip_Developer_Guide_Linux_Recovery_CN_pic/media/image11.jpeg)

#### 4.3.4 **SD**卡升级问题

 在实际项目开发中，经常遇到使用 SD 卡制作启动盘，用以升级裸片或者升级Flash固件。在第3章节，我
们阐述了SD 卡制作启动盘并可以正常进入 recovery 模式，进行升级的情况，但实际使用过程中，常遇到
SD 卡升级无法正常进行，串口亦无任何输出的情况。本小节就此情景下做针对性的说明。
此处，以 RK1808 平台为例，其他 RK 平台芯片（RK3288、RK3399、RK3399PRO）类似，给出SD卡 管
脚与 UART 2 调试串口 IO复用后，SD卡作为启动卡升级的解决方案。

1.  首先检查硬件原路图，查看 SD 卡 GPIO 管脚是否与 uart2
     串口管脚复用，若硬件有复用，需调整uboot 下的dtsi，打开使能
     sdmmc，禁用 uart2 (系统默认使用uart 2
     作为调试串口)。若无复用，检查SD 卡上电与初始化部分。

2.  修改 loader，将 loader 中 uart 的打印重新配置，修改
     SDK/rkbin/tools/ddrbin\_param.txt 中 uart id
     。假如可以将串口飞线连接到 uart1 m0，则 uart id=1；如果飞到 uart1
     m1，那么 uart id=1 uart iomux=1。

3.  重新生成 ddr.bin，执行以下命令
```bash
cd SDK/rkbin/tools
rkbin/tools$./ddrbin_tool ddrbin_param.txt
../bin/rk1x/rk1808_ddr_933MHz_v1.04.bin
1
```
 此处 rk1808\_ddr\_933MHz\_v1.04.bin 文件，根据 SDK 中当前
 rkbin/bin/rk1x/ 目录下的文件名保持一致。

 具体平台目录有差异，根据实际芯片平台的前两个数字命名。

 ddrbin\_tool工具参数详细内容，可参考说明文档：
```bash
SDK/rkbin/tools/ddrbin_tool_user_guide.txt 
```
4.  修改 kernel dts配置。
修改调试串口，除了 ddr.bin
 修改外，内核也需要修改。

 ![](Rockchip_Developer_Guide_Linux_Recovery_CN_pic/media/image12.png)

5 修改启动参数 cmdline：
`kernel/arch/arm64/boot/dts/rockchip/rk1808-evb-v10.dts`
```bash
chosen {
bootargs = "earlycon=uart8250,mmio32,0xff550000 console=ttyFIQ0
root=PARTUUID=614e0000-0000 rootfstype=ext4 rootwait swiotlb=1 kpti=0
snd_aloop.index=7";
};
```
 此处 0xff550000 这个地址要根据实际的串口修改，各个不同串口地址在`arch/arm64/boot/dts/rockchip/rk1808.dtsi`这个文件里可以搜索找到，其他平台类似，查找对应平台的设备树文件。

 如：RK1808 平台 uart2: serial\@ff550000， uart1: serial\@ff540000。

 ![](Rockchip_Developer_Guide_Linux_Recovery_CN_pic/media/image13.jpeg)
6 编译固件

 uboot编译： ./build.sh uboot
 或者进入u-boot目录中，执行编译后生成文件在 u-boot 目录下：
```bash
u-boot/
├── rk1808_loader_v1.03.104.bin
├── trust.img
└── uboot.img
```
 kernel编译：`./build.sh kernel`
  recovery编译：`./build.sh recovery`和`/build.sh updateimg`

   7 正确烧录编译好的固件以后

 打包生成 update.img 升级包， 使用"SDDiskTool\_v1.62"或更新版本，烧录
 update.img 到SD卡中。

 开发板断电，
 插上SD卡，上电。此时串口可以从uart1或其他当前所指定的飞线的串口打印log，观察log，并根据log具体分析SD卡升级问题。

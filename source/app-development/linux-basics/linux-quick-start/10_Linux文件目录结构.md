# 10. Linux文件目录结构

## 10.1 前言
Linux文件系统采用层级树状结构，所有资源（包括硬件设备、进程信息）都表现为文件。与Windows的主要差异：
- **无盘符概念**：所有存储设备挂载到统一目录树
- **严格区分大小写**：`File.txt`与`file.txt`是两个不同文件
- **隐藏文件机制**：以`.`开头的文件/目录默认不可见

---

## 10.2 Linux文件目录结构

### 10.2.1 根目录
- **路径表示**：`/`
- **核心特性**：
  - 所有目录的起点
  - 必须包含系统启动所需的最小文件集合
  - 挂载点：外部存储设备通过挂载接入目录树

### 10.2.2 根目录（/）核心目录一览表

| 目录         | 用途描述                                                                 | 重要文件/子目录示例                           | 管理命令/操作                         | 注意事项                     |
|--------------|--------------------------------------------------------------------------|-----------------------------------------------|----------------------------------------|------------------------------|
| ​**/bin**​     | 基础用户命令（所有用户可用）                                             | `ls`, `cp`, `bash`, `grep`                    | `which ls` 查看命令路径                | 与/usr/bin合并趋势（某些发行版）|
| ​**/boot**​    | 启动加载文件与内核                                                       | `vmlinuz-5.15.0`, `initrd.img`                | `update-grub` 更新启动配置              | 勿随意删除内核文件            |
| ​**/dev**​     | 设备文件（物理/虚拟设备）                                                | `sda`（磁盘）, `ttyS0`（串口）, `null`        | `mknod` 创建设备文件                   | 大多数文件由内核自动生成       |
| ​**/etc**​     | 系统全局配置文件                                                         | `passwd`, `fstab`, `network/interfaces`        | `nano /etc/ssh/sshd_config`            | 修改前务必备份                |
| ​**/home**​    | 普通用户主目录                                                           | `user1/Downloads`, `user2/.bashrc`            | `useradd -m username` 创建用户          | 权限隔离重要区域               |
| ​**/lib**​     | 系统级共享库与内核模块                                                   | `libc.so.6`, `/modules/`                       | `ldconfig` 更新库缓存                  | 32位系统使用，64位系统用/lib64 |
| ​**/media**​   | 可移动设备自动挂载点                                                     | `USB_Drive/`, `CDROM/`                         | `udisksctl mount -b /dev/sdb1`         | 现代系统多用/run/media         |
| ​**/mnt**​     | 临时手动挂载点                                                           | `nas/`, `backup_disk/`                         | `mount /dev/sdb1 /mnt/backup`          | 建议创建子目录管理             |
| ​**/opt**​     | 第三方商业软件安装目录                                                   | `google/chrome`, `matlab/`                     | 需手动配置环境变量                     | 遵循软件包规范安装             |
| ​**/proc**​    | 进程与系统信息虚拟文件系统                                               | `cpuinfo`, `1/status`（PID1进程）              | `cat /proc/meminfo` 查看内存详情       | 数据实时生成勿直接修改          |
| ​**/root**​    | 超级用户主目录                                                           | `.ssh/`, `.bash_history`                        | `sudo -i` 进入root环境                 | 普通用户无访问权限             |
| ​**/run**​     | 运行时可变数据（系统启动后生成）                                         | `sshd.pid`, `user/1000/`                        | `systemctl status` 查看服务状态         | 重启后数据丢失                 |
| ​**/sbin**​    | 系统管理命令（需root权限）                                               | `fdisk`, `iptables`, `reboot`                   | `sudo sbin/command` 执行管理操作        | 普通用户无权执行               |
| ​**/srv**​     | 服务相关数据（网站/FTP等）                                               | `www/`, `git/`                                  | 需手动配置服务指向                     | 实际使用中较少强制规范          |
| ​**/sys**​     | 内核与硬件配置接口                                                       | `class/net/eth0`, `devices/system/cpu/`         | `echo 1 > /sys/class/leds/input::capslock/brightness` 控制键盘灯 | 修改可能影响硬件状态           |
| ​**/tmp**​     | 临时文件（所有用户可写）                                                 | `chrome_1234/`, `installer.sh`                 | `mktemp` 创建临时文件                   | 默认10天自动清理（systemd）     |
| ​**/usr**​     | 用户程序与只读数据（Unix System Resources）                              | `bin/`, `local/`, `share/man/`                  | `make install` 默认安装位置             | 系统升级时保留                 |
| ​**/var**​     | 可变数据文件（日志/缓存等）                                              | `log/`, `cache/apt/`, `lib/mysql/`             | `journalctl -u service` 查看服务日志   | 需要定期清理旧数据             |
| ​**/lost+found**​ | 文件系统修复后恢复的文件                                               | `#12345`, `#67890`（inode编号）                | `fsck` 磁盘检查后生成                   | 仅ext3/4文件系统可见           |
| ​**/selinux**​ | SELinux安全策略配置（仅支持SELinux的系统）                              | `config`, `policy/`                            | `sestatus` 查看状态                    | 禁用后此目录可能为空            |

### 10.2.3 Linux与Windows主要目录对比
| 目录      | 用途                                | 典型内容示例                | Windows近似对应       |
|-----------|-----------------------------------|---------------------------|----------------------|
| **/bin**  | 基础命令程序                       | `ls`, `cp`, `bash`        | C:\Windows\System32  |
| **/etc**  | 系统配置文件                       | `passwd`, `network/`      | C:\ProgramData       |
| **/home** | 用户主目录                         | `user1/`, `user2/`        | C:\Users             |
| **/root** | 超级用户的主目录                   | `.bashrc`, `.ssh/`        | (无直接对应)          |
| **/dev**  | 设备文件                           | `sda`, `ttyS0`            | 设备管理器            |
| **/proc** | 进程与内核信息                     | `1/status`, `meminfo`     | 任务管理器            |

### 10.2.4 用户目录结构
| 用户类型   | 主目录路径      | 默认包含内容                |
|------------|----------------|---------------------------|
| root用户   | `/root`        | 系统级配置文件/SSH密钥     |
| 普通用户   | `/home/用户名` | 桌面/文档/下载等个人文件夹  |

---

## 详细目录解析

### /bin 与 /sbin
- **/bin**：所有用户可用的基础命令  
  ```bash
  $ ls /bin | head -5
  bash   cat   chmod   cp   date
  ```
- **/sbin**：系统管理员专用的维护命令  
  ```bash
  $ ls /sbin | grep 'fdisk'
  fdisk
  ```

### /boot
- 包含启动加载器与内核文件  
  ```bash
  $ ls /boot
  initramfs-5.15.0-78-generic  vmlinuz-5.15.0-78-generic
  ```

### /dev
- 设备文件示例：
  - `/dev/sda`：第一块SATA硬盘
  - `/dev/ttyUSB0`：第一个USB串口设备
  - `/dev/null`：数据黑洞设备

### /etc
- 重要配置文件：
  ```bash
  /etc/passwd    # 用户账户信息
  /etc/fstab     # 磁盘挂载配置
  /etc/ssh/      # SSH服务配置目录
  ```

### /proc
- 查看CPU信息：
  ```bash
  cat /proc/cpuinfo | grep 'model name'
  ```
- 查看内存使用：
  ```bash
  free -h
  ```

### /var
- 动态数据存储：
  - `/var/log`：系统日志
  - `/var/www`：Web服务器默认目录
  - `/var/lib/mysql`：MySQL数据库文件

### /usr
- 用户程序与资源：
  - `/usr/bin`：用户级应用程序
  - `/usr/lib`：共享库文件
  - `/usr/local`：手动安装的软件

---

## 10.3 总结
### Linux vs Windows目录差异
| 特性            | Linux                  | Windows               |
|-----------------|------------------------|-----------------------|
| 根目录          | `/`                    | `C:\`, `D:\`等盘符     |
| 配置文件位置    | 集中在/etc             | 分散在注册表/各程序目录|
| 用户数据        | /home/用户名           | C:\Users\用户名        |

### 学习建议
1. 使用`tree -L 1 /`快速查看根目录结构
2. 通过`man hier`查看官方目录说明
3. 修改系统文件前备份（建议使用`cp file file.bak`）
4. 避免直接操作`/proc`与`/sys`中的虚拟文件

附：目录结构速查命令
```bash
# 查看目录占用空间
du -sh /*
# 查找文件路径
find / -name "*.conf" 2>/dev/null
```

**文档版本控制**  
`Rev 1.0.0 | 最后更新：2025-02-26 | 适用硬件版本：RK平台系列产品`

**版权声明**  
© 2025 福州牛新牛科技有限公司. 保留所有权利。
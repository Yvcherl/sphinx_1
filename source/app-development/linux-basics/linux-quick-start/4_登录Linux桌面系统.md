# 4. 登录Linux桌面系统

## 4.1 前言
本章以**Ubuntu 22.04 LTS**为例，系统讲解Linux桌面环境的核心操作流程，涵盖从开机到关机全生命周期的关键操作场景。

---

## 4.2 开机
### 硬件启动阶段
1. **BIOS/UEFI初始化**：完成硬件自检（POST）
2. **引导加载程序**：GRUB2加载内核（默认等待3秒）
3. **内核启动**：加载驱动并挂载根文件系统
4. **系统服务启动**：systemd并行启动基础服务（SSH/NetworkManager等）

### 用户可见阶段
- 显示主板LOGO（部分设备支持自定义）
- 出现Ubuntu启动动画（ Plymouth 图形界面）
- 进入登录界面（GDM显示管理器）

---

## 4.3 登录桌面系统

### 4.3.1 图形界面登录
**操作步骤**：
1. 选择用户账户（支持头像点击）
2. 输入密码（支持键盘布局切换）
3. 选择桌面会话类型：
   ```markdown
   - Ubuntu (默认使用Wayland协议)
   - Ubuntu on Xorg (传统X11协议)
   - 故障安全模式（1024x768分辨率）
   ```
4. 点击"Sign In"按钮（或按Enter键）

**技术特性**：
- 密码错误3次触发PAM延时策略
- 自动挂载用户主目录（/home/<user>）
- 加载用户级systemd服务（~/.config/systemd/user）

### 4.3.2 命令行登录
**进入控制台**：
- 快捷键：`Ctrl + Alt + F2` ~ `F6`
- 显示`Ubuntu 22.04 LTS tty2`终端提示符

**登录流程**：
```bash
# 输入用户名（root用户需先配置sudo权限）
ubuntu login: your_username
Password: ********

# 登录成功提示
Welcome to Ubuntu 22.04 LTS (GNU/Linux 5.15.0-76-generic x86_64)
Last login: Mon Aug 14 09:32:21 CST 2023 on tty2
```

---

## 4.4 退出登录

### 4.4.1 图形界面退出
**操作路径**：
1. 点击右上角系统菜单
2. 选择用户头像 → "Log Out"
3. 确认返回登录界面

**后台行为**：
- 终止用户进程（保留系统服务）
- 卸载用户文件系统
- 清理/tmp临时文件

### 4.4.2 命令行退出
```bash
# 普通用户退出
$ exit

# 结束指定用户会话
$ loginctl terminate-user <username>
```

---

## 4.5 关机重启

### 4.5.1 图形界面操作
**标准流程**：
1. 系统菜单 → Power Off / Restart
2. 60秒等待确认（强制关机会导致数据丢失警告）

**高级选项**：
- 休眠模式（需要swap分区≥内存大小）
- 切换用户（保持当前会话后台运行）

### 4.5.2 命令行操作
```bash
# 立即关机（需sudo权限）
$ sudo shutdown -h now

# 定时重启（10分钟后）
$ sudo shutdown -r +10 "System upgrade required"

# 取消关机计划
$ sudo shutdown -c
```

**systemctl命令**：
```bash
# 现代系统推荐方式
$ systemctl poweroff
$ systemctl reboot
```

---

## 4.6 总结
### 操作对比表
| 操作类型        | 图形界面耗时 | 命令行耗时 | 适用场景               |
|----------------|-------------|-----------|-----------------------|
| 登录            | 3-8秒       | 1-2秒     | 日常使用/故障排查       |
| 退出            | 2-5秒       | <1秒      | 多用户切换             |
| 关机            | 10-15秒     | 5-8秒     | 系统维护               |

### 最佳实践
1. 生产环境优先使用`systemctl`命令
2. 避免直接按电源键强制关机（可能损坏ext4/btrfs文件系统）
3. 多用户系统使用`who`命令检查活跃会话
4. 配置自动锁屏：`Settings → Privacy → Screen Lock`
```bash
# 命令行配置锁屏超时（300秒）
gsettings set org.gnome.desktop.session idle-delay 300
```

附：Ubuntu登录界面故障恢复方法
```bash
# 重置显示管理器
sudo systemctl restart gdm
```

**文档版本控制**  
`Rev 1.0.0 | 最后更新：2025-02-26 | 适用硬件版本：RK平台系列产品`

**版权声明**  
© 2025 福州牛新牛科技有限公司. 保留所有权利。
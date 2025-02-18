**Rockchip Repo** 镜像服务器部署指南
------------------------------------------------

**前⾔概述**

本⽂介绍了如何搭建 Gitolite 服务器，并⽤于 SDK
的管理，旨在帮助客⼾完善对 SDK 代码的管理与维护。
产品版本

[TOC]

## 1.  搭建 Gitolite 服务器
- 创建 Gitolite 账⼾
```bash
sudo adduser git
sudo usermod -G sudo -a git
```
- 下载、安装 Gitolite
```bash
su git
git clone https://github.com/sitaramc/gitolite
mkdir $HOME/bin
./gitolite/install -to $HOME/bin
```
- 添加管理员权限

    git ⽤⼾的 `~/.ssh` ⽬录下应该有两个密钥：
    - RK 密钥：⽤于从 RK 服务器同步代码

    - Gitolite 密钥：⽤于 Gitolite 代码权限管理

    公钥的名称建议为 $username.pub 的形式，⽅便后续权限添加管理。
```bash
./bin/gitolite setup -pk ~/.ssh/$username.pub
```
## 2.  同步 RK 服务器仓库

### 2.1.  RK Gitolite 服务器代码同步
以下以 `rk3326_linux5.10_release.xml` 为例，说明如何同步代码。
```bash
# 代码同步应该在 repositories 下进行
cd repositories
# 同步 rk3326_linux5.10_release.xml SDK
repo init --mirror --repo-url ssh://git@www.rockchip.com.cn/repo/rk/tools/repo \
-u ssh://git@www.rockchip.com.cn/linux/rockchip/platform/manifests \
-b linux -m rk3326_linux5.10_release.xml
# 进行代码同步
.repo/repo/repo sync -c
# 生成 SDK project 列表，后续添加权限管理需要
.repo/repo/repo list -n > project.list
```
### 2.2.  RK Gerrit 服务器代码同步
以下以 `rk3562_linux_release.xml` 为例，说明如何同步代码。
```bash
# 代码同步应该在 repositories 下进行
cd repositories
# 同步 rk3562_linux_release.xml SDK
repo init --mirror --repo-url https://gerrit.rock-chips.com:8443/repo-release/tools/repo \
-u https://gerrit.rock-chips.com:8443/linux/rockchip/platform/manifests \
-b rk3562 -m rk3562_linux_release.xml
# 进行代码同步
.repo/repo/repo sync -c
# 生成 SDK project 列表，后续添加权限管理需要
.repo/repo/repo list -n > project.list
```

## 3.  Gitolite 权限管理
Gitolite服务器通过gitolite - admin仓库管理权限，管理员用户可以通过`ssh://git@$HostIP/gitolite - admin`下载该仓库，其中$HostIP为Gitolite服务器的IP。该仓库的文件结构如下:

```bash
├── conf
│ └── gitolite.conf # 记录仓库、用户权限的配置文件
└── keydir # 需要开通权限的公钥，都需要添加到该路径
├── git.pub # git 用户的公钥
└── test.pub # test 用户的公钥
```
添加RK仓库列表到Gitolite中，同时添加group1、group2以及用户git和test。

```bash
```bash
# 预处理 project.list，并添加到 gitolite.conf
sed -i's/^/@linux = \&/g' project.list
echo "" >>./conf/gitolite.conf
cat project.list >>./conf/gitolite.conf
echo "" >>./conf/gitolite.conf

# gitolite.conf 文件添加以下内容
@group1 = git
@group2 = test

repo @linux
    RW+ = @group1
    RW  = @group2
    R   = @all
```
## 4.  镜像服务器代码下载
完成以上步骤后，就可以通过 Gitolite 服务器进行 SDK 的下载。需要注意的是，下载的仓库地址需要根据 Gitolite 服务器进行修改，通常 repositories 目录是所有仓库的根目录，如 rk3326_linux5.10_release.xml SDK，可以通过以下地址进行下载:
```bash
repo init --repo-url ssh://git@$HostIP/repo \
-u ssh://git@$HostIP/rockchip/platform/manifests \
-b linux -m rk3326_linux5.10_release.xml
```
## 5.  FAQ

### 5.1.  repo sync 时反复要求输⼊密码
这种情况只有在从 Gerrit 服务器同步代码时才会出现，可以设置` git config --global
credential.helper store` 开启⾃动输⼊密码。
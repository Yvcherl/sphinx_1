# Can 开发⽂档

| 芯片名称 | 内核版本 |
|--|--|
| RV1126 | 4.4 & 4.19 |
| RK3568 | 4.19 & 5.10 |
| RK3588 | 5.10 |

 读者对象

 本⽂档（本指南）主要适⽤于以下⼯程师：技术⽀持⼯程师,软件开发⼯程师


##   **CAN** 驱动

### 1.1  驱动⽂件


 驱动⽂件所在位置：

 RV1126/RV1109使⽤：
`drivers/net/can/rockchip/rockchip_can.c`
 RK3568/RK3588使⽤:
`drivers/net/can/rockchip/rockchip_canfd.c`

### 1.2**DTS** 节点配置

 主要参数:
 `interrupts = <GIC_SPI 100 IRQ_TYPE_LEVEL_HIGH>;`

 转换完成，产⽣中断信号。
 `clock`
 ```bash
 assigned-clocks = <&cru CLK_CAN>;
assigned-clock-rates = <200000000>;
clocks = <&cru CLK_CAN>, <&cru PCLK_CAN>;
clock-names = "baudclk", "apb_pclk";
 ```

 时钟频率可以修改，如果CAN的⽐特率1M建议修改CAN时钟到300M，信号更稳定。低于1M⽐特率的，时钟设置200M就可以。CAN时钟最好设置成⽐特率的偶数倍，便于分出精准的⽐特率频率。
`compatible`
```bash
.compatible = "rockchip,can-1.0",
```
 RV1126/RV1109使⽤\"rockchip,can-1.0\"。
 RK3568使⽤\"rockchip,rk3568-can-2.0\"。
 RK3588使⽤\"rockchip,can-2.0\"。

 配置can\_h和can\_l的iomux作为can功能使⽤。

### 1.3 内核配置
```bash
Symbol: CAN_ROCKCHIP [=y]
|
| Type : tristate
|
| Prompt: Rockchip CAN controller
|
| Location:
|
| -> Networking support (NET [=y])
|
| -> CAN bus subsystem support (CAN [=y])
|
| -> CAN Device Drivers
|
| -> Platform CAN drivers with Netlink support (CAN_DEV [=y])
|
| Defined at drivers/net/can/rockchip/Kconfig:1
|
| Depends on: NET [=y] && CAN [=y] && CAN_DEV [=y] && ARCH_ROCKCHIP [=y]
```
```bash
Symbol: CANFD_ROCKCHIP [=y]
|
| Type : tristate
|
| Prompt: Rockchip CANFD controller
|
| Location:
|
| -> Networking support (NET [=y])
|
| -> CAN bus subsystem support (CAN [=y])
|
| -> CAN Device Drivers
|
| -> Platform CAN drivers with Netlink support (CAN_DEV [=y])
|
| Defined at drivers/net/can/rockchip/Kconfig:10
|
| Depends on: NET [=y] && CAN [=y] && CAN_DEV [=y] && ARCH_ROCKCHIP [=y]
```

## 2 .**CAN** 通信测试⼯具

 canutils是常⽤的CAN通信测试⼯具包，内含5个独⽴的程序：canconfig、candump、canecho、cansend、cansequence。这⼏个程序的功能简述如下：
`canconfig`
 ⽤于配置 CAN 总线接口的参数，主要是波特率和模式。
`candump`
 从 CAN 总线接口接收数据并以⼗六进制形式打印到标准输出，也可以输出到指定⽂件。
 `canecho`
 把从 CAN 总线接口接收到的所有数据重新发送到 CAN 总线接口。
`cansend`
 往指定的 CAN 总线接口发送指定的数据。
`cansequence`
 往指定的 CAN总线接口⾃动重复递增数字，也可以指定接收模式并校验检查接收的递增数字。
`ip`
 CAN波特率、功能等配置。

 注意：busybox⾥也有集成了ip⼯具，但busybox⾥的是阉割版本。不⽀持CAN的操作。故使⽤前请先确定ip命令的版本（iproute2）。

 上⾯⼯具包，⽹络上都有详细的编译说明。如果是⾃⼰编译buildroot，直接开启宏就可以⽀持上述⼯具包。也可以联系我们获取。
 ```bash
 BR2_PACKAGE_CAN_UTILS=y
BR2_PACKAGE_IPROUTE2=y
 ```

## 3 **CAN** 常⽤命令接口


1. 查询当前⽹络设备:
`ifconfig -a`
2. CAN启动:
关闭CAN:
`ip link set can0 down`
设置⽐特率500KHz:
`ip link set can0 type can bitrate 500000`
打印can0信息:
`ip -details -statistics link show can0`
启动CAN:
`ip link set can0 up`

3. CAN发送:
发送（标准帧,数据帧,ID:123,date:DEADBEEF）:
`cansend can0 123#DEADBEEF`
发送（标准帧,远程帧,ID:123）:
`cansend can0 123#R`

发送（扩展帧,数据帧,ID:00000123,date:DEADBEEF）:
`cansend can0 00000123#12345678`
发送（扩展帧,远程帧,ID:00000123）:
`cansend can0 00000123#R`
3. CAN接收:
开启打印，等待接收:
`candump can0`

  ## 4. CAN常见问题排查

### 4.1 无法收发

回环模式测试:

启动can后，io输入命令开启回环自测（基地址根据实际dts启动的can配置）:

`io -4 0xfe580000 0x8415`

回环模式下，cansend后candump可以接收，说明控制器工作正常。这种状态下，只要检查: IOMUX是否正确；硬件连接是否正确；终端120欧姆电阻有没有接入；转换芯片是否正常。

### 4.2 概率性不能收发

先确认比特率是否是精准的，下面命令可以看到can当前的实际比特率以及配置信息。如果比特率偏差会造成收发异常，需要根据比特率调整输入时钟，以分到精准的比特率。

`ip -details -statistics link show can0`

采样点调整，上面can命令会打印当前配置的采样点，尽量保证同网络中采样点一致。可以保障收发的稳定性。

## 5. CAN比特率和采样点计算

目前CAN架构根据输入频率和比特率自动计算。采样点的规则按照CiA标准协议：

```c
/* Use CiA recommended sample points */
    if (bt->sample_point) {
        sample_point_nominal = bt->sample_point;
    } else {
        if (bt->bitrate > 800000)
            sample_point_nominal = 750;
        else if (bt->bitrate > 500000)
            sample_point_nominal = 800;
        else
            sample_point_nominal = 875;
    }
  ```  

比特率计算公式（详细原理可以百度，这里只介绍芯片配置相关）:
`BitRate = clk_can / (2 *(brq + 1) / ((tseg2 + 1) + (tseg1 + 1) + 1))`
`Sample = (1 + (tseg1 + 1)) / (1 + (tseg1 + 1) + (tseg2 + 1))`
brq、tseg1、tseg2 见 CAN 的 TRM 中 BITTIMING 寄存器。

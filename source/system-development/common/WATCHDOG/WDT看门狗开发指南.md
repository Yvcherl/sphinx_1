# WATCHDOG

本文主要介绍Rockchip Linux 平台WATCHDOG开门狗功能的配置及使用。

---

## 1、概述
**功能**：WDT是一种硬件机制，用于在软件运行异常时自动重启系统，当WDT计数器减至0时，触发系统复位，防止软件错误导致的系统卡死。

**支持芯片**：RK356X、RK3588等Rockchip系列芯片。

**内核版本**：Linux 4.4/4.19/5.10。

---

## 2、驱动配置
### 2.1. **驱动文件**  
驱动文件路径：`drivers/watchdog/dw_wdt.c`

### 2.2. **DTS节点配置**  

**DTS 配置参考⽂档路径**：

```
Documentation/devicetree/bindings/watchdog/dw_wdt.txt (Linux内核文档)
```

**关键参数**：

- `interrupts`：中断模式时先触发中断，超时后复位
```
interrupts = <GIC_SPI 120 IRQ_TYPE_LEVEL_HIGH 0>;
```
  
- `clocks`：WDT工作时钟源，用于计算计数周期
```
clocks = <&cru PCLK_WDT>;
```

---

## 3、WDT使用
### 3.1. **操作接口**  
通过操作设备节点 `/dev/watchdog` 控制看门狗。 

**示例代码如下：**
   ```c
    int main(void) 
    {
        int fd = open("/dev/watchdog", O_WRONLY); //通过open来启动watchdog
        int ret = 0;
        if (fd == -1) {
            perror("watchdog");
            exit(EXIT_FAILURE);
        }
        while (1) {
            ret = write(fd, "\0", 1); //通过write来喂狗
            if (ret != 1) {
                ret = -1;
                break;
            }
            sleep(10);
        }
        close(fd);
        return ret;
    }
  ```

### 3.2. **关键行为**  
   - **正常关闭**（未写入'V'，例如`echo A > /dev/watchdog`）：停止喂狗，触发复位。
   - **安全关闭**（写入'V'后关闭，例如先`write(fd, "V", 1)`或者`echo A > /dev/watchdog`，然后`close()`）：内核继续喂狗，系统不重启。
   - **强制复位**：配置 `CONFIG_WATCHDOG_NOWAYOUT` 后，即使写入'V'仍会复位。

---

## 4、内核配置

**启用选项：**`CONFIG_WATCHDOG=y`（位于 `Device Drivers → Watchdog Timer Support`）。

**配置示例：**
```
Symbol: WATCHDOG [=y]
Type : boolean
Prompt: Watchdog Timer Support
    Location:
    (1) -> Device Drivers
    Defined at drivers/watchdog/Kconfig:6
```
---

## 5、常见问题
### 5.1. **WDT无法停止**  
旧版本需通过禁用时钟或软复位停止（需安全环境执行），新版支持寄存器停止。

### 5.2. **精度问题**  

仅有16档精度，相邻档位间隔大，因此无法精准计数。假设wdt clock为100MHz，最⼤超时时间 0x7fffffff / 100MHz = 21秒，如果需要更⼤的超时，需要调整对应的wdt clock 。
```
0000: 0x0000ffff
0001: 0x0001ffff
0010: 0x0003ffff
0011: 0x0007ffff
0100: 0x000fffff
0101: 0x001fffff
0110: 0x003fffff
0111: 0x007fffff
1000: 0x00ffffff
1001: 0x01ffffff
1010: 0x03ffffff
1011: 0x07ffffff
1100: 0x0fffffff
1101: 0x1fffffff
1110: 0x3fffffff
1111: 0x7fffffff
```

### 5.3. **RK356X暂停功能** 

使⽤Rockchip⾃带的io命令或者busybox的devmem命令可以实现暂停计数以及恢复计数。

**打开**
```
CONFIG_DEVMEM
```
**关闭**
```
CONFIG_STRICT_DEVMEM
```
0xfdc60504来⾃SYS_GRF的GRF_SOC_CON1寄存器，对bit4写1暂停计数，写0恢复计数，⾼16位为写使能位。

**暂停计数**

向寄存器 `0xfdc60504` 写入 `0x00100010` 

```
io -4 0xfdc60504 0x00100010
```

或者

```
busybox devmem 0xfdc60504 32 0x00100010
```


**恢复计数**

向寄存器 `0xfdc60504` 写入写入 `0x00100000`

```
io -4 0xfdc60504 0x00100000
```

或者

```
busybox devmem 0xfdc60504 32 0x00100000
```

**命令示例**
```bash
io -4 0xfdc60504 0x00100010    # 暂停
busybox devmem 0xfdc60504 32 0x00100000  # 恢复
```

### 5.4. **RK3588暂停功能**  
- **暂停计数**：向寄存器 `0xfd58c000` 写入 `0x00010001`。
- **恢复计数**：写入 `0x00100000`。
- 命令示例：
```bash
io -4 0xfd58c000 0x00010001    # 暂停
busybox devmem 0xfd58c000 32 0x00100000  # 恢复
```

---

## 6. 修订记录

初始版本：V1.0（2025-02-23）

作者：Nnewn

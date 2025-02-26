# SARADC

<a href="https://work.weixin.qq.com/kfid/kfc04b5ffb556109a43" style="text-decoration:none; 
display:inline-block; padding:8px 15px; background-color:#007bff; color:#fff; border-radius:5px;
" target="_blank">点击一下，立即进行微信沟通</a>

---

本文主要介绍了Rockchip平台下SARADC的相关开发信息，包括硬件规格、驱动文件位置与内核配置选项等。通过阅读本文，您可以了解如何在Rockchip平台上使用SARADC进行模拟信号的采集。

---

## 1. 硬件特性
- **SARADC 规格**  
  - 6 通道、10bit 有效位、1MSPS 转换速度（输入频率 13MHz 时）。
  - 参考电压 `vref-supply` 最大为 **1.8V**，ADC 值范围 **0-1024**（电压与ADC值成线性关系）。

---

## 2. 驱动文件与内核配置
**驱动文件位置**  
  `drivers/iio/adc/rockchip_saradc.c`
**内核配置选项**  
  ```bash
  Symbol: ROCKCHIP_SARADC [=y]
  Location: Device Drivers → Industrial I/O → Analog to digital converters
  ```
  - 依赖项：`IIO`、`ARCH_ROCKCHIP`、`RESET_CONTROLLER`。

**详细配置如下**
```bash
Symbol: ROCKCHIP_SARADC [=y]
Type  : tristate
Prompt: Rockchip SARADC driver
  Location:
    -> Device Drivers
      -> Industrial I/O support (IIO [=y])
（1）         -> Analog to digital converters
  Defined at drivers/iio/adc/Kconfig:319
  Depends on: IIO [=y] && (ARCH_ROCKCHIP [=y] || ARM && COMPILE_TEST [=n]) && RESET_CONTROLLER [=y]
```

---

## 3. DTS 节点配置
关键参数说明（DTS配置可参考 `Documentation/devicetree/bindings/iio/adc/rockchip-saradc.txt`），本文主要对如下参数进行说明：

- **`interrupts`**  
  转换完成中断信号，例如：`interrupts = <GIC_SPI 62 IRQ_TYPE_LEVEL_HIGH 0>;`。
- **`io-channel-cells`**  
  必须设为 `1`（遵循 IIO 绑定规范），例如`io-channel-cells = <1>;`。
- **`vref-supply`**  
  参考电压源，需根据硬件设计配置，例如`vref-supply = <&vccadc_ref>;`。

---

## 4. 驱动工作流程
- **初始化与注册**  
  - 通过 `rockchip_saradc_probe` 初始化 `struct iio_dev`，调用 `iio_device_register` 注册设备。
- **采样过程**  
  核心函数 `rockchip_saradc_read_raw`：
  1. **配置寄存器**  
     - 设置上电延时：`writel_relaxed(8, info->regs + SARADC_DLY_PU_SOC)`。
     - 启动采样：使能电源、选择通道、开启中断（`SARADC_CTRL_POWER_CTRL | SARADC_CTRL_IRQ_ENABLE`）。
  2. **等待中断**  
     `wait_for_completion_timeout` 等待转换完成。
  3. **读取数据**  
     中断处理函数 `rockchip_saradc_isr` 中读取 `SARADC_DATA` 寄存器值，保存至 `info->last_val`。
  4. **关闭 ADC**  
     清除中断并断电：`writel_relaxed(0, info->regs + SARADC_CTRL)`。
- **数据转换**  
  调用 `iio_convert_raw_to_processed_unlocked` 将原始 ADC 值转换为电压。

---

## 5. 使用示例（ADC-Key）
- **输入设备注册**  
  通过 `adc-keys.c` 初始化 `struct input_polled_dev`，调用 `input_register_polled_device`。
- **数据获取流程**  
  `adc_keys_poll` → `iio_read_channel_processed` → `rockchip_saradc_read_raw`。

---

## 6. 用户空间与内核接口
- **用户空间接口**  
  读取原始 ADC 值（通道号替换 `*`）：
  ```bash
  cat /sys/bus/iio/devices/iio:device0/in_voltage*_raw
  ```
  - 示例（通道0）：  
    `cat /sys/bus/iio/devices/iio:device0/in_voltage0_raw`

- **内核接口**  
  - 获取原始值：`iio_read_channel_raw()`  
  - 获取电压值：`iio_read_channel_processed()`

---

## 7. 注意事项
- **参考电压限制**：最大 1.8V，超压可能损坏硬件。
- **中断处理**：需及时清除中断并关闭 ADC 以降低功耗。
- **兼容性**：文档适用于 Rockchip 芯片（内核 4.4/4.19），其他版本需验证。

---

## 8. 修订记录

初始版本：V1.0（2025-02-23）

作者：Nnewn

# STM32超声波测距仪系统

基于 STM32F103C8 微控制器开发的超声波测距仪系统，支持 OLED 显示、串口通信、按键控制和 LED 报警功能。

## 功能特性

- **双超声波模块测距**：支持两个 HC-SR04 超声波传感器同时工作  
- **OLED 实时显示**：128×64 OLED 屏幕显示距离数据和系统状态  
- **串口通信**：通过 UART1 发送格式化的测距数据  
- **按键控制**：支持按键设置报警距离和开关报警功能  
- **LED 报警**：当检测距离小于设定值时自动报警  
- **开机动画**：友好的用户界面体验  

## 硬件要求

### 主控芯片
- STM32F103C8T6（ARM Cortex-M3，72 MHz，64 KB Flash，20 KB RAM）

### 外设模块
- HC-SR04 超声波测距模块 ×2  
- 0.96 寸 OLED 显示屏（I²C 接口）  
- LED 指示灯  
- 按键开关  
- 串口转 USB 模块（用于调试）

### 开发环境
- Keil MDK-ARM 5.x  
- STM32F1xx 标准外设库  

## 硬件连接

### 超声波模块 1（PB6/PB7）
<pre>
HC-SR04_1    STM32F103C8
VCC         3.3 V
GND         GND
Trig        PB6
Echo        PB7
</pre>

### 超声波模块 2（PA6/PA7）
<pre>
HC-SR04_2    STM32F103C8
VCC         3.3 V
GND         GND
Trig        PA6
Echo        PA7
</pre>

### OLED 显示屏（I²C）
<pre>
OLED        STM32F103C8
VCC         3.3 V
GND         GND
SCL         PB8
SDA         PB9
</pre>

### 其它外设
<pre>
LED         PB14
按键         PA0 PA1 PA2
UART1       PA9(TX)，PA10(RX)
</pre>

## 软件架构

### 主要模块
- **main.c/h**：主程序控制逻辑  
- **hc_sr04.c/h**：超声波测距驱动  
- **oled.c/h**：OLED 显示驱动  
- **display.c/h**：显示界面管理  
- **key.c/h**：按键处理  
- **led.c/h**：LED 控制  
- **usart.c/h**：串口通信  
- **delay.c/h**：延时函数  

### 系统流程
1. 系统初始化 → 外设配置 → 开机动画  
2. 主循环：测距 → 显示更新 → 串口输出 → 报警判断  
3. 按键中断：参数设置和功能切换  

## 编译和烧录

### 编译步骤
1. 打开 Keil MDK-ARM  
2. 加载项目文件 `Project.uvprojx`  
3. 选择目标设备：STM32F103C8  
4. 编译项目（F7）

### 烧录方法
1. 连接 ST-Link 调试器  
2. 在 Keil 中点击下载按钮  
3. 或使用 STM32CubeProgrammer  

## 使用方法

### 基本操作
1. 上电后系统自动启动，显示开机动画  
2. OLED 屏幕实时显示当前测距值  
3. 串口输出格式化的测距数据  
4. 按键可设置报警距离和开关报警功能  

### 串口数据格式
| Distance: 025 cm | Alarm: 020 cm | Status: ON |


### 按键功能
- **Key1**：切换报警开关  
- **Key2**：报警距离增加  
- **Key3**：报警距离减小  

## 技术参数

- **测距范围**：2 cm – 400 cm  
- **测距精度**：±3 mm  
- **更新频率**：10 Hz  
- **工作电压**：3.3 V  
- **工作温度**：-10 ℃ ~ +60 ℃  

## 故障排除

### 常见问题
1. **OLED 无显示**：检查 I²C 连接和地址设置  
2. **测距异常**：检查超声波模块连接和供电  
3. **串口无输出**：检查波特率设置（115200）  
4. **按键无响应**：检查按键连接和上拉电阻  

## 项目结构
<pre>
STM32-Ultrasonic-Distance-Meter/
├── README.md                 # 项目说明
├── .gitignore               # Git 忽略文件
├── LICENSE                  # 开源许可证
├── src/                     # 源代码
│   ├── User/                # 用户代码
│   ├── Library/             # STM32 库文件
│   └── Start/               # 启动文件
├── project/                 # 工程文件
│   ├── Project.uvprojx      # Keil 工程
│   └── Project.uvoptx       # 工程配置
└── docs/                    # 文档
    ├── hardware.md          # 硬件说明
    └── images/              # 项目图片
</pre>

## 贡献指南

欢迎提交 Issue 和 Pull Request 来改进项目！

## 许可证

本项目采用 MIT 许可证 — 查看 [LICENSE](LICENSE) 文件了解详情。

## 作者

- **开发者**：CreamyKitten  
- **邮箱**：str41379@163.com  
- **项目地址**：https://github.com/CreamyKitten/STM32-OLED-Ultrasonic-Distance-Meter  

## 致谢

感谢 STM32 社区和开源硬件社区的支持！

---

如果本项目对您有帮助，请给个 Star 支持一下！

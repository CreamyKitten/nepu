# nepu
我在大学时写过的作业。(The assignments I did in university)

## 项目列表

### 1. 智能学生成绩信息管理系统
基于Python和Tkinter开发的智能学生成绩信息管理系统，具有完整的用户认证、学生管理、成绩管理、数据分析和可视化功能。

**技术栈**: Python, Tkinter, Pandas, NumPy, Matplotlib, Pillow

**功能特性**:
- 用户认证系统（登录/注册/验证码）
- 学生信息管理（增删改查/搜索筛选）
- 成绩管理（录入/修改/查询/统计）
- 数据分析与可视化（多种图表展示）
- 数据导入导出（Excel格式）
- 智能分析功能（学习情况分析/教学分析）

**安装运行**:
```bash
git clone https://github.com/CreamyKitten/student-grade-management-system
cd student-grade-management-system
pip install -r requirements.txt
python main.py
```

**默认账户**: teacher01 / 123456

### 2. STM32-OLED-Ultrasonic-Distance-Meter
基于STM32F103C8的OLED超声波测距仪系统，支持HC-SR04模块测距、实时显示、串口通信、按键控制和LED报警功能。

**技术栈**: C, STM32F103C8, HC-SR04, OLED

**功能特性**:
- 双超声波模块测距（支持两个HC-SR04同时工作）
- OLED实时显示（128×64屏幕显示距离数据）
- 串口通信（通过UART1发送格式化数据）
- 按键控制（设置报警距离和开关报警功能）
- LED报警（距离小于设定值时自动报警）
- 开机动画（友好的用户界面体验）

**硬件要求**:
- STM32F103C8T6主控芯片
- HC-SR04超声波测距模块×2
- 0.96寸OLED显示屏（I²C接口）
- LED指示灯和按键开关

**开发环境**: Keil MDK-ARM 5.x, STM32F1xx标准外设库

**技术参数**:
- 测距范围：2cm-400cm
- 测距精度：±3mm
- 更新频率：10Hz
- 工作电压：3.3V

## 联系方式
- **开发者**: CreamyKitten
- **邮箱**: str41379@163.com
- **GitHub**: https://github.com/CreamyKitten
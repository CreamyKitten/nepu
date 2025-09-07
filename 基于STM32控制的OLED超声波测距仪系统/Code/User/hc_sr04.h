/**
 * @brief HC-SR04超声波测距模块相关定义
 */

#ifndef _HC_SR04_H_
#define _HC_SR04_H_

#include "stm32f10x.h"
#include "sys.h" 
#include "delay.h"

// 第一个超声波模块引脚定义（PB6/PB7）
#define Trig    (PBout(6))          // 触发信号输出，PB6
#define TRIG_0()         (Trig=0)   // 触发信号低电平
#define TRIG_1()         (Trig=1)   // 触发信号高电平
#define ECHO_R()  {GPIOB->CRL&=0X0FFFFFFF;GPIOB->CRL|=8<<28;}  // 配置ECHO为输入
#define ECHO_IN()           (PBin(7))  // 回响信号输入，PB7

// 获取第一个模块的距离值
unsigned int GetDistance(void);

// 第二个超声波模块引脚定义（PA6/PA7）
#define Trig1    (PAout(6))         // 触发信号输出，PA6
#define TRIG1_0()         (Trig1=0) // 触发信号低电平
#define TRIG1_1()         (Trig1=1) // 触发信号高电平
#define ECHO1_R()  {GPIOA->CRL&=0X0FFFFFFF;GPIOA->CRL|=8<<28;}  // 配置ECHO为输入
#define ECHO1_IN()           (PAin(7))  // 回响信号输入，PA7

// 获取第二个模块的距离值
unsigned int GetDistance1(void);

#endif

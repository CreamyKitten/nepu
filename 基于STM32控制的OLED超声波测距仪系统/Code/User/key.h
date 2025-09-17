/**
 * @brief 按键处理相关定义和函数声明
 */

#ifndef __KEY_H
#define __KEY_H

#include "sys.h"

// 按键引脚定义
#define KEY1 PAin(0)    // 报警开关
#define KEY2 PAin(2)    // 增加距离
#define KEY3 PAin(4)    // 减少距离

// 全局变量声明
extern unsigned int AlarmDis;     // 报警距离阈值
extern unsigned int AlarmDisf;    // 报警功能开关标志

// 函数声明
void Key_Init(void);    // 按键初始化
void KeyFunc(void);     // 按键处理函数

#endif 
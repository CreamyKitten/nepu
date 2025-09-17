/**
 * @brief 显示功能相关定义和函数声明
 */

#ifndef __DISPLAY_H
#define __DISPLAY_H

#include "stm32f10x.h"
#include "OLED.h"
#include "Delay.h"

// 函数声明
void Display_Init(void);                    // 显示初始化
void Display_StartupAnimation(void);        // 显示开机动画
void Display_Update(uint16_t distance,      // 更新显示内容
                   uint16_t alarmDis, 
                   uint8_t alarmState);

#endif 
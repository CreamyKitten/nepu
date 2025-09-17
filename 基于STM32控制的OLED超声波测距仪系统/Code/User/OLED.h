/**
 * @brief OLED显示功能相关定义和函数声明
 */

#ifndef __OLED_H
#define __OLED_H

#include "stm32f10x.h"

// OLED状态结构体
typedef struct{
	unsigned char State;  // OLED显示状态
}Oled_;
extern Oled_ Oled;

// 基本控制函数
void OLED_Init(void);                // 初始化OLED
void OLED_Clear(void);               // 清屏

// 显示函数
void OLED_ShowChar(uint8_t Line, uint8_t Column, char Char);                                  // 显示字符
void OLED_ShowString(uint8_t Line, uint8_t Column, char *String);                            // 显示字符串
void OLED_ShowNum(uint8_t Line, uint8_t Column, uint32_t Number, uint8_t Length);            // 显示无符号数
void OLED_ShowSignedNum(uint8_t Line, uint8_t Column, int32_t Number, uint8_t Length);       // 显示有符号数
void OLED_ShowHexNum(uint8_t Line, uint8_t Column, uint32_t Number, uint8_t Length);         // 显示16进制数
void OLED_ShowBinNum(uint8_t Line, uint8_t Column, uint32_t Number, uint8_t Length);         // 显示2进制数

#endif

/**
 * @brief USART串口通信相关函数声明
 */

#ifndef __USART_H
#define __USART_H

#include "stm32f10x.h"
#include <stdio.h>

// 串口初始化
void USART1_Init(void);
// 发送单字节
void USART1_SendByte(uint8_t Byte);
// 发送数组
void USART1_SendArray(uint8_t *Array, uint16_t Length);
// 发送字符串
void USART1_SendString(char *String);
// 发送数字，自动补零
void USART1_SendNumber(uint32_t Number, uint8_t Length);
uint32_t USART1_Pow(uint32_t X, uint32_t Y);

#endif 
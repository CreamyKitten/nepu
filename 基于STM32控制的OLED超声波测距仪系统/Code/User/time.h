/**
 * @brief 定时器相关定义和函数声明
 */

#ifndef __TIME_H
#define __TIME_H

#include "stm32f10x.h"  

// 时钟计数器结构体
typedef struct{
//	unsigned char t100ms;
	unsigned char tl00msf;      // 100ms标志
	unsigned int t10ms;         // 10ms计数
	unsigned char t10msf;       // 10ms标志
	unsigned int t10mscount;    // 10ms计数器
	u32 t1s;                    // 1s计数
	unsigned char t1sf;         // 1s标志
	unsigned int t100ms;        // 100ms计数
	unsigned char LedTime;      // LED时间
	unsigned char RG;           // 右绿灯
	unsigned char RY;           // 右黄灯
	unsigned char RR;           // 右红灯
	unsigned char LG;           // 左绿灯
	unsigned char LY;           // 左黄灯
	unsigned char LR;           // 左红灯
}clock2_;

extern clock2_ clock2;

// 定时器初始化，arr为自动重装值，psc为预分频值
void TIM2_Int_Init(u16 arr, u16 psc);

#endif

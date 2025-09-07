/**
 * @brief LED控制相关定义和函数声明
 */

#ifndef __LED_H
#define __LED_H

// LED控制结构体
typedef struct{
	unsigned char Flag;   // LED标志位
	unsigned char State;  // LED状态
}Led_;
extern Led_ Led;

// LED引脚定义
#define LED PBout(14)    // LED，PB14

// LED控制函数
void LedIoInit(void);    // LED初始化
void AlaarmOn(void);     // LED开
void AlaarmOff(void);    // LED关

#endif

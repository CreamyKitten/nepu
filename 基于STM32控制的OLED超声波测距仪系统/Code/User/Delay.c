// 基于SysTick定时器的延时功能实现（系统时钟72MHz）
#include "stm32f10x.h"

// 微秒级延时，范围：0~233015us（受限于24位计数器）
void Delay_us(uint32_t xus)
{
	// 配置SysTick定时器
	SysTick->LOAD = 72 * xus;				// 设置重装值，72MHz时钟下每us计数72次
	SysTick->VAL = 0x00;					// 清空当前计数值
	SysTick->CTRL = 0x00000005;				// 使用HCLK时钟源(72MHz)，启动定时器
	while(!(SysTick->CTRL & 0x00010000));	// 等待COUNTFLAG置位（计数完成）
	SysTick->CTRL = 0x00000004;				// 关闭定时器
}

// 毫秒级延时，通过调用微秒延时实现
void Delay_ms(uint32_t xms)
{
	while(xms--)
	{
		Delay_us(1000);				// 1ms = 1000us
	}
}
 
// 秒级延时，通过调用毫秒延时实现
void Delay_s(uint32_t xs)
{
	while(xs--)
	{
		Delay_ms(1000);				// 1s = 1000ms
	}
} 

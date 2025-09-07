// 定时器配置和中断处理，实现精确的时间计数功能
#include "time.h"

// 时钟计数器结构体实例，用于跟踪不同时间间隔
clock2_ clock2;

// 初始化TIM2定时器，配置时钟频率：Freq = 72M/((arr+1)*(psc+1))
// arr: 自动重装值，psc: 预分频系数
void TIM2_Int_Init(u16 arr , u16 psc)
{
	TIM_TimeBaseInitTypeDef  TIM_TimeBaseStructure;
	NVIC_InitTypeDef NVIC_InitStructure;

	// 使能TIM2时钟
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2, ENABLE); 

	// 配置定时器基本参数
	TIM_TimeBaseStructure.TIM_Period = arr;      // 设置计数器重装值
	TIM_TimeBaseStructure.TIM_Prescaler = psc;   // 设置预分频值
	TIM_TimeBaseStructure.TIM_ClockDivision = TIM_CKD_DIV1;     // 设置时钟分频因子
	TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_Up;  // 向上计数模式
	TIM_TimeBaseInit(TIM2, &TIM_TimeBaseStructure); 
 
	// 使能TIM2更新中断
	TIM_ITConfig(TIM2 , TIM_IT_Update , ENABLE ); 
	
	// 配置NVIC中断优先级
	NVIC_InitStructure.NVIC_IRQChannel = TIM2_IRQn;  // 选择TIM2中断通道
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 2;  // 抢占优先级2
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 3;         // 子优先级3
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;            // 使能中断通道
	NVIC_Init(&NVIC_InitStructure);  

	// 使能TIM2计数器
	TIM_Cmd(TIM2, ENABLE);  	 
}

// TIM2中断处理函数，每次中断更新10ms、100ms和1s计数器
void TIM2_IRQHandler()
{
	if(TIM_GetITStatus(TIM2 , TIM_IT_Update) != RESET) 
	{
		// 更新各个时间计数器
		clock2.t1s++;      // 1秒计数器
		clock2.t10ms++;    // 10毫秒计数器
		clock2.t100ms++;   // 100毫秒计数器

		// 10ms定时标志处理
		if(clock2.t10ms>100){  // 达到100个计数周期（1秒）
			clock2.t10msf=1;   // 设置10ms标志位
			clock2.t10ms=0;    // 清零计数器
		}

		// 1s定时标志处理
		if(clock2.t1s>=2500){  // 达到2500个计数周期（2.5秒）
			clock2.t1sf=1;     // 设置1s标志位
			clock2.t1s=0;      // 清零计数器
		}

		// 清除中断标志位，为下一次中断做准备
		TIM_ClearITPendingBit(TIM2 , TIM_IT_Update ); 
	}
}


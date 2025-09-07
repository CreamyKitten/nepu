/**
 * @file main.c
 * @brief 主程序文件，实现超声波测距系统的主要功能
 * @details 本文件包含了主循环控制和系统初始化
 */

#include "stm32f10x.h"                  // Device header
#include "main.h"
#include "usart.h"
#include "key.h"
#include "display.h"

/**
 * @brief 主函数
 * @details 程序入口，实现：
 *          1. 外设初始化
 *          2. 显示开机动画
 *          3. 发送欢迎信息
 *          4. 主循环中实现距离测量、显示更新和报警控制
 */
int main(void)
{
	// 初始化外设
	TIM2_Int_Init(100, 72);
	LedIoInit();
	Display_Init();
	Key_Init();
	USART1_Init();
	
	// 显示开机动画
	Display_StartupAnimation();
	
	// 发送欢迎信息到串口
	USART1_SendString("\r\n============================\r\n");
	USART1_SendString("  Distance Measurement System\r\n");
	USART1_SendString("============================\r\n\r\n");
	
	while (1)
	{
		if(clock2.t1sf==1)
		{
			clock2.t1sf=0;
			
			// 获取距离数据
			uint16_t distance = GetDistance1();
			
			// 更新显示
			Display_Update(distance, AlarmDis, AlarmDisf);
			
			// 发送格式化的串口数据
			USART1_SendString("| Distance: ");
			USART1_SendNumber(distance, 3);
			USART1_SendString(" cm | Alarm: ");
			USART1_SendNumber(AlarmDis, 3);
			USART1_SendString(" cm | Status: ");
			USART1_SendString(AlarmDisf ? "ON " : "OFF");
			USART1_SendString(" |\r\n");
			
			// 报警控制
			if(distance < AlarmDis && AlarmDisf==1)
			{
				AlaarmOn();
			}
			else
			{
				AlaarmOff();
			}
		}
		KeyFunc();
	}
}

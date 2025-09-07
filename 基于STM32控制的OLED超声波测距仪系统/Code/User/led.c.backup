/**
 * @file led.c
 * @brief LED控制功能实现
 */

#include "main.h"

// LED控制结构体实例
Led_ Led;

/**
 * @brief 初始化LED的GPIO引脚
 * @param None
 * @return None
 */
void LedIoInit(void){
	// 使能GPIOB时钟
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);
	
	GPIO_InitTypeDef GPIO_InitStructure;
	// 配置为推挽输出模式
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
	// 设置PB14引脚
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_14;
	// 设置GPIO速度为50MHz
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOB, &GPIO_InitStructure);
	
	GPIO_SetBits(GPIOB, GPIO_Pin_14);  // 默认LED关闭（高电平熄灭）
}

/**
 * @brief 开启LED
 * @param None
 * @return None
 */
void AlaarmOn(void){
	GPIO_ResetBits(GPIOB, GPIO_Pin_14);  // 输出低电平点亮LED
}

/**
 * @brief 关闭LED
 * @param None
 * @return None
 */
void AlaarmOff(void){
	GPIO_SetBits(GPIOB, GPIO_Pin_14);    // 输出高电平熄灭LED
	}


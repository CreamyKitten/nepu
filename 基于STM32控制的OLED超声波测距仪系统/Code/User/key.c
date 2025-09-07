/**
 * @file key.c
 * @brief 按键处理功能实现
 */

#include "key.h"
#include "stm32f10x.h"

// 全局变量定义
unsigned int AlarmDis = 20;     // 报警距离阈值，默认20cm
unsigned int AlarmDisf = 1;     // 报警功能开关标志，1开启，0关闭
static unsigned char KeyPress = 0;     // 按键按下标志
static unsigned int KeyCount = 0;      // 按键消抖计数器

/**
 * @brief 初始化按键GPIO
 * @details 配置PA0、PA2、PA4为上拉输入模式
 */
void Key_Init(void)
{
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);
    
    GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0 | GPIO_Pin_2 | GPIO_Pin_4;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOA, &GPIO_InitStructure);
}

/**
 * @brief 按键功能处理函数
 * @details 处理三个按键的功能：
 *          KEY1: 切换报警开关
 *          KEY2: 增加报警距离
 *          KEY3: 减少报警距离
 */
void KeyFunc(void){
    if(KEY1==0){
        KeyCount++;
        if(KeyCount<5){
            return;
        }
        if(KeyPress==0){
            KeyPress=1;
            AlarmDisf=!AlarmDisf;
        }
    }
    else if(KEY2==0){
        KeyCount++;
        if(KeyCount<5){
            return;
        }
        if(KeyPress==0){
            KeyPress=1;
            AlarmDis++;
        }
    }
    else if(KEY3==0){
        KeyCount++;
        if(KeyCount<5){
            return;
        }
        if(KeyPress==0){
            KeyPress=1;
            AlarmDis--;
        }
    }
    else{
        KeyPress=0;
        KeyCount=0;
    }               
} 
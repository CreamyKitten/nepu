/**
 * @file hc_sr04.c
 * @brief HC-SR04超声波测距模块驱动实现
 * @details 实现了两个超声波模块的初始化和距离测量功能
 */

#include  <stdlib.h>
#include  <stdio.h>
#include "hc_sr04.h"
#include "math.h"
#include "delay.h"

/**
 * @brief 初始化第一个HC-SR04模块的GPIO引脚
 * @details 配置PB6(TRIG)和PB7(ECHO)为推挽输出模式
 *          初始化时设置引脚为高电平
 * @param None
 * @return None
 */
void IO_INIT(void)
{
    GPIO_InitTypeDef  GPIO_InitStructure;
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB,ENABLE); 
    
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_6|GPIO_Pin_7;     // TRIG和ECHO引脚
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;         // 推挽输出
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOB, &GPIO_InitStructure);
    
    GPIO_SetBits(GPIOB,GPIO_Pin_6|GPIO_Pin_7);
}

/**
 * @brief 获取第一个HC-SR04模块的测距结果
 * @details 测量流程：
 *          1. 初始化IO
 *          2. 发送20us的触发信号
 *          3. 等待回响信号
 *          4. 计算距离（距离 = 时间 * 声速 / 2）
 * @return unsigned int 返回测得的距离，单位为厘米
 */
unsigned int GetDistance(void)
{
    int us_count=0;
    unsigned int distance_data=0;

    IO_INIT();
    ECHO_R();

    // 发送触发信号
    TRIG_1();// 设置TRIG引脚为高电平
    Delay_us(20);
    TRIG_0();         

    // 等待回响信号
    while(ECHO_IN()==0); // 等待ECHO变高(超声波开始传播)
    while(ECHO_IN()==1)  // 测量ECHO高电平持续时间
    {
        Delay_us(10);
        us_count++;
    }

    // 计算距离
    distance_data=us_count*10;  // 总时间(微秒) = 计数*10us
    distance_data/=58;  // 距离(cm) = 时间(μs)/58
    
    return distance_data;
}

/**
 * @brief 初始化第二个HC-SR04模块的GPIO引脚
 * @details 配置PA6(TRIG)和PA7(ECHO)为推挽输出模式
 *          初始化时设置引脚为高电平
 * @param None
 * @return None
 */
void IO_INIT1(void)
{
    GPIO_InitTypeDef  GPIO_InitStructure;
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA,ENABLE); 
    
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_6|GPIO_Pin_7;     // TRIG和ECHO引脚
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;         // 推挽输出
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOA, &GPIO_InitStructure);
    
    GPIO_SetBits(GPIOA,GPIO_Pin_6|GPIO_Pin_7);
}

/**
 * @brief 获取第二个HC-SR04模块的测距结果
 * @details 测量流程与第一个模块相同，但使用不同的GPIO引脚
 * @return unsigned int 返回测得的距离，单位为厘米
 */
unsigned int GetDistance1(void)
{
    int us_count1=0;
    unsigned int distance_data1=0;

    IO_INIT1();
    ECHO1_R();

    // 发送触发信号
    TRIG1_1();
    Delay_us(20);
    TRIG1_0();         

    // 等待回响信号
    while(ECHO1_IN()==0); 
    while(ECHO1_IN()==1)
    {
        Delay_us(10);
        us_count1++;
    }

    // 计算距离
    distance_data1=us_count1*10;
    distance_data1/=58;
    
    return distance_data1;
}

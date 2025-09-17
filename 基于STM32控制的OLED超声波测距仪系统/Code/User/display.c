/**
 * @file display.c
 * @brief 显示功能实现
 */

#include "display.h"

/**
 * @brief 显示初始化
 */
void Display_Init(void)
{
    OLED_Init();
}

/**
 * @brief 显示开机动画
 * @details 显示欢迎信息和加载动画效果
 */
void Display_StartupAnimation(void)
{
    // 清屏
    OLED_Clear();
    
    // 显示欢迎信息
    OLED_ShowString(1, 2, "Welcome to");
    OLED_ShowString(2, 1, "Distance Meter");
    
    // 显示加载动画
    for(uint8_t i = 1; i <= 16; i++)
    {
        OLED_ShowString(3, i, ">");
        Delay_ms(50);
    }
    
    OLED_Clear();
}

/**
 * @brief 更新OLED显示内容
 * @param distance 当前测量的距离值
 * @param alarmDis 报警阈值距离
 * @param alarmState 报警状态（开/关）
 */
void Display_Update(uint16_t distance, uint16_t alarmDis, uint8_t alarmState)
{
    static uint16_t maxDist = 0;
    static uint16_t minDist = 9999;
    
    // 更新最大最小值
    if(distance > maxDist) maxDist = distance;  // 如果当前距离大于最大距离，更新最大距离// 如果当前距离小于最小距离且大于0，更新最小距离
    if(distance < minDist && distance > 0) minDist = distance;  // 如果当前距离小于最小距离且大于0，更新最小距离
    
    // 显示标题
    OLED_ShowString(1, 1, "Distance Monitor");
    
    // 显示当前距离
    OLED_ShowString(2, 1, "Dist:");
    OLED_ShowNum(2, 6, distance, 3);
    OLED_ShowString(2, 9, "cm");
    
    // 显示报警阈值
    OLED_ShowString(3, 1, "Alarm:");
    OLED_ShowNum(3, 7, alarmDis, 3);
    OLED_ShowString(3, 10, "cm");
    OLED_ShowString(3, 13, alarmState ? "ON " : "OFF");
    
    // 显示最大最小值
    OLED_ShowString(4, 1, "Max:");
    OLED_ShowNum(4, 5, maxDist, 3);
    OLED_ShowString(4, 9, "Min:");
    OLED_ShowNum(4, 13, minDist, 3);
} 
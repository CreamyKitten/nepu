/**
 * @file usart.c
 * @brief USART串口通信相关功能实现
 * @details 实现了USART1的初始化和数据发送功能
 */

#include "usart.h"

/**
 * @brief 初始化USART1串口
 * @details 配置USART1的GPIO和通信参数：
 *          - PA9(TX)：复用推挽输出
 *          - PA10(RX)：浮空输入
 *          - 波特率：115200
 *          - 8位数据位，1位停止位，无校验位
 * @param None
 * @return None
 */
void USART1_Init(void)
{
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_USART1, ENABLE);
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);
    
    // 配置GPIO
    GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_9;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOA, &GPIO_InitStructure);
    
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN_FLOATING;
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_10;
    GPIO_Init(GPIOA, &GPIO_InitStructure);
    
    // 配置USART
    USART_InitTypeDef USART_InitStructure;
    USART_InitStructure.USART_BaudRate = 115200;
    USART_InitStructure.USART_WordLength = USART_WordLength_8b;
    USART_InitStructure.USART_StopBits = USART_StopBits_1;
    USART_InitStructure.USART_Parity = USART_Parity_No;
    USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;
    USART_InitStructure.USART_Mode = USART_Mode_Tx | USART_Mode_Rx;
    USART_Init(USART1, &USART_InitStructure);
    
    USART_Cmd(USART1, ENABLE);
}

/**
 * @brief 通过USART1发送单个字节
 * @param Byte 要发送的字节数据
 * @details 等待发送完成后才返回
 */
void USART1_SendByte(uint8_t Byte)
{
    USART_SendData(USART1, Byte);
    while(USART_GetFlagStatus(USART1, USART_FLAG_TXE) == RESET);
}

/**
 * @brief 通过USART1发送数组
 * @param Array 要发送的数组指针
 * @param Length 数组长度
 * @details 循环发送数组中的每个字节
 */
void USART1_SendArray(uint8_t *Array, uint16_t Length)
{
    uint16_t i;
    for(i = 0; i < Length; i++)
    {
        USART1_SendByte(Array[i]);
    }
}

/**
 * @brief 通过USART1发送字符串
 * @param String 要发送的字符串指针
 * @details 发送以'\0'结尾的字符串
 */
void USART1_SendString(char *String)
{
    uint8_t i;
    for(i = 0; String[i] != '\0'; i++)
    {
        USART1_SendByte(String[i]);
    }
}

/**
 * @brief 通过USART1发送数字
 * @param Number 要发送的数字
 * @param Length 数字的位数
 * @details 将数字转换为ASCII字符后发送
 *          如果数字位数不足Length，前面补0
 */
void USART1_SendNumber(uint32_t Number, uint8_t Length)
{
    uint8_t i;
    uint8_t Buffer[10];
    for(i = 0; i < Length; i++)
    {
        Buffer[Length - i - 1] = Number % 10 + '0';
        Number /= 10;
    }
    USART1_SendArray(Buffer, Length);
} 
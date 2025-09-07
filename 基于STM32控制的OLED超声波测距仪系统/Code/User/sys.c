// 系统底层功能实现，包含CPU和中断控制函数
#include "sys.h"
 
// 使CPU进入休眠状态，等待中断唤醒（WFI指令）
void WFI_SET(void)
{
	__ASM volatile("wfi");      // Wait For Interrupt指令，降低功耗
}

// 关闭所有可屏蔽中断（PRIMASK=1）
void INTX_DISABLE(void)
{		  
	__ASM volatile("cpsid i");  // Change Processor State, Disable Interrupts
}

// 使能所有可屏蔽中断（PRIMASK=0）
void INTX_ENABLE(void)
{
	__ASM volatile("cpsie i");  // Change Processor State, Enable Interrupts
}

// 设置主堆栈指针MSP（Main Stack Pointer）
// addr: 新的堆栈指针地址
__asm void MSR_MSP(u32 addr) 
{
	MSR MSP, r0             // 将r0寄存器的值加载到MSP
	BX r14                  // 返回调用函数（r14是链接寄存器LR）
}

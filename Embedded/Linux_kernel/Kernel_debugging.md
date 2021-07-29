### Kernel Debugging

1. Debugging 이란?

   - 디버깅은 버그를 잡는 과정이다.
   - 더 나아가 리눅스 커널과 드라이버가 정상 동작할 때 자료구조와 함수 흐름까지 파악하는 것
   - 커널 디버깅은 실전 개발과 코드 학습에 매우 중요하다.

2. Debugging - 문제 해결 능력

   - 커널 디버기은 문제 해결 능력 그 자체이기 때문에 대부분의 임베디드 및 BSP 개발자들은 커널 디버깅 능력을 키우기위해 노력한다.

   - ```
     개발 도중 만나는 문제들
     1. 부팅 도중 커널 크래시 발생
     2. 인터럽트 핸들러를 설정했는데 인터럽트 핸들러가 호출되지 않음
     3. 시스템 응답 속도가 매우 느려짐
     4. 파일 복사가 안 됨
     ```

   - 실전 개발에서는 확보한 커널 로그와 메모리 덤프로 문제 원인 분석

   - 커널 디버깅 할때는 다른개발자가 작성한커널 코드를 만날 가능성이높다.

     - 이유 : 디바이스 드라이버는 커널 함수로 구성돼 있고 커널 함수는 각 서브시스템을 담당한 개발자가작성한코드이기 때문

   - 디버깅 시 커널을구성하는 서브시스템이 정상적으로 동작할 때 다음 내용을 파악할 필요가 있다.

     - ```
       1. 함수가 실행될때 변경되는 자료구조
       2. 함수가 실행되는 빈도와 실행 시간
       3. 실행 중인 코드르 어떤 프로세스가 실행하는지 확인
       ```

     - 이유 : 프로그램이 정상적으로 동작할 때 함수 호출 흐름과 자료구조를 알고 있어야 오류나 버그가 발생했을 때 무엇이 문제인지 판단할 수 있기 때문

3. 디버깅 따라해보기 - 커널 로그 분석

   - 임베디드 리눅스 개발 시 문제가 생기면 대부분 커널 로그를 본다.
   - 디바이스 드라이버는 드라이버 코드에서 오류메시지를 출력하지 않고 드라이버가 호출한 커널 함수 내부에서 출력한다.

   - https://www.unix.com/programming/148285-what-unbalanced-irq.html : 리눅스 포럼에서 논의된 커널로그

   - ```
     WARNING: at kernel/irq/manage.c:225 __enable_irq+0x3b/0x57()
     Unbalanced enable for IRQ 4
     Modules linked in: svsknfdrvr [last unloaded: osal_linux]
     Pid: 634, comm: ash Tainted: G W 2.6.28 #1
     Call Trace:
     [<c011a7f9>] warn_slowpath+0x76/0x8d
     [<c012fac8>] profile_tick+0x2d/0x57
     [<c011ed72>] irq_exit+0x32/0x34
     [<c010f22c>] smp_apic_timer_interrupt+0x41/0x71
     [<c01039ec>] apic_timer_interrupt+0x28/0x30
     [<c011b2b4>] vprintk+0x1d3/0x300
     [<c013a2af>] __setup_irq+0x11c/0x1f2
     [<c013a177>] __enable_irq+0x3b/0x57
     [<c013a506>] enable_irq+0x37/0x54
     [<c68c9156>] svsknfdrvr_open+0x5e/0x65 [svsknfdrvr]
     [<c016440a>] chrdev_open+0xce/0x1a4
     [<c016433c>] chrdev_open+0x0/0x1a4
     [<c01602f7>] __dentry_open+0xcc/0x23a
     [<c016049a>] nameidata_to_filp+0x35/0x3f
     [<c016b3c5>] do_filp_open+0x16f/0x6ef
     [<c0278fd5>] tty_write+0x1a2/0x1c9
     [<c0160128>] do_sys_open+0x42/0xcb
     [<c0160201>] sys_open+0x23/0x2a
     [<c0102e71>] sysenter_do_call+0x12/0x25
     ```

   - 분석 첫번 째 : 오류 메시지를 커널의 어느 코드에서 출력했는지 확인

     - ```
       WARNING: at kernel/irq/manage.c:225 __enable_irq+0x3b/0x57()
       ```

     - https://github.com/raspberrypi/linux/blob/rpi-5.10.y/kernel/irq/manage.c : __enable() 함수 확인

     - ```c
       // __enable_irq() 함수의 읿부
       void __enable_irq(struct irq_desc *desc)
       {
       	switch (desc->depth) {
       	case 0:
        err_out:
       		WARN(1, KERN_WARNING "Unbalanced enable for IRQ %d\n",
       		     irq_desc_get_irq(desc));
       ```

     - irq_desc 구조체의 depth 필드는 인터럽트 활성화 시 0, 비활성화 시 1 설정

     - err_out의 코드는 인터럽트 2번 활성화 시 실행 -> 이미 인터럽트를 활성화했는데 다시 활성화했으니 경고 메시지와  함께 콜 스택 출력(WARN() 매크로 함수가 호출되면 커널 로그로 콜 스택 출력)

   - 분석 두번째 : 소스코드에서 에러 메시지 출력한 이유 살펴보기

     - ```
       WARNING: at kernel/irq/manage.c:225 __enable_irq+0x3b/0x57()
       Unbalanced enable for IRQ 4
       ```

     - 4번 인터럽트를 2번 호출했다는 의미

     - 위 에러 메시지는 enable_irq() 함수에서 출력하는데 이는 이 함수를 호출한 드라이버 코드에 오류가 있을 가능성이 높다는 것을 의미한다.

     - 문제 해결을 위해서 드라이버 코드를 분석한다.

     - ```
       WARNING: at kernel/irq/manage.c:225 __enable_irq+0x3b/0x57()
       Unbalanced enable for IRQ 4
       Modules linked in: svsknfdrvr [last unloaded: osal_linux]
       ```

     - svsknfdrvr 드라이버 모듈이 언급되어 있다. 만약 enable_irq() 함수를 호출한 코드가 svsknfdrvr 드라이버 코드에 있다면 이를 분석한 후 오류가 있는지 점검한다.

   - 분석 셋째 : 필요에따라 디버깅 코드를 작성해 다시 문제가 발생했을 때 추가 커널 로그 확보를 시도한다.

     - ```c
       diff --git a/kernel/irq/manage.c b/kernel/irq/manage.c
       --- a/kernel/irq/manage.c
       +++ b/kernel/irq/manage.c
       @@ -388,6 +388,8 @@ setup_affinity(unsigned int irq, struct irq_desc *desc, struct cpumask *mask)
       void __disable_irq(struct irq_desc *desc, unsigned int irq)
       {
       	if(irq == 4)
           	WARN(1, KERN_WARNING "irq 4 is disabled %d, desc->depth %d \n", irq,
                   desc->depth);
           if (!desc->depth++)
       		irq_disable(desc);
       }
       
       @@-442,6 +444,9 @@ EXPORT_SYMBOL(disable_irq);
       
       void __enable_irq(struct irq_desc *desc, unsigned int irq)
       {
       	if(irq == 4)
           	WARN(1, KERN_WARNING "irq 4 is enabled %d, desc->depth %d \n", irq,
                   desc->depth);
       	switch(desc->depth){
       	case 0;
       err_out:
       ```

     - 위와 같은 디버깅 패치 코드를 통해 문제의 원인을 찾을 수 있다.

     - 이 패치 코드를 빌드해서 시스템에 반영하면 어떤 코드에서 4번 인터럽트를 연속으로 활성화하는지 알 수 있다.

   - 결론적으로 디버깅 능력이 문제 해결 능력과 마찬가지이므로 디버깅 실력을 늘릴 필요가 있다.


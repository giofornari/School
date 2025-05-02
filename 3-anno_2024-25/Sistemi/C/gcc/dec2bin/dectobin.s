	.file	"dectobin.c"
	.text
	.section	.rodata
	.align 8
.LC0:
	.string	"Inserisci un numero da convertire in binario: "
.LC1:
	.string	"%d"
	.text
	.globl	main
	.type	main, @function
main:
.LFB0:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$32, %rsp
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	leaq	.LC0(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-24(%rbp), %rax
	movq	%rax, %rsi
	leaq	.LC1(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	__isoc99_scanf@PLT
	movl	-24(%rbp), %eax
	testl	%eax, %eax
	jns	.L2
	movl	$45, %edi
	call	putchar@PLT
	movl	-24(%rbp), %eax
	negl	%eax
	movl	%eax, -20(%rbp)
	jmp	.L3
.L2:
	movl	-24(%rbp), %eax
	movl	%eax, -20(%rbp)
.L3:
	movl	$31, -16(%rbp)
	jmp	.L4
.L6:
	subl	$1, -16(%rbp)
.L4:
	cmpl	$0, -16(%rbp)
	js	.L5
	movl	-16(%rbp), %eax
	movl	-20(%rbp), %edx
	movl	%eax, %ecx
	shrl	%cl, %edx
	movl	%edx, %eax
	andl	$1, %eax
	testl	%eax, %eax
	je	.L6
.L5:
	movl	-16(%rbp), %eax
	movl	%eax, -12(%rbp)
	jmp	.L7
.L10:
	movl	-12(%rbp), %eax
	movl	-20(%rbp), %edx
	movl	%eax, %ecx
	shrl	%cl, %edx
	movl	%edx, %eax
	andl	$1, %eax
	testl	%eax, %eax
	je	.L8
	movl	$49, %edi
	call	putchar@PLT
	jmp	.L9
.L8:
	movl	$48, %edi
	call	putchar@PLT
.L9:
	subl	$1, -12(%rbp)
.L7:
	cmpl	$0, -12(%rbp)
	jns	.L10
	movl	$10, %edi
	call	putchar@PLT
	movl	$0, %eax
	movq	-8(%rbp), %rdx
	subq	%fs:40, %rdx
	je	.L12
	call	__stack_chk_fail@PLT
.L12:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	main, .-main
	.ident	"GCC: (GNU) 14.2.1 20250207"
	.section	.note.GNU-stack,"",@progbits

	.file	"terne.c"
	.text
	.section	.rodata
.LC0:
	.string	"Inserisci il valore max: "
.LC1:
	.string	"%d"
.LC2:
	.string	"Terna: %d, %d, %d\n"
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
	subq	$48, %rsp
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	leaq	.LC0(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-36(%rbp), %rax
	movq	%rax, %rsi
	leaq	.LC1(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	__isoc99_scanf@PLT
	movl	$1, -32(%rbp)
	jmp	.L2
.L9:
	movl	-32(%rbp), %eax
	addl	$1, %eax
	movl	%eax, -28(%rbp)
	jmp	.L3
.L8:
	movl	-32(%rbp), %eax
	imull	%eax, %eax
	movl	%eax, %edx
	movl	-28(%rbp), %eax
	imull	%eax, %eax
	addl	%edx, %eax
	movl	%eax, -24(%rbp)
	movl	-36(%rbp), %edx
	movl	-36(%rbp), %eax
	imull	%edx, %eax
	cmpl	%eax, -24(%rbp)
	jg	.L13
	pxor	%xmm1, %xmm1
	cvtsi2sdl	-24(%rbp), %xmm1
	movq	%xmm1, %rax
	movq	%rax, %xmm0
	call	sqrt@PLT
	movq	%xmm0, %rax
	movq	%rax, -16(%rbp)
	movsd	-16(%rbp), %xmm0
	cvttsd2sil	%xmm0, %eax
	movl	%eax, -20(%rbp)
	pxor	%xmm0, %xmm0
	cvtsi2sdl	-20(%rbp), %xmm0
	ucomisd	-16(%rbp), %xmm0
	jp	.L6
	ucomisd	-16(%rbp), %xmm0
	jne	.L6
	movl	-36(%rbp), %eax
	cmpl	%eax, -20(%rbp)
	jg	.L6
	movl	-20(%rbp), %eax
	imull	%eax, %eax
	cmpl	%eax, -24(%rbp)
	jne	.L6
	movl	-20(%rbp), %ecx
	movl	-28(%rbp), %edx
	movl	-32(%rbp), %eax
	movl	%eax, %esi
	leaq	.LC2(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
.L6:
	addl	$1, -28(%rbp)
.L3:
	movl	-36(%rbp), %eax
	cmpl	%eax, -28(%rbp)
	jle	.L8
	jmp	.L5
.L13:
	nop
.L5:
	addl	$1, -32(%rbp)
.L2:
	movl	-36(%rbp), %eax
	cmpl	%eax, -32(%rbp)
	jle	.L9
	movl	$0, %eax
	movq	-8(%rbp), %rdx
	subq	%fs:40, %rdx
	je	.L11
	call	__stack_chk_fail@PLT
.L11:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	main, .-main
	.ident	"GCC: (GNU) 14.2.1 20250207"
	.section	.note.GNU-stack,"",@progbits

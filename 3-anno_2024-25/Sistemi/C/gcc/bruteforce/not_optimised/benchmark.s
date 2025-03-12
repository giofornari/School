	.file	"benchmark.c"
	.text
	.globl	A
	.bss
	.align 32
	.type	A, @object
	.size	A, 8000000
A:
	.zero	8000000
	.globl	B
	.align 32
	.type	B, @object
	.size	B, 8000000
B:
	.zero	8000000
	.globl	C
	.align 32
	.type	C, @object
	.size	C, 8000000
C:
	.zero	8000000
	.section	.rodata
	.align 8
.LC3:
	.string	"Tempo impiegato per la moltiplicazione delle matrici: %.3f secondi\n"
	.text
	.globl	main
	.type	main, @function
main:
.LFB6:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$48, %rsp
	movl	$0, %edi
	call	time@PLT
	movl	%eax, %edi
	call	srand@PLT
	movl	$0, -44(%rbp)
	jmp	.L2
.L5:
	movl	$0, -40(%rbp)
	jmp	.L3
.L4:
	call	rand@PLT
	pxor	%xmm0, %xmm0
	cvtsi2sdl	%eax, %xmm0
	movsd	.LC0(%rip), %xmm1
	divsd	%xmm1, %xmm0
	movl	-40(%rbp), %eax
	cltq
	movl	-44(%rbp), %edx
	movslq	%edx, %rdx
	imulq	$1000, %rdx, %rdx
	addq	%rdx, %rax
	leaq	0(,%rax,8), %rdx
	leaq	A(%rip), %rax
	movsd	%xmm0, (%rdx,%rax)
	call	rand@PLT
	pxor	%xmm0, %xmm0
	cvtsi2sdl	%eax, %xmm0
	movsd	.LC0(%rip), %xmm1
	divsd	%xmm1, %xmm0
	movl	-40(%rbp), %eax
	cltq
	movl	-44(%rbp), %edx
	movslq	%edx, %rdx
	imulq	$1000, %rdx, %rdx
	addq	%rdx, %rax
	leaq	0(,%rax,8), %rdx
	leaq	B(%rip), %rax
	movsd	%xmm0, (%rdx,%rax)
	addl	$1, -40(%rbp)
.L3:
	cmpl	$999, -40(%rbp)
	jle	.L4
	addl	$1, -44(%rbp)
.L2:
	cmpl	$999, -44(%rbp)
	jle	.L5
	call	clock@PLT
	movq	%rax, -24(%rbp)
	movl	$0, -36(%rbp)
	jmp	.L6
.L11:
	movl	$0, -32(%rbp)
	jmp	.L7
.L10:
	movl	-32(%rbp), %eax
	cltq
	movl	-36(%rbp), %edx
	movslq	%edx, %rdx
	imulq	$1000, %rdx, %rdx
	addq	%rdx, %rax
	leaq	0(,%rax,8), %rdx
	leaq	C(%rip), %rax
	pxor	%xmm0, %xmm0
	movsd	%xmm0, (%rdx,%rax)
	movl	$0, -28(%rbp)
	jmp	.L8
.L9:
	movl	-32(%rbp), %eax
	cltq
	movl	-36(%rbp), %edx
	movslq	%edx, %rdx
	imulq	$1000, %rdx, %rdx
	addq	%rdx, %rax
	leaq	0(,%rax,8), %rdx
	leaq	C(%rip), %rax
	movsd	(%rdx,%rax), %xmm1
	movl	-28(%rbp), %eax
	cltq
	movl	-36(%rbp), %edx
	movslq	%edx, %rdx
	imulq	$1000, %rdx, %rdx
	addq	%rdx, %rax
	leaq	0(,%rax,8), %rdx
	leaq	A(%rip), %rax
	movsd	(%rdx,%rax), %xmm2
	movl	-32(%rbp), %eax
	cltq
	movl	-28(%rbp), %edx
	movslq	%edx, %rdx
	imulq	$1000, %rdx, %rdx
	addq	%rdx, %rax
	leaq	0(,%rax,8), %rdx
	leaq	B(%rip), %rax
	movsd	(%rdx,%rax), %xmm0
	mulsd	%xmm2, %xmm0
	addsd	%xmm1, %xmm0
	movl	-32(%rbp), %eax
	cltq
	movl	-36(%rbp), %edx
	movslq	%edx, %rdx
	imulq	$1000, %rdx, %rdx
	addq	%rdx, %rax
	leaq	0(,%rax,8), %rdx
	leaq	C(%rip), %rax
	movsd	%xmm0, (%rdx,%rax)
	addl	$1, -28(%rbp)
.L8:
	cmpl	$999, -28(%rbp)
	jle	.L9
	addl	$1, -32(%rbp)
.L7:
	cmpl	$999, -32(%rbp)
	jle	.L10
	addl	$1, -36(%rbp)
.L6:
	cmpl	$999, -36(%rbp)
	jle	.L11
	call	clock@PLT
	movq	%rax, -16(%rbp)
	movq	-16(%rbp), %rax
	subq	-24(%rbp), %rax
	pxor	%xmm0, %xmm0
	cvtsi2sdq	%rax, %xmm0
	movsd	.LC2(%rip), %xmm1
	divsd	%xmm1, %xmm0
	movsd	%xmm0, -8(%rbp)
	movq	-8(%rbp), %rax
	movq	%rax, %xmm0
	leaq	.LC3(%rip), %rax
	movq	%rax, %rdi
	movl	$1, %eax
	call	printf@PLT
	movl	$0, %eax
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE6:
	.size	main, .-main
	.section	.rodata
	.align 8
.LC0:
	.long	-4194304
	.long	1105199103
	.align 8
.LC2:
	.long	0
	.long	1093567616
	.ident	"GCC: (GNU) 14.2.1 20250207"
	.section	.note.GNU-stack,"",@progbits

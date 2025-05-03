	.file	"benchmark.c"
	.text
	.section	.rodata.str1.8,"aMS",@progbits,1
	.align 8
.LC2:
	.string	"Tempo impiegato per la moltiplicazione delle matrici: %.3f secondi\n"
	.section	.text.startup,"ax",@progbits
	.p2align 4
	.globl	main
	.type	main, @function
main:
.LFB22:
	.cfi_startproc
	pushq	%r15
	.cfi_def_cfa_offset 16
	.cfi_offset 15, -16
	xorl	%edi, %edi
	pushq	%r14
	.cfi_def_cfa_offset 24
	.cfi_offset 14, -24
	leaq	B(%rip), %r14
	pushq	%r13
	.cfi_def_cfa_offset 32
	.cfi_offset 13, -32
	movq	%r14, %r13
	pushq	%r12
	.cfi_def_cfa_offset 40
	.cfi_offset 12, -40
	leaq	A(%rip), %r12
	pushq	%rbp
	.cfi_def_cfa_offset 48
	.cfi_offset 6, -48
	leaq	8000000(%r12), %r15
	movq	%r12, %rbp
	pushq	%rbx
	.cfi_def_cfa_offset 56
	.cfi_offset 3, -56
	subq	$8, %rsp
	.cfi_def_cfa_offset 64
	call	time@PLT
	movl	%eax, %edi
	call	srand@PLT
.L2:
	xorl	%ebx, %ebx
.L3:
	call	rand@PLT
	pxor	%xmm0, %xmm0
	cvtsi2sdl	%eax, %xmm0
	divsd	.LC0(%rip), %xmm0
	movsd	%xmm0, 0(%rbp,%rbx)
	call	rand@PLT
	pxor	%xmm0, %xmm0
	cvtsi2sdl	%eax, %xmm0
	divsd	.LC0(%rip), %xmm0
	movsd	%xmm0, 0(%r13,%rbx)
	addq	$8, %rbx
	cmpq	$8000, %rbx
	jne	.L3
	addq	$8000, %rbp
	addq	$8000, %r13
	cmpq	%r15, %rbp
	jne	.L2
	call	clock@PLT
	leaq	C(%rip), %r10
	xorl	%r9d, %r9d
	leaq	8008000(%r14), %r8
	movq	%rax, %rbx
	leaq	8000000+B(%rip), %r11
.L5:
	imulq	$8000, %r9, %rdi
	movq	%r11, %rcx
	movq	%r10, %rsi
	addq	%r12, %rdi
.L7:
	leaq	-8000000(%rcx), %rax
	movq	%rdi, %rdx
	pxor	%xmm1, %xmm1
	.p2align 6
	.p2align 4
	.p2align 3
.L6:
	movsd	(%rdx), %xmm0
	addq	$8000, %rax
	addq	$8, %rdx
	unpcklpd	%xmm0, %xmm0
	mulpd	-8000(%rax), %xmm0
	addpd	%xmm0, %xmm1
	cmpq	%rcx, %rax
	jne	.L6
	leaq	16(%rax), %rcx
	movaps	%xmm1, (%rsi)
	addq	$16, %rsi
	cmpq	%r8, %rcx
	jne	.L7
	addq	$1, %r9
	addq	$8000, %r10
	cmpq	$1000, %r9
	jne	.L5
	call	clock@PLT
	pxor	%xmm0, %xmm0
	leaq	.LC2(%rip), %rdi
	subq	%rbx, %rax
	cvtsi2sdq	%rax, %xmm0
	movl	$1, %eax
	divsd	.LC1(%rip), %xmm0
	call	printf@PLT
	addq	$8, %rsp
	.cfi_def_cfa_offset 56
	xorl	%eax, %eax
	popq	%rbx
	.cfi_def_cfa_offset 48
	popq	%rbp
	.cfi_def_cfa_offset 40
	popq	%r12
	.cfi_def_cfa_offset 32
	popq	%r13
	.cfi_def_cfa_offset 24
	popq	%r14
	.cfi_def_cfa_offset 16
	popq	%r15
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE22:
	.size	main, .-main
	.globl	C
	.bss
	.align 32
	.type	C, @object
	.size	C, 8000000
C:
	.zero	8000000
	.globl	B
	.align 32
	.type	B, @object
	.size	B, 8000000
B:
	.zero	8000000
	.globl	A
	.align 32
	.type	A, @object
	.size	A, 8000000
A:
	.zero	8000000
	.section	.rodata.cst8,"aM",@progbits,8
	.align 8
.LC0:
	.long	-4194304
	.long	1105199103
	.align 8
.LC1:
	.long	0
	.long	1093567616
	.ident	"GCC: (GNU) 14.2.1 20250207"
	.section	.note.GNU-stack,"",@progbits

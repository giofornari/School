	.file	"benchmark.c"
	.text
	.section	.rodata.str1.8,"aMS",@progbits,1
	.align 8
.LC3:
	.string	"Tempo impiegato per la moltiplicazione delle matrici: %.3f secondi\n"
	.text
	.globl	main
	.type	main, @function
main:
.LFB22:
	.cfi_startproc
	pushq	%r15
	.cfi_def_cfa_offset 16
	.cfi_offset 15, -16
	pushq	%r14
	.cfi_def_cfa_offset 24
	.cfi_offset 14, -24
	pushq	%r13
	.cfi_def_cfa_offset 32
	.cfi_offset 13, -32
	pushq	%r12
	.cfi_def_cfa_offset 40
	.cfi_offset 12, -40
	pushq	%rbp
	.cfi_def_cfa_offset 48
	.cfi_offset 6, -48
	pushq	%rbx
	.cfi_def_cfa_offset 56
	.cfi_offset 3, -56
	subq	$8, %rsp
	.cfi_def_cfa_offset 64
	movl	$0, %edi
	call	time@PLT
	movl	%eax, %edi
	call	srand@PLT
	leaq	A(%rip), %rbp
	leaq	B(%rip), %r12
	leaq	8000000(%rbp), %r15
	movq	%r12, %r14
	movq	%rbp, %r13
.L2:
	movl	$0, %ebx
.L3:
	call	rand@PLT
	pxor	%xmm0, %xmm0
	cvtsi2sdl	%eax, %xmm0
	divsd	.LC1(%rip), %xmm0
	movsd	%xmm0, 0(%r13,%rbx)
	call	rand@PLT
	pxor	%xmm0, %xmm0
	cvtsi2sdl	%eax, %xmm0
	divsd	.LC1(%rip), %xmm0
	movsd	%xmm0, (%r14,%rbx)
	addq	$8, %rbx
	cmpq	$8000, %rbx
	jne	.L3
	addq	$8000, %r13
	addq	$8000, %r14
	cmpq	%r15, %r13
	jne	.L2
	call	clock@PLT
	movq	%rax, %rbx
	movl	$0, %r8d
	leaq	C(%rip), %r10
	leaq	8008000(%r12), %r9
.L5:
	leaq	(%r8,%r10), %rsi
	leaq	8000000(%r12), %rcx
.L7:
	movq	%rsi, %rdi
	leaq	(%r8,%rbp), %rdx
	leaq	-8000000(%rcx), %rax
	pxor	%xmm1, %xmm1
	.p2align 5
.L6:
	movsd	(%rdx), %xmm0
	mulsd	(%rax), %xmm0
	addsd	%xmm0, %xmm1
	addq	$8, %rdx
	addq	$8000, %rax
	cmpq	%rcx, %rax
	jne	.L6
	movsd	%xmm1, (%rdi)
	addq	$8, %rsi
	addq	$8, %rcx
	cmpq	%r9, %rcx
	jne	.L7
	addq	$8000, %r8
	cmpq	$8000000, %r8
	jne	.L5
	call	clock@PLT
	subq	%rbx, %rax
	pxor	%xmm0, %xmm0
	cvtsi2sdq	%rax, %xmm0
	divsd	.LC2(%rip), %xmm0
	leaq	.LC3(%rip), %rdi
	movl	$1, %eax
	call	printf@PLT
	movl	$0, %eax
	addq	$8, %rsp
	.cfi_def_cfa_offset 56
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
.LC1:
	.long	-4194304
	.long	1105199103
	.align 8
.LC2:
	.long	0
	.long	1093567616
	.ident	"GCC: (GNU) 14.2.1 20250207"
	.section	.note.GNU-stack,"",@progbits

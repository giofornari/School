	.file	"b.c"
	.text
	.globl	limite
	.bss
	.align 8
	.type	limite, @object
	.size	limite, 8
limite:
	.zero	8
	.globl	count_naive
	.align 4
	.type	count_naive, @object
	.size	count_naive, 4
count_naive:
	.zero	4
	.globl	count_erato
	.align 4
	.type	count_erato, @object
	.size	count_erato, 4
count_erato:
	.zero	4
	.globl	start
	.align 8
	.type	start, @object
	.size	start, 8
start:
	.zero	8
	.globl	end
	.align 8
	.type	end, @object
	.size	end, 8
end:
	.zero	8
	.globl	cpu_time_used
	.align 8
	.type	cpu_time_used, @object
	.size	cpu_time_used, 8
cpu_time_used:
	.zero	8
	.text
	.globl	isPrime
	.type	isPrime, @function
isPrime:
.LFB6:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movq	%rdi, -24(%rbp)
	cmpq	$1, -24(%rbp)
	ja	.L2
	movl	$0, %eax
	jmp	.L3
.L2:
	cmpq	$3, -24(%rbp)
	ja	.L4
	movl	$1, %eax
	jmp	.L3
.L4:
	movq	-24(%rbp), %rax
	andl	$1, %eax
	testq	%rax, %rax
	je	.L5
	movq	-24(%rbp), %rcx
	movabsq	$-6148914691236517205, %rdx
	movq	%rcx, %rax
	mulq	%rdx
	shrq	%rdx
	movq	%rdx, %rax
	addq	%rax, %rax
	addq	%rdx, %rax
	subq	%rax, %rcx
	movq	%rcx, %rdx
	testq	%rdx, %rdx
	jne	.L6
.L5:
	movl	$0, %eax
	jmp	.L3
.L6:
	movq	$5, -8(%rbp)
	jmp	.L7
.L10:
	movq	-24(%rbp), %rax
	movl	$0, %edx
	divq	-8(%rbp)
	movq	%rdx, %rax
	testq	%rax, %rax
	je	.L8
	movq	-8(%rbp), %rax
	leaq	2(%rax), %rsi
	movq	-24(%rbp), %rax
	movl	$0, %edx
	divq	%rsi
	movq	%rdx, %rcx
	movq	%rcx, %rax
	testq	%rax, %rax
	jne	.L9
.L8:
	movl	$0, %eax
	jmp	.L3
.L9:
	addq	$6, -8(%rbp)
.L7:
	movq	-8(%rbp), %rax
	imulq	%rax, %rax
	cmpq	%rax, -24(%rbp)
	jnb	.L10
	movl	$1, %eax
.L3:
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE6:
	.size	isPrime, .-isPrime
	.section	.rodata
.LC0:
	.string	"Errore di allocazione memoria"
	.text
	.globl	isPrimeErato
	.type	isPrimeErato, @function
isPrimeErato:
.LFB7:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$64, %rsp
	movq	%rdi, -56(%rbp)
	cmpq	$1, -56(%rbp)
	ja	.L12
	movl	$0, %eax
	jmp	.L13
.L12:
	cmpq	$2, -56(%rbp)
	je	.L14
	cmpq	$3, -56(%rbp)
	jne	.L15
.L14:
	movl	$1, %eax
	jmp	.L13
.L15:
	movq	-56(%rbp), %rax
	andl	$1, %eax
	testq	%rax, %rax
	jne	.L16
	movl	$0, %eax
	jmp	.L13
.L16:
	movabsq	$1000000000000000, %rax
	movq	%rax, -16(%rbp)
	movq	-56(%rbp), %rax
	cmpq	-16(%rbp), %rax
	jnb	.L17
	movq	-56(%rbp), %rax
	addq	$1, %rax
	movl	$1, %esi
	movq	%rax, %rdi
	call	calloc@PLT
	movq	%rax, -8(%rbp)
	cmpq	$0, -8(%rbp)
	jne	.L18
	leaq	.LC0(%rip), %rax
	movq	%rax, %rdi
	call	puts@PLT
	movl	$1, %edi
	call	exit@PLT
.L18:
	movq	$2, -32(%rbp)
	jmp	.L19
.L23:
	movq	-8(%rbp), %rdx
	movq	-32(%rbp), %rax
	addq	%rdx, %rax
	movzbl	(%rax), %eax
	testb	%al, %al
	jne	.L20
	movq	-32(%rbp), %rax
	imulq	%rax, %rax
	movq	%rax, -24(%rbp)
	jmp	.L21
.L22:
	movq	-8(%rbp), %rdx
	movq	-24(%rbp), %rax
	addq	%rdx, %rax
	movb	$1, (%rax)
	movq	-32(%rbp), %rax
	addq	%rax, -24(%rbp)
.L21:
	movq	-24(%rbp), %rax
	cmpq	%rax, -56(%rbp)
	jnb	.L22
.L20:
	addq	$1, -32(%rbp)
.L19:
	movq	-32(%rbp), %rax
	imulq	%rax, %rax
	cmpq	%rax, -56(%rbp)
	jnb	.L23
	movq	-8(%rbp), %rdx
	movq	-56(%rbp), %rax
	addq	%rdx, %rax
	movzbl	(%rax), %eax
	testb	%al, %al
	sete	%al
	movzbl	%al, %eax
	movl	%eax, -36(%rbp)
	movq	-8(%rbp), %rax
	movq	%rax, %rdi
	call	free@PLT
	movl	-36(%rbp), %eax
	jmp	.L13
.L17:
	movl	$2, %edi
	call	exit@PLT
.L13:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE7:
	.size	isPrimeErato, .-isPrimeErato
	.section	.rodata
.LC1:
	.string	"%llu"
	.align 8
.LC3:
	.string	"Metodo ingenuo: trovati %d numeri primi fino a %llu in %f secondi\n"
	.align 8
.LC4:
	.string	"Metodo crivello: trovati %d numeri primi fino a %llu in %f secondi\n"
	.align 8
.LC5:
	.string	"I due metodi hanno dato lo stesso risultato: %d numeri primi trovati.\n"
	.align 8
.LC6:
	.string	"ERRORE: i due metodi hanno dato risultati diversi!"
	.text
	.globl	main
	.type	main, @function
main:
.LFB8:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$16, %rsp
	leaq	limite(%rip), %rax
	movq	%rax, %rsi
	leaq	.LC1(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	__isoc99_scanf@PLT
	call	clock@PLT
	movq	%rax, start(%rip)
	movq	$2, -16(%rbp)
	jmp	.L25
.L27:
	movq	-16(%rbp), %rax
	movq	%rax, %rdi
	call	isPrime
	testl	%eax, %eax
	je	.L26
	movl	count_naive(%rip), %eax
	addl	$1, %eax
	movl	%eax, count_naive(%rip)
.L26:
	addq	$1, -16(%rbp)
.L25:
	movq	limite(%rip), %rax
	cmpq	-16(%rbp), %rax
	jnb	.L27
	call	clock@PLT
	movq	%rax, end(%rip)
	movq	end(%rip), %rdx
	movq	start(%rip), %rax
	subq	%rax, %rdx
	pxor	%xmm0, %xmm0
	cvtsi2sdq	%rdx, %xmm0
	movsd	.LC2(%rip), %xmm1
	divsd	%xmm1, %xmm0
	movsd	%xmm0, cpu_time_used(%rip)
	movq	cpu_time_used(%rip), %rcx
	movq	limite(%rip), %rdx
	movl	count_naive(%rip), %eax
	movq	%rcx, %xmm0
	movl	%eax, %esi
	leaq	.LC3(%rip), %rax
	movq	%rax, %rdi
	movl	$1, %eax
	call	printf@PLT
	call	clock@PLT
	movq	%rax, start(%rip)
	movq	$2, -8(%rbp)
	jmp	.L28
.L30:
	movq	-8(%rbp), %rax
	movq	%rax, %rdi
	call	isPrimeErato
	testl	%eax, %eax
	je	.L29
	movl	count_erato(%rip), %eax
	addl	$1, %eax
	movl	%eax, count_erato(%rip)
.L29:
	addq	$1, -8(%rbp)
.L28:
	movq	limite(%rip), %rax
	cmpq	-8(%rbp), %rax
	jnb	.L30
	call	clock@PLT
	movq	%rax, end(%rip)
	movq	end(%rip), %rdx
	movq	start(%rip), %rax
	subq	%rax, %rdx
	pxor	%xmm0, %xmm0
	cvtsi2sdq	%rdx, %xmm0
	movsd	.LC2(%rip), %xmm1
	divsd	%xmm1, %xmm0
	movsd	%xmm0, cpu_time_used(%rip)
	movq	cpu_time_used(%rip), %rcx
	movq	limite(%rip), %rdx
	movl	count_erato(%rip), %eax
	movq	%rcx, %xmm0
	movl	%eax, %esi
	leaq	.LC4(%rip), %rax
	movq	%rax, %rdi
	movl	$1, %eax
	call	printf@PLT
	movl	count_naive(%rip), %edx
	movl	count_erato(%rip), %eax
	cmpl	%eax, %edx
	jne	.L31
	movl	count_naive(%rip), %eax
	movl	%eax, %esi
	leaq	.LC5(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	jmp	.L32
.L31:
	leaq	.LC6(%rip), %rax
	movq	%rax, %rdi
	call	puts@PLT
.L32:
	movl	$0, %eax
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE8:
	.size	main, .-main
	.section	.rodata
	.align 8
.LC2:
	.long	0
	.long	1093567616
	.ident	"GCC: (GNU) 14.2.1 20250207"
	.section	.note.GNU-stack,"",@progbits

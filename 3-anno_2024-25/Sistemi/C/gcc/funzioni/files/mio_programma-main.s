	.file	"main.c"
	.text
	.section	.rodata
.LC1:
	.string	"v1 (tutti 1.0): "
.LC3:
	.string	"v1 + v2: "
.LC5:
	.string	"v1 + 3: "
.LC7:
	.string	"v1 * 4: "
.LC8:
	.string	"v1 - v2: "
	.align 8
.LC9:
	.string	"Prodotto scalare (v1 . v2): %lf\n"
.LC10:
	.string	"Concatenazione di v1 e v2: "
.LC11:
	.string	"v1_copy prima di reverse: "
.LC12:
	.string	"v1_copy dopo reverse: "
.LC14:
	.string	"v_unsorted prima di sort: "
.LC15:
	.string	"v_unsorted dopo sort: "
.LC16:
	.string	"v_shuffle prima di shuffle: "
.LC17:
	.string	"v_shuffle dopo shuffle: "
	.align 8
.LC18:
	.string	"v_rshft prima di right shift: "
	.align 8
.LC19:
	.string	"v_rshft dopo right shift di 2: "
.LC20:
	.string	"v_lshft prima di left shift: "
	.align 8
.LC21:
	.string	"v_lshft dopo left shift di 2: "
	.align 8
.LC22:
	.string	"v_rrot prima di right rotation: "
	.align 8
.LC23:
	.string	"v_rrot dopo right rotation di 2: "
	.align 8
.LC24:
	.string	"v_lrot prima di left rotation: "
	.align 8
.LC25:
	.string	"v_lrot dopo left rotation di 2: "
	.align 8
.LC26:
	.string	"Slice di v1_copy (dalla posizione 1 per 3 elementi): "
.LC27:
	.string	"Norma di v1: %lf\n"
.LC28:
	.string	"Media di v1: %lf\n"
.LC29:
	.string	"Minimo di v1: %lf\n"
.LC30:
	.string	"Massimo di v1: %lf\n"
.LC31:
	.string	"Somma di v1: %lf\n"
.LC33:
	.string	"true"
.LC34:
	.string	"false"
	.align 8
.LC35:
	.string	"v1 uguale a se stesso (tolleranza 0.0001): %s\n"
	.align 8
.LC36:
	.string	"v_map prima di map_vec (sqrt): "
.LC37:
	.string	"v_map dopo map_vec (sqrt): "
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
	subq	$864, %rsp
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	movq	.LC0(%rip), %rdx
	leaq	-768(%rbp), %rax
	movq	%rdx, %xmm0
	movl	$5, %esi
	movq	%rax, %rdi
	call	fill_vec@PLT
	leaq	.LC1(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-768(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	print_vec@PLT
	movq	.LC2(%rip), %rdx
	leaq	-720(%rbp), %rax
	movq	%rdx, %xmm0
	movl	$5, %esi
	movq	%rax, %rdi
	call	fill_vec@PLT
	leaq	-672(%rbp), %rdx
	leaq	-720(%rbp), %rsi
	leaq	-768(%rbp), %rax
	movl	$5, %ecx
	movq	%rax, %rdi
	call	add_vec@PLT
	leaq	.LC3(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-672(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	print_vec@PLT
	leaq	-624(%rbp), %rsi
	movq	.LC4(%rip), %rcx
	leaq	-768(%rbp), %rax
	movl	$5, %edx
	movq	%rcx, %xmm0
	movq	%rax, %rdi
	call	adds_vec@PLT
	leaq	.LC5(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-624(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	print_vec@PLT
	leaq	-576(%rbp), %rsi
	movq	.LC6(%rip), %rcx
	leaq	-768(%rbp), %rax
	movl	$5, %edx
	movq	%rcx, %xmm0
	movq	%rax, %rdi
	call	muls_vec@PLT
	leaq	.LC7(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-576(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	print_vec@PLT
	leaq	-528(%rbp), %rdx
	leaq	-720(%rbp), %rsi
	leaq	-768(%rbp), %rax
	movl	$5, %ecx
	movq	%rax, %rdi
	call	sub_vec@PLT
	leaq	.LC8(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-528(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	print_vec@PLT
	leaq	-720(%rbp), %rcx
	leaq	-768(%rbp), %rax
	movl	$5, %edx
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	dot_vec@PLT
	movq	%xmm0, %rax
	movq	%rax, -848(%rbp)
	movq	-848(%rbp), %rax
	movq	%rax, %xmm0
	leaq	.LC9(%rip), %rax
	movq	%rax, %rdi
	movl	$1, %eax
	call	printf@PLT
	leaq	-96(%rbp), %rcx
	leaq	-720(%rbp), %rdx
	leaq	-768(%rbp), %rax
	movq	%rcx, %r8
	movl	$5, %ecx
	movl	$5, %esi
	movq	%rax, %rdi
	call	concat_vec@PLT
	leaq	.LC10(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-96(%rbp), %rax
	movl	$10, %esi
	movq	%rax, %rdi
	call	print_vec@PLT
	movl	$0, -856(%rbp)
	jmp	.L2
.L3:
	pxor	%xmm1, %xmm1
	cvtsi2sdl	-856(%rbp), %xmm1
	movsd	.LC0(%rip), %xmm0
	addsd	%xmm1, %xmm0
	movl	-856(%rbp), %eax
	cltq
	movsd	%xmm0, -480(%rbp,%rax,8)
	addl	$1, -856(%rbp)
.L2:
	cmpl	$4, -856(%rbp)
	jle	.L3
	leaq	.LC11(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-480(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	print_vec@PLT
	leaq	-480(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	reverse_vec@PLT
	leaq	.LC12(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-480(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	print_vec@PLT
	movsd	.LC13(%rip), %xmm0
	movsd	%xmm0, -432(%rbp)
	movsd	.LC4(%rip), %xmm0
	movsd	%xmm0, -424(%rbp)
	movsd	.LC6(%rip), %xmm0
	movsd	%xmm0, -416(%rbp)
	movsd	.LC0(%rip), %xmm0
	movsd	%xmm0, -408(%rbp)
	movsd	.LC2(%rip), %xmm0
	movsd	%xmm0, -400(%rbp)
	leaq	.LC14(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-432(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	print_vec@PLT
	leaq	-432(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	sort_vec@PLT
	leaq	.LC15(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-432(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	print_vec@PLT
	movsd	.LC0(%rip), %xmm0
	movsd	%xmm0, -384(%rbp)
	movsd	.LC2(%rip), %xmm0
	movsd	%xmm0, -376(%rbp)
	movsd	.LC4(%rip), %xmm0
	movsd	%xmm0, -368(%rbp)
	movsd	.LC6(%rip), %xmm0
	movsd	%xmm0, -360(%rbp)
	movsd	.LC13(%rip), %xmm0
	movsd	%xmm0, -352(%rbp)
	leaq	.LC16(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-384(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	print_vec@PLT
	leaq	-384(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	shuffle_vec@PLT
	leaq	.LC17(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-384(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	print_vec@PLT
	movsd	.LC0(%rip), %xmm0
	movsd	%xmm0, -336(%rbp)
	movsd	.LC2(%rip), %xmm0
	movsd	%xmm0, -328(%rbp)
	movsd	.LC4(%rip), %xmm0
	movsd	%xmm0, -320(%rbp)
	movsd	.LC6(%rip), %xmm0
	movsd	%xmm0, -312(%rbp)
	movsd	.LC13(%rip), %xmm0
	movsd	%xmm0, -304(%rbp)
	leaq	.LC18(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-336(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	print_vec@PLT
	leaq	-336(%rbp), %rax
	movl	$5, %edx
	movl	$2, %esi
	movq	%rax, %rdi
	call	rshft_vec@PLT
	leaq	.LC19(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-336(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	print_vec@PLT
	movsd	.LC0(%rip), %xmm0
	movsd	%xmm0, -288(%rbp)
	movsd	.LC2(%rip), %xmm0
	movsd	%xmm0, -280(%rbp)
	movsd	.LC4(%rip), %xmm0
	movsd	%xmm0, -272(%rbp)
	movsd	.LC6(%rip), %xmm0
	movsd	%xmm0, -264(%rbp)
	movsd	.LC13(%rip), %xmm0
	movsd	%xmm0, -256(%rbp)
	leaq	.LC20(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-288(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	print_vec@PLT
	leaq	-288(%rbp), %rax
	movl	$5, %edx
	movl	$2, %esi
	movq	%rax, %rdi
	call	lshft_vec@PLT
	leaq	.LC21(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-288(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	print_vec@PLT
	movsd	.LC0(%rip), %xmm0
	movsd	%xmm0, -240(%rbp)
	movsd	.LC2(%rip), %xmm0
	movsd	%xmm0, -232(%rbp)
	movsd	.LC4(%rip), %xmm0
	movsd	%xmm0, -224(%rbp)
	movsd	.LC6(%rip), %xmm0
	movsd	%xmm0, -216(%rbp)
	movsd	.LC13(%rip), %xmm0
	movsd	%xmm0, -208(%rbp)
	leaq	.LC22(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-240(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	print_vec@PLT
	leaq	-240(%rbp), %rax
	movl	$5, %edx
	movl	$2, %esi
	movq	%rax, %rdi
	call	rrot_vec@PLT
	leaq	.LC23(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-240(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	print_vec@PLT
	movsd	.LC0(%rip), %xmm0
	movsd	%xmm0, -192(%rbp)
	movsd	.LC2(%rip), %xmm0
	movsd	%xmm0, -184(%rbp)
	movsd	.LC4(%rip), %xmm0
	movsd	%xmm0, -176(%rbp)
	movsd	.LC6(%rip), %xmm0
	movsd	%xmm0, -168(%rbp)
	movsd	.LC13(%rip), %xmm0
	movsd	%xmm0, -160(%rbp)
	leaq	.LC24(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-192(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	print_vec@PLT
	leaq	-192(%rbp), %rax
	movl	$5, %edx
	movl	$2, %esi
	movq	%rax, %rdi
	call	lrot_vec@PLT
	leaq	.LC25(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-192(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	print_vec@PLT
	leaq	-800(%rbp), %rsi
	leaq	-480(%rbp), %rax
	movl	$3, %ecx
	movl	$1, %edx
	movq	%rax, %rdi
	call	slice_vec@PLT
	leaq	.LC26(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-800(%rbp), %rax
	movl	$3, %esi
	movq	%rax, %rdi
	call	print_vec@PLT
	leaq	-768(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	norm_vec@PLT
	movq	%xmm0, %rax
	movq	%rax, -840(%rbp)
	movq	-840(%rbp), %rax
	movq	%rax, %xmm0
	leaq	.LC27(%rip), %rax
	movq	%rax, %rdi
	movl	$1, %eax
	call	printf@PLT
	leaq	-768(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	mean_vec@PLT
	movq	%xmm0, %rax
	movq	%rax, -832(%rbp)
	movq	-832(%rbp), %rax
	movq	%rax, %xmm0
	leaq	.LC28(%rip), %rax
	movq	%rax, %rdi
	movl	$1, %eax
	call	printf@PLT
	leaq	-768(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	min_vec@PLT
	movq	%xmm0, %rax
	movq	%rax, -824(%rbp)
	movq	-824(%rbp), %rax
	movq	%rax, %xmm0
	leaq	.LC29(%rip), %rax
	movq	%rax, %rdi
	movl	$1, %eax
	call	printf@PLT
	leaq	-768(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	max_vec@PLT
	movq	%xmm0, %rax
	movq	%rax, -816(%rbp)
	movq	-816(%rbp), %rax
	movq	%rax, %xmm0
	leaq	.LC30(%rip), %rax
	movq	%rax, %rdi
	movl	$1, %eax
	call	printf@PLT
	leaq	-768(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	sum_vec@PLT
	movq	%xmm0, %rax
	movq	%rax, -808(%rbp)
	movq	-808(%rbp), %rax
	movq	%rax, %xmm0
	leaq	.LC31(%rip), %rax
	movq	%rax, %rdi
	movl	$1, %eax
	call	printf@PLT
	movq	.LC32(%rip), %rdx
	leaq	-768(%rbp), %rcx
	leaq	-768(%rbp), %rax
	movq	%rdx, %xmm0
	movl	$5, %edx
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	eq_vec@PLT
	movb	%al, -857(%rbp)
	cmpb	$0, -857(%rbp)
	je	.L4
	leaq	.LC33(%rip), %rax
	jmp	.L5
.L4:
	leaq	.LC34(%rip), %rax
.L5:
	movq	%rax, %rsi
	leaq	.LC35(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	$0, -852(%rbp)
	jmp	.L6
.L7:
	movl	-852(%rbp), %eax
	cltq
	movsd	-720(%rbp,%rax,8), %xmm1
	movl	-852(%rbp), %eax
	addl	$1, %eax
	pxor	%xmm0, %xmm0
	cvtsi2sdl	%eax, %xmm0
	mulsd	%xmm1, %xmm0
	movl	-852(%rbp), %eax
	cltq
	movsd	%xmm0, -144(%rbp,%rax,8)
	addl	$1, -852(%rbp)
.L6:
	cmpl	$4, -852(%rbp)
	jle	.L7
	leaq	.LC36(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-144(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	print_vec@PLT
	leaq	-144(%rbp), %rax
	movq	sqrt@GOTPCREL(%rip), %rdx
	movl	$5, %esi
	movq	%rax, %rdi
	call	map_vec@PLT
	leaq	.LC37(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-144(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	print_vec@PLT
	movl	$0, %eax
	movq	-8(%rbp), %rdx
	subq	%fs:40, %rdx
	je	.L9
	call	__stack_chk_fail@PLT
.L9:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	main, .-main
	.section	.rodata
	.align 8
.LC0:
	.long	0
	.long	1072693248
	.align 8
.LC2:
	.long	0
	.long	1073741824
	.align 8
.LC4:
	.long	0
	.long	1074266112
	.align 8
.LC6:
	.long	0
	.long	1074790400
	.align 8
.LC13:
	.long	0
	.long	1075052544
	.align 8
.LC32:
	.long	-350469331
	.long	1058682594
	.ident	"GCC: (GNU) 14.2.1 20250207"
	.section	.note.GNU-stack,"",@progbits

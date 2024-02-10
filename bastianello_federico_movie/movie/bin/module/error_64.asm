
section .bss


section .data

	msg_error db "errore durante l'esecuzione del programma", 0
	len_msg equ $ - msg_error


section .text
	global _start


%macro GXOR 0
	xor rax, rax
	xor rbx, rbx
	xor rcx, rcx
	xor rdx, rdx
%endmacro


_start:	GXOR

	push len_msg
	push msg_error
	call main

	mov rdi, rax		; stato di uscita dalla funzione main

_exit:	mov rax, 60
	syscall 


main:	push rbp
	mov rbp, rsp

	mov rsi, [rbp + 16]
	mov rdx, [rbp + 24]	
	mov rdi, 1
	mov rax, 1
	syscall

	mov rax, 0
	mov rsp, rbp
	pop rbp
	ret



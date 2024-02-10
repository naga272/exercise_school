section .data
	msg db "errore durante l'esecuzione del programma", 0
	len equ $ - msg

section .bss


section .text
	global _start

%macro GXOR 0
	xor eax, eax
	xor ebx, ebx
	xor edx, edx
	xor ecx, ecx
%endmacro


_start: GXOR

	push len
	push msg
	call main

	mov ebx, eax

_exit:	mov eax, 1
	int 80h


main:	push 	ebp
	mov 	ebp, esp

	mov 	eax, 4
	mov 	edi, 1
	mov 	ecx, [ebp + 8]
	mov 	edx, [ebp + 12]
	int 80h


	mov eax, 1

	mov esp, ebp
	pop ebp
	ret


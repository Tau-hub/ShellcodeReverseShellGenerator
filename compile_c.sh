#!/bin/bash
gcc shellcode.c -o exec_shellcode -fno-stack-protector -z execstack -no-pie -m32 
chmod +x exec_shellcode
./exec_shellcode

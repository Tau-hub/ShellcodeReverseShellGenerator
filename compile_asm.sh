#!/bin/bash
set -u
file=$1
object=$(ls $file | sed "s/\.s/\.o/")
nasm -f elf32  $file && ld -m elf_i386 $object
rm $object 

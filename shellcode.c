#include <stdio.h>
#include <string.h>
#include <sys/mman.h>


	const char code[] = 
   "";
int main(){
  int r =  mprotect((void *)((int)code & ~4095),  4096, PROT_READ | PROT_WRITE|PROT_EXEC); 
  int (*ret)() = (int(*)())code;
  return ret();
}
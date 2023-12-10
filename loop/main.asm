SECTION "asdf", ROM0
LOAD "code", WRAMX[$d322]
inc a
loop:
	jp loop

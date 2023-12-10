SECTION "asdf", ROM0
LOAD "code", WRAMX[$d322]
ld hl, homestuck
call PrintText
ret
nop
homestuck:
	text "homestuck.com"
	prompt
	text_end

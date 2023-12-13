; jumps to box data for larger programs
SECTION "asdf", ROM0
LOAD "code", WRAMX[wBagItems+4]

call wBoxDataStart+1
ret



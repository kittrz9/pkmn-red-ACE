; a few items shorter than this other ram writer
; https://glitchcity.wiki/wiki/Reusable_RAM_writer
;
; also has no duplicate item stacks, most of
; the items can be found in the celadon store
;
; you have to input the data backwards though,
; since it not incrementing the high byte of
; the address itself would mean you'd need to
; increase that item's count by 1, which would
; be more of a hassle than just having to
; write it backwards
;
; you are expected to toss 1 item from addressHigh
; (4th item in bag, 2nd item in this code)
; when the low byte underflows
;
; Lemonade x(value)
; Carbos x(high byte)
; X Accuracy x(low byte)
; PP Up x33
; Calcium x211
; Revive x46
; HP Up x175
; Water Stone x201


SECTION "asdf", ROM0
LOAD "code", WRAMX[wBagItems+4]

; change this when assembling to your desired address
; it's just set to the player name to test it
DEF modifiedAddr = wPlayerName+6

value:
ld a, $00
addressHigh:
ld h, HIGH(modifiedAddr)
addressLow:
ld l, LOW(modifiedAddr)
ld [hld], a ; hld to get a non-glitch item
ld hl, addressLow+1
dec [hl]
ld l, LOW(value+1)
xor a, a ; set a to 0 since value is probably changed
ld [hli], a
ret

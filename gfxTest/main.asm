SECTION "asdf", ROM0
LOAD "code", WRAMX[wBoxDataStart+1]


loop:
ld hl, wTileMap
ld c, 19
resetStr:
ld de, string
ld b, stringEnd-string
dec c
jp z, screenDone
nextChar:
ld a, [de]
ld [hli], a
halt
inc de
dec b
jp z, resetStr
jp nextChar
screenDone:
ld bc, $1214
ld hl, wTileMap
call ClearScreenArea
jp loop

string:
	db "fortnite battle pass"
stringEnd:


SECTION "asdf", ROM0
ld a, $ff ; $ff mutes, anything else changes the music or plays a sound effect
call PlaySound ; PlaySound https://github.com/pret/pokered/blob/437ab7a9404f6027ec9adb2cefc56abe74aa4f0e/pokered.sym#L568
ret

# pokemon red ACE stuff

just stuff to assemble programs for pokemon gen 1 arbitrary code execution<br><br>

I think this stuff would probably also be useful with gen 2 if you know what you're doing, but I never played gen 2 lmao<br><br>

you *must* have [rgbds](https://github.com/gbdev/rgbds) installed to be able to assemble your code<br><br>

## usage

clone this repo along with the disassembly submodule<br>
```sh
git clone (this repos url)
git submodule update --init
```

make a folder and put in a file named `main.asm` to put your assembly code in<br>

all the included stuff in [the disassembly](https://github.com/pret/pokered/tree/master) is also included to allow for easier stuff (like having text macros)<br>

your file should start with something like this to have your starting point correct (the ROM0 thing is only there so the assembler doesn't scream about having code in ram)<br>

```
SECTION "asdf", ROM0
LOAD "code", WRAMX[$d322]
```

then run the `assemble.sh` script like this, replacing `$PRG_NAME` with your folder's name<br>

```sh
./assemble.sh $PRG_NAME
```

your program should then be assembled into a file with the name `$PRG_NAME.prg` in that folder.<br>

you should use whatever hex editor you prefer (such as `xxd` on linux) to view your program.<br>

to convert your program into items, you need to get a list of all 255 items in the game separated by commas and put it into a file named `itemList.txt`<br>
then you should just be able to run `prgToItems.py` like this, once again replacing `$PRG_NAME` with your folder's name<br>
```sh
./prgToItems.py $PRG_NAME
```

I'm not sure if I should put the `itemList.txt` file in this repo since it's taken from <https://glitchcity.wiki/wiki/The_Big_HEX_List> which says "This list is for use on Glitch City Laboratories ONLY."<br>

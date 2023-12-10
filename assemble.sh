#!/bin/sh

ASM_FLAGS="-I pokered/ -P ../includes.asm"


PRG_NAME=$1

if [ -z "$(command -v rgbasm)" ]; then
	echo "rgbasm not installed"
	exit 1
fi

# probably unnecessary but whatever
if [ -z "$(command -v rgblink)" ]; then
	echo "rgblink not installed"
	exit 1
fi

if [ -z "$PRG_NAME" ]; then
	echo "no program name"
	exit 1
fi

if [ ! -f "$PRG_NAME"/main.asm ]; then
	echo "$PRG_NAME/main.asm not found"
	exit 1
fi

#cd "$PRG_NAME" || exit 1

rgbasm $ASM_FLAGS $PRG_NAME/main.asm -o $PRG_NAME/main.o
rgblink -x $PRG_NAME/main.o -o $PRG_NAME/"$PRG_NAME".prg

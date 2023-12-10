#!/bin/sh


PRG_NAME=$1

if [ -z "$PRG_NAME" ]; then
	echo "no program name"
	exit 1
fi

cd "$PRG_NAME" || exit 1

rm main.o "$PRG_NAME".prg


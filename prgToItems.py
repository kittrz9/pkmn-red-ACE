#!/bin/env python3

import sys
import os

# itemList.txt taken from https://glitchcity.wiki/wiki/The_Big_HEX_List
# idk if I am supposed to be able to do stuff like this
# due to the "This list is for use on Glitch City Laboratories ONLY." notice

def main():
	if len(sys.argv) != 2:
		print(f"usage:\n\t {sys.argv[0]} program")
		exit(1)

	if not os.path.exists("./itemList.txt"):
		print("could not find itemList.txt\nthe list is from https://glitchcity.wiki/wiki/The_Big_HEX_List\nI'm not sure if I should include the list itself due to the \"This list is for use on Glitch City Laboratories ONLY.\" line on the page.")
		exit(1)

	itemList = open("itemList.txt", "r")
	items = itemList.read().split(',')

	prgName = sys.argv[1]

	if os.path.isdir(prgName):
		inFile = open(prgName + "/" + prgName + ".prg", "rb")
	elif os.path.isfile(prgName):
		inFile = open(prgName, "rb")

	inBytes = inFile.read()
	#print(inBytes.hex())
	for i in range(0, len(inBytes)):
		b = inBytes[i]
		if i%2 == 0:
			print(items[b], end=" x")
		else:
			print(b)

	if len(inBytes)%2 == 1:
		print("Any")


	#print(lines);

if __name__ == "__main__":
	main()

#!/bin/env python3

import sys
import os


def generateItemList():
	charmap = {}

	with open("pokered/constants/charmap.asm", "r") as f:
		lines = f.readlines()
		for l in lines:
			if l.lstrip().startswith("charmap"):
				i = l.find("charmap") + len("charmap")
				while l[i] != "\"":
					i += 1
				i += 1
				str = ""
				while l[i] != "\"":
					str += l[i]
					i += 1
				#print(str)
				while not l[i].isalnum():
					i += 1
				byte = ""
				while l[i].isalnum():
					byte += l[i]
					i += 1
				byte = int(byte, 16)
				#print(byte)
				if not byte in charmap:
					charmap[byte] = str
				#charmap.append((str, byte))
				#print(l.strip())
		f.close()

	charmap[0x54] = "POKe"
	#print(charmap)

	items = [""] * 256
	with open("pokered/pokered.gbc", "rb") as f:
		f.seek(0x472b, os.SEEK_SET);
		#items = [""] * 256
		count = 0
		str = ""
		while count < 256:
			byte = int.from_bytes(f.read(1))
			if(byte == 0x50):
				id = count+1
				if id == 0xFF:
					str = "CANCEL"
				elif id > 0xC3 and id < 0xFF:
					str = ""
					number = 0
					if count > 0xC8:
						str += "T"
						number = count - 0xC8
					else:
						str += "H"
						number = count - 0xC3
					str += "M{:02d}".format(number)

				items[id % 256] = str
				#print("{}: {}".format(hex(count), str[0:32]))
				count += 1
				str = ""
				continue
			if(not byte in charmap):
				str += "#"
				continue
			str += charmap[byte]

		#for i, itemName in enumerate(items):
			#print("{},".format(itemName[0:16]), end='')
			#print("{}: {}".format(hex(i), itemName[0:16]))

		f.close()
	return items

def main():
	if len(sys.argv) != 2:
		print(f"usage:\n\t {sys.argv[0]} program")
		exit(1)

	items = [""] * 256
	# it probably doesn't matter at all if it just generates the whole list every time
	# but idk it just seems like a bad idea to do it like that lmao
	if not os.path.exists("itemList.txt"):
		items = generateItemList()
		with open("itemList.txt", "w") as f:
			for i, itemName in enumerate(items):
				f.write("{},".format(itemName[0:16]))
			f.close()
	else:
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

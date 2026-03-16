import os
import random


#SAVCheckSum:
#;Check Sum (result[1 byte] is complemented)
#	ld d, 0
#.loop
#	ld a, [hli]
#	add d
#	ld d, a
#	dec bc
#	ld a, b
#	or c
#	jr nz, .loop
#	ld a, d
#	cpl
#	ret

def checksum(data):
	sum = 0
	for b in data:
		sum += b
		sum &= 0xff
	sum = ~sum & 0xff
	return sum

itemsProgram = None
with open("box/box.prg", "rb") as f:
	itemsProgram = f.read()
	f.close()

boxProgram = None
with open("gfxTest/gfxTest.prg", "rb") as f:
	boxProgram = f.read()
	f.close()

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
				charmap[str] = byte
			#charmap.append((str, byte))
			#print(l.strip())
	f.close()

def strToPkmnChars(str):
	newStr = bytes(0)
	for c in str:
		newStr += charmap[c].to_bytes()
	return newStr

#print(strToPkmnChars("TEST!"))

bank0 = bytearray(bytes(0x2000)) # sprite buffer and hall of fame data
bank1 = bytearray(bytes(0x2000)) # game data
bank2 = bytearray(bytes(0x2000)) # box 1-6
bank3 = bytearray(bytes(0x2000)) # box 7-12

# name
#bank1[0x0598:0x05A2] = strToPkmnChars("kittrz") + b'\x50'
# for some reason using the slice notation stuff makes the array shorter????
playerName = strToPkmnChars("kittrz") + b'\x50'
for i, c in enumerate(playerName):
	bank1[0x598 + i] = c
# main data
wramMainData = 0xd2f7
sramMainData = 0x5a3
mainDataIndex = 0x05A3

def wramToSram(addr):
	return addr - wramMainData + sramMainData

#InitPlayerData:
#InitPlayerData2:
#
#	call Random
#	ldh a, [hRandomSub]
#	ld [wPlayerID], a
#
#	call Random
#	ldh a, [hRandomAdd]
#	ld [wPlayerID + 1], a
#
mainDataIndex = wramToSram(0xd359)
bank1[mainDataIndex] = random.randbytes(1)[0]
mainDataIndex += 1
bank1[mainDataIndex] = random.randbytes(1)[0]


#$d31d = wNumBagItems
#$d31d = wPokedexSeenEnd
mainDataIndex = wramToSram(0xd31d)
bank1[mainDataIndex] = 20
mainDataIndex += 1
#$d31e = wBagItems
for i in range(0, 20):
	# 256 master balls by default
	bank1[mainDataIndex+i*2] = 1
	bank1[mainDataIndex+i*2+1] = 0
bank1[mainDataIndex+0] = 0x5D # 8F
bank1[mainDataIndex+1] = 0x01 # x1
for i, b in enumerate(itemsProgram):
	bank1[mainDataIndex+i+4] = b

#$d347 = wPlayerMoney
mainDataIndex = wramToSram(0xd347)
bank1[mainDataIndex] = 0xFF
bank1[mainDataIndex+1] = 0xFF
#$d34a = wRivalName
#bank1[mainDataIndex:mainDataIndex+(0x355-0x34a)] = strToPkmnChars("asdf")+b'\x50'
mainDataIndex = wramToSram(0xd34a)
rivalName = strToPkmnChars("asdf")+b'\x50'
for i, c in enumerate(rivalName):
	bank1[mainDataIndex + i] = c
#$d356 = wObtainedBadges
mainDataIndex = wramToSram(0xd356)
bank1[mainDataIndex] = 0x00
#$d358 = wLetterPrintingDelayFlags
mainDataIndex = wramToSram(0xd358)
bank1[mainDataIndex] = 1
#$d35b = wMapMusicSoundID
mainDataIndex = wramToSram(0xd35b)
bank1[mainDataIndex] = 0xBA
mainDataIndex += 1
#$d35c = wMapMusicROMBank
mainDataIndex = wramToSram(0xd35c)
bank1[mainDataIndex] = 0x2
mainDataIndex += 1
#$d35d = wMapPalOffset
mainDataIndex = wramToSram(0xd35d)
mainDataIndex += 1
#$d35e = wCurMap
mainDataIndex = wramToSram(0xd35e)
bank1[mainDataIndex] = 0x26
mainDataIndex += 1
#$d35f = wCurrentTileBlockMapViewPointer
mainDataIndex = wramToSram(0xd35f)
bank1[mainDataIndex] = 0x12
mainDataIndex += 1
bank1[mainDataIndex] = 0xC7
mainDataIndex += 1
#$d361 = wYCoord
mainDataIndex = wramToSram(0xd361)
bank1[mainDataIndex] = 0x06
mainDataIndex += 1
#$d362 = wXCoord
mainDataIndex = wramToSram(0xd362)
bank1[mainDataIndex] = 0x03
mainDataIndex += 1
#$d363 = wYBlockCoord
mainDataIndex = wramToSram(0xd363)
bank1[mainDataIndex] = 0x00
mainDataIndex += 1
#$d364 = wXBlockCoord
mainDataIndex = wramToSram(0xd364)
bank1[mainDataIndex] = 0x01
mainDataIndex += 1
#$d365 = wLastMap
mainDataIndex += 1
#$d366 = wUnusedD366
mainDataIndex += 1


# copying this data from what it is at the start of the game for now
# hopefully I'll have these be able to be changed to whatever once I figure out how all this works
#$d367 = wCurMapHeader
#$d367 = wCurMapTileset
mainDataIndex = wramToSram(0xd367)
bank1[mainDataIndex] = 4
mainDataIndex += 1
#$d368 = wCurMapHeight
mainDataIndex = wramToSram(0xd368)
bank1[mainDataIndex] = 4
mainDataIndex += 1
#$d369 = wCurMapWidth
mainDataIndex = wramToSram(0xd369)
bank1[mainDataIndex] = 4
mainDataIndex += 1
#$d36a = wCurMapDataPtr
mainDataIndex = wramToSram(0xd36a)
bank1[mainDataIndex] = 0x10
mainDataIndex += 1
bank1[mainDataIndex] = 0x40
mainDataIndex += 1
#$d36c = wCurMapTextPtr
mainDataIndex = wramToSram(0xd36c)
bank1[mainDataIndex] = 0xCF
mainDataIndex += 1
bank1[mainDataIndex] = 0x40
mainDataIndex += 1
#$d36e = wCurMapScriptPtr
mainDataIndex = wramToSram(0xd36e)
bank1[mainDataIndex] = 0xB0
mainDataIndex += 1
bank1[mainDataIndex] = 0x40
mainDataIndex += 1
#$d370 = wCurMapConnections
mainDataIndex += 1
#$d371 = wNorthConnectedMap
#$d371 = wCurMapHeaderEnd
#$d371 = wNorthConnectionHeader
mainDataIndex = wramToSram(0xd371)
bank1[mainDataIndex] = 0xFF
mainDataIndex += 1
#$d372 = wNorthConnectionStripSrc
#$d374 = wNorthConnectionStripDest
#$d376 = wNorthConnectionStripLength
#$d377 = wNorthConnectedMapWidth
#$d378 = wNorthConnectedMapYAlignment
#$d379 = wNorthConnectedMapXAlignment
#$d37a = wNorthConnectedMapViewPointer
#$d37c = wSouthConnectionHeader
#$d37c = wSouthConnectedMap
mainDataIndex = wramToSram(0xd37c)
bank1[mainDataIndex] = 0xFF
mainDataIndex += 1
#$d37d = wSouthConnectionStripSrc
#$d37f = wSouthConnectionStripDest
#$d381 = wSouthConnectionStripLength
#$d382 = wSouthConnectedMapWidth
#$d383 = wSouthConnectedMapYAlignment
#$d384 = wSouthConnectedMapXAlignment
#$d385 = wSouthConnectedMapViewPointer
#$d387 = wWestConnectedMap
#$d387 = wWestConnectionHeader
mainDataIndex = wramToSram(0xd387)
bank1[mainDataIndex] = 0xFF
mainDataIndex += 1
#$d388 = wWestConnectionStripSrc
#$d38a = wWestConnectionStripDest
#$d38c = wWestConnectionStripLength
#$d38d = wWestConnectedMapWidth
#$d38e = wWestConnectedMapYAlignment
#$d38f = wWestConnectedMapXAlignment
#$d390 = wWestConnectedMapViewPointer
#$d392 = wEastConnectionHeader
#$d392 = wEastConnectedMap
mainDataIndex = 0xd392 - wramMainData + sramMainData
mainDataIndex = wramToSram(0xd392)
bank1[mainDataIndex] = 0xFF
mainDataIndex += 1
#$d393 = wEastConnectionStripSrc
#$d395 = wEastConnectionStripDest
#$d397 = wEastConnectionStripLength
#$d398 = wEastConnectedMapWidth
#$d399 = wEastConnectedMapYAlignment
#$d39a = wEastConnectedMapXAlignment
#$d39b = wEastConnectedMapViewPointer
#$d39d = wSpriteSet
#$d3a8 = wSpriteSetID
#$d3a9 = wObjectDataPointerTemp
mainDataIndex = 0xd3a9 - wramMainData + sramMainData
mainDataIndex = wramToSram(0xd3a9)
bank1[mainDataIndex] = 0xd0
bank1[mainDataIndex+1] = 0x40
mainDataIndex += 0xd3ad-0xd3a9
#$d3ad = wMapBackgroundTile
mainDataIndex = wramToSram(0xd3ad)
bank1[mainDataIndex] = 0x0A
mainDataIndex += 1
#$d3ae = wNumberOfWarps
mainDataIndex = wramToSram(0xd3ae)
bank1[mainDataIndex] = 1
mainDataIndex += 1
#$d3af = wWarpEntries
mainDataIndex = wramToSram(0xd3af)
bank1[mainDataIndex] = 1
mainDataIndex += 1
bank1[mainDataIndex] = 7
mainDataIndex += 1
bank1[mainDataIndex] = 2
mainDataIndex += 1
bank1[mainDataIndex] = 0x25
mainDataIndex += 1
#$d42f = wDestinationWarpID
mainDataIndex = wramToSram(0xd42f)
bank1[mainDataIndex] = 0xFF
#$d4b0 = wNumSigns
#$d4b1 = wSignCoords
#$d4d1 = wSignTextIDs
#$d4e1 = wNumSprites
#$d4e2 = wYOffsetSinceLastSpecialWarp
#$d4e3 = wXOffsetSinceLastSpecialWarp
#$d4e4 = wMapSpriteData
#$d504 = wMapSpriteExtraData
#$d524 = wCurrentMapHeight2
mainDataIndex = wramToSram(0xd524)
bank1[mainDataIndex] = 0x08
mainDataIndex += 1
bank1[mainDataIndex] = 0x08
mainDataIndex += 1
bank1[mainDataIndex] = 0x00
mainDataIndex += 1
bank1[mainDataIndex] = 0x98
mainDataIndex += 1
bank1[mainDataIndex] = 0x00
mainDataIndex += 1
bank1[mainDataIndex] = 0x08
mainDataIndex += 1
bank1[mainDataIndex] = 0x00
mainDataIndex += 1
bank1[mainDataIndex] = 0x19
mainDataIndex += 1
bank1[mainDataIndex] = 0x70
mainDataIndex += 1
bank1[mainDataIndex] = 0x52
mainDataIndex += 1
bank1[mainDataIndex] = 0xE0
mainDataIndex += 1
bank1[mainDataIndex] = 0x4D
mainDataIndex += 1
bank1[mainDataIndex] = 0x49
mainDataIndex += 1
bank1[mainDataIndex] = 0x17
mainDataIndex += 1
bank1[mainDataIndex] = 0xFF
mainDataIndex += 1
bank1[mainDataIndex] = 0xFF
mainDataIndex += 1
bank1[mainDataIndex] = 0xFF
mainDataIndex += 1
bank1[mainDataIndex] = 0xFF
mainDataIndex += 1
#$d525 = wCurrentMapWidth2
#$d526 = wMapViewVRAMPointer
#$d528 = wPlayerMovingDirection
#$d529 = wPlayerLastStopDirection
#$d52a = wPlayerDirection
#$d52b = wTilesetBank
#$d52c = wTilesetBlocksPtr
#$d52e = wTilesetGfxPtr
#$d530 = wTilesetCollisionPtr
#$d532 = wTilesetTalkingOverTiles
#$d535 = wGrassTile
#$d53a = wNumBoxItems
mainDataIndex = 0xd53a - wramMainData + sramMainData
bank1[mainDataIndex] = 1
mainDataIndex += 1
#$d53b = wBoxItems
bank1[mainDataIndex] = 0x14
mainDataIndex += 1
bank1[mainDataIndex] = 1
mainDataIndex += 1
bank1[mainDataIndex] = 0xff
mainDataIndex += 1
#$d5a0 = wCurrentBoxNum
mainDataIndex = 0xd5a0 - wramMainData + sramMainData
bank1[mainDataIndex] = 1
#$d5a2 = wNumHoFTeams
#$d5a3 = wUnusedD5A3
#$d5a4 = wPlayerCoins
#$d5a6 = wMissableObjectFlags
mainDataIndex = 0xd5a6 - wramMainData + sramMainData
bank1[mainDataIndex] = 0xa5
mainDataIndex += 1
bank1[mainDataIndex] = 0x00
mainDataIndex += 1
bank1[mainDataIndex] = 0x7e
mainDataIndex += 1
bank1[mainDataIndex] = 0x01
mainDataIndex += 1
bank1[mainDataIndex] = 0x0c
mainDataIndex += 1
bank1[mainDataIndex] = 0x41
mainDataIndex += 1
bank1[mainDataIndex] = 0x02
mainDataIndex += 1
bank1[mainDataIndex] = 0x00
mainDataIndex += 1
bank1[mainDataIndex] = 0x10
mainDataIndex += 1
bank1[mainDataIndex] = 0x10
mainDataIndex += 1
bank1[mainDataIndex] = 0x00
mainDataIndex += 1
bank1[mainDataIndex] = 0x00
mainDataIndex += 1
bank1[mainDataIndex] = 0x0c
mainDataIndex += 1
bank1[mainDataIndex] = 0x00
mainDataIndex += 1
bank1[mainDataIndex] = 0x02
mainDataIndex += 1
bank1[mainDataIndex] = 0x00
mainDataIndex += 1
bank1[mainDataIndex] = 0x80
mainDataIndex += 1
bank1[mainDataIndex] = 0x01
mainDataIndex += 1
bank1[mainDataIndex] = 0x00
mainDataIndex += 1
bank1[mainDataIndex] = 0x00
mainDataIndex += 1
bank1[mainDataIndex] = 0x00
mainDataIndex += 1
bank1[mainDataIndex] = 0x00
mainDataIndex += 1
bank1[mainDataIndex] = 0x00
mainDataIndex += 1
bank1[mainDataIndex] = 0x00
mainDataIndex += 1
bank1[mainDataIndex] = 0x00
mainDataIndex += 1
bank1[mainDataIndex] = 0x00
mainDataIndex += 1
bank1[mainDataIndex] = 0x40
mainDataIndex += 1
bank1[mainDataIndex] = 0x9e
mainDataIndex += 1
bank1[mainDataIndex] = 0x07
mainDataIndex += 1
#$d5c6 = wMissableObjectFlagsEnd

# d163 is where 8f jumps to (start of the party data)
# https://glitchcity.wiki/wiki/ItemDex/RB:093#Older_setups
# party data in sram is at f2c
mainDataIndex = 0xf2c
prg = [ 0x03, 0xc3, 0x22, 0xd3, 0xff]
for i, b in enumerate(prg):
	bank1[mainDataIndex + i] = b

# hp
mainDataIndex = 0xf2c + 9
bank1[mainDataIndex] = 1
mainDataIndex = 0xf2c + 42
bank1[mainDataIndex] = 1

for i, b in enumerate(boxProgram):
	bank1[0x10c1 + i] = b

bank1[0x1523] = checksum(bank1[0x598:0x1523])


with open("test.sav", "wb") as f:
	print(hex(f.write(bank0)))
	print(hex(f.write(bank1)))
	print(hex(f.write(bank2)))
	print(hex(f.write(bank3)))

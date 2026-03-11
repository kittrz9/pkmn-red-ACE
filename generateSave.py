import os


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
#$d2f7 = wMainDataStart
#$d2f7 = wPokedexOwned
#$d30a = wPokedexOwnedEnd
#leaving this empty
mainDataIndex += 0xd30a-0xd2f7

#$d30a = wPokedexSeen
#leaving this empty
mainDataIndex += 0xd31d-0xd30a

#$d31d = wNumBagItems
#$d31d = wPokedexSeenEnd
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
mainDataIndex += 20*2

#$d347 = wPlayerMoney
bank1[mainDataIndex] = 0xFF
bank1[mainDataIndex+1] = 0xFF
mainDataIndex += 2
#$d34a = wRivalName
#bank1[mainDataIndex:mainDataIndex+(0x355-0x34a)] = strToPkmnChars("asdf")+b'\x50'
rivalName = strToPkmnChars("asdf")+b'\x50'
for i, c in enumerate(rivalName):
	bank1[mainDataIndex + i] = c
#$d355 = wOptions
mainDataIndex = 0xd355 - wramMainData + sramMainData
mainDataIndex += 1
#$d356 = wObtainedBadges
bank1[mainDataIndex] = 0x00
mainDataIndex += 2
#$d358 = wLetterPrintingDelayFlags
bank1[mainDataIndex] = 1
mainDataIndex += 1
#$d359 = wPlayerID
mainDataIndex += 2
#$d35b = wMapMusicSoundID
bank1[mainDataIndex] = 0xBA
mainDataIndex += 1
#$d35c = wMapMusicROMBank
bank1[mainDataIndex] = 0x2
mainDataIndex += 1
#$d35d = wMapPalOffset
mainDataIndex += 1
#$d35e = wCurMap
bank1[mainDataIndex] = 0x26
mainDataIndex += 1
#$d35f = wCurrentTileBlockMapViewPointer
bank1[mainDataIndex] = 0x12
mainDataIndex += 1
bank1[mainDataIndex] = 0xC7
mainDataIndex += 1
#$d361 = wYCoord
bank1[mainDataIndex] = 0x06
mainDataIndex += 1
#$d362 = wXCoord
bank1[mainDataIndex] = 0x03
mainDataIndex += 1
#$d363 = wYBlockCoord
bank1[mainDataIndex] = 0x00
mainDataIndex += 1
#$d364 = wXBlockCoord
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
bank1[mainDataIndex] = 4
mainDataIndex += 1
#$d368 = wCurMapHeight
bank1[mainDataIndex] = 4
mainDataIndex += 1
#$d369 = wCurMapWidth
bank1[mainDataIndex] = 4
mainDataIndex += 1
#$d36a = wCurMapDataPtr
bank1[mainDataIndex] = 0x10
mainDataIndex += 1
bank1[mainDataIndex] = 0x40
mainDataIndex += 1
#$d36c = wCurMapTextPtr
bank1[mainDataIndex] = 0xCF
mainDataIndex += 1
bank1[mainDataIndex] = 0x40
mainDataIndex += 1
#$d36e = wCurMapScriptPtr
bank1[mainDataIndex] = 0xB0
mainDataIndex += 1
bank1[mainDataIndex] = 0x40
mainDataIndex += 1
#$d370 = wCurMapConnections
mainDataIndex += 1
#$d371 = wNorthConnectedMap
#$d371 = wCurMapHeaderEnd
#$d371 = wNorthConnectionHeader
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
mainDataIndex = 0xd37c - wramMainData + sramMainData
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
mainDataIndex = 0xd387 - wramMainData + sramMainData
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
bank1[mainDataIndex] = 0xd0
bank1[mainDataIndex+1] = 0x40
mainDataIndex += 0xd3ad-0xd3a9
#$d3ad = wMapBackgroundTile
bank1[mainDataIndex] = 0x0A
mainDataIndex += 1
#$d3ae = wNumberOfWarps
bank1[mainDataIndex] = 1
mainDataIndex += 1
#$d3af = wWarpEntries
bank1[mainDataIndex] = 1
mainDataIndex += 1
bank1[mainDataIndex] = 7
mainDataIndex += 1
bank1[mainDataIndex] = 2
mainDataIndex += 1
bank1[mainDataIndex] = 0x25
mainDataIndex += 1
#$d42f = wDestinationWarpID
mainDataIndex = 0xd42f - wramMainData + sramMainData
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
mainDataIndex = 0xd524-wramMainData+sramMainData
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
#$d5cd = wSavedSpriteImageIndex
#$d5ce = wMissableObjectList
#$d5f0 = wOaksLabCurScript
#$d5f0 = wGameProgressFlags
#$d5f1 = wPalletTownCurScript
#$d5f3 = wBluesHouseCurScript
#$d5f4 = wViridianCityCurScript
#$d5f7 = wPewterCityCurScript
#$d5f8 = wRoute3CurScript
#$d5f9 = wRoute4CurScript
#$d5fb = wViridianGymCurScript
#$d5fc = wPewterGymCurScript
#$d5fd = wCeruleanGymCurScript
#$d5fe = wVermilionGymCurScript
#$d5ff = wCeladonGymCurScript
#$d600 = wRoute6CurScript
#$d601 = wRoute8CurScript
#$d602 = wRoute24CurScript
#$d603 = wRoute25CurScript
#$d604 = wRoute9CurScript
#$d605 = wRoute10CurScript
#$d606 = wMtMoon1FCurScript
#$d607 = wMtMoonB2FCurScript
#$d608 = wSSAnne1FRoomsCurScript
#$d609 = wSSAnne2FRoomsCurScript
#$d60a = wRoute22CurScript
#$d60c = wRedsHouse2FCurScript
#$d60d = wViridianMartCurScript
#$d60e = wRoute22GateCurScript
#$d60f = wCeruleanCityCurScript
#$d617 = wSSAnneBowCurScript
#$d618 = wViridianForestCurScript
#$d619 = wMuseum1FCurScript
#$d61a = wRoute13CurScript
#$d61b = wRoute14CurScript
#$d61c = wRoute17CurScript
#$d61d = wRoute19CurScript
#$d61e = wRoute21CurScript
#$d61f = wSafariZoneGateCurScript
#$d620 = wRockTunnelB1FCurScript
#$d621 = wRockTunnel1FCurScript
#$d623 = wRoute11CurScript
#$d624 = wRoute12CurScript
#$d625 = wRoute15CurScript
#$d626 = wRoute16CurScript
#$d627 = wRoute18CurScript
#$d628 = wRoute20CurScript
#$d629 = wSSAnneB1FRoomsCurScript
#$d62a = wVermilionCityCurScript
#$d62b = wPokemonTower2FCurScript
#$d62c = wPokemonTower3FCurScript
#$d62d = wPokemonTower4FCurScript
#$d62e = wPokemonTower5FCurScript
#$d62f = wPokemonTower6FCurScript
#$d630 = wPokemonTower7FCurScript
#$d631 = wRocketHideoutB1FCurScript
#$d632 = wRocketHideoutB2FCurScript
#$d633 = wRocketHideoutB3FCurScript
#$d634 = wRocketHideoutB4FCurScript
#$d636 = wRoute6GateCurScript
#$d637 = wRoute8GateCurScript
#$d639 = wCinnabarIslandCurScript
#$d63a = wPokemonMansion1FCurScript
#$d63c = wPokemonMansion2FCurScript
#$d63d = wPokemonMansion3FCurScript
#$d63e = wPokemonMansionB1FCurScript
#$d63f = wVictoryRoad2FCurScript
#$d640 = wVictoryRoad3FCurScript
#$d642 = wFightingDojoCurScript
#$d643 = wSilphCo2FCurScript
#$d644 = wSilphCo3FCurScript
#$d645 = wSilphCo4FCurScript
#$d646 = wSilphCo5FCurScript
#$d647 = wSilphCo6FCurScript
#$d648 = wSilphCo7FCurScript
#$d649 = wSilphCo8FCurScript
#$d64a = wSilphCo9FCurScript
#$d64b = wHallOfFameCurScript
#$d64c = wChampionsRoomCurScript
#$d64d = wLoreleisRoomCurScript
#$d64e = wBrunosRoomCurScript
#$d64f = wAgathasRoomCurScript
#$d650 = wCeruleanCaveB1FCurScript
#$d651 = wVictoryRoad1FCurScript
#$d653 = wLancesRoomCurScript
#$d658 = wSilphCo10FCurScript
#$d659 = wSilphCo11FCurScript
#$d65b = wFuchsiaGymCurScript
#$d65c = wSaffronGymCurScript
#$d65e = wCinnabarGymCurScript
#$d65f = wGameCornerCurScript
#$d660 = wRoute16Gate1FCurScript
#$d661 = wBillsHouseCurScript
#$d662 = wRoute5GateCurScript
#$d663 = wRoute7GateCurScript
#$d663 = wPowerPlantCurScript
#$d665 = wSSAnne2FCurScript
#$d666 = wSeafoamIslandsB3FCurScript
#$d667 = wRoute23CurScript
#$d668 = wSeafoamIslandsB4FCurScript
#$d669 = wRoute18Gate1FCurScript
#$d6b8 = wGameProgressFlagsEnd
#$d6f0 = wObtainedHiddenItemsFlags
#$d6fe = wObtainedHiddenCoinsFlags
#$d700 = wWalkBikeSurfState
#$d70b = wTownVisitedFlag
#$d70d = wSafariSteps
#$d70f = wFossilItem
#$d710 = wFossilMon
#$d713 = wEnemyMonOrTrainerClass
#$d714 = wPlayerJumpingYScreenCoordsIndex
#$d715 = wRivalStarter
#$d717 = wPlayerStarter
#$d718 = wBoulderSpriteIndex
#$d719 = wLastBlackoutMap
#$d71a = wDestinationMap
#$d71b = wUnusedD71B
#$d71c = wTileInFrontOfBoulderAndBoulderCollisionResult
#$d71d = wDungeonWarpDestinationMap
#$d71e = wWhichDungeonWarp
#$d71f = wUnusedD71F
#$d728 = wd728
#$d72a = wBeatGymFlags
#$d72c = wd72c
#$d72d = wd72d
#$d72e = wd72e
#$d730 = wd730
#$d732 = wd732
#$d733 = wFlags_D733
#$d734 = wBeatLorelei
#$d736 = wd736
#$d737 = wCompletedInGameTradeFlags
#$d73b = wWarpedFromWhichWarp
#$d73c = wWarpedFromWhichMap
#$d73f = wCardKeyDoorY
#$d740 = wCardKeyDoorX
#$d743 = wFirstLockTrashCanIndex
#$d744 = wSecondLockTrashCanIndex
#$d747 = wEventFlags
#$d887 = wLinkEnemyTrainerName
#$d887 = wGrassRate
#$d888 = wGrassMons
#$d893 = wSerialEnemyDataBlock
#$d89c = wEnemyPartyCount
#$d89d = wEnemyPartySpecies
#$d8a4 = wEnemyMons
#$d8a4 = wEnemyMon1Species
#$d8a4 = wEnemyMon1
#$d8a4 = wWaterRate
#$d8a5 = wWaterMons
#$d8a5 = wEnemyMon1HP
#$d8a7 = wEnemyMon1BoxLevel
#$d8a8 = wEnemyMon1Status
#$d8a9 = wEnemyMon1Type1
#$d8a9 = wEnemyMon1Type
#$d8aa = wEnemyMon1Type2
#$d8ab = wEnemyMon1CatchRate
#$d8ac = wEnemyMon1Moves
#$d8b0 = wEnemyMon1OTID
#$d8b2 = wEnemyMon1Exp
#$d8b5 = wEnemyMon1HPExp
#$d8b7 = wEnemyMon1AttackExp
#$d8b9 = wEnemyMon1DefenseExp
#$d8bb = wEnemyMon1SpeedExp
#$d8bd = wEnemyMon1SpecialExp
#$d8bf = wEnemyMon1DVs
#$d8c1 = wEnemyMon1PP
#$d8c5 = wEnemyMon1Level
#$d8c6 = wEnemyMon1MaxHP
#$d8c6 = wEnemyMon1Stats
#$d8c8 = wEnemyMon1Attack
#$d8ca = wEnemyMon1Defense
#$d8cc = wEnemyMon1Speed
#$d8ce = wEnemyMon1Special
#$d8d0 = wEnemyMon2Species
#$d8d0 = wEnemyMon2
#$d8d1 = wEnemyMon2HP
#$d8d3 = wEnemyMon2BoxLevel
#$d8d4 = wEnemyMon2Status
#$d8d5 = wEnemyMon2Type1
#$d8d5 = wEnemyMon2Type
#$d8d6 = wEnemyMon2Type2
#$d8d7 = wEnemyMon2CatchRate
#$d8d8 = wEnemyMon2Moves
#$d8dc = wEnemyMon2OTID
#$d8de = wEnemyMon2Exp
#$d8e1 = wEnemyMon2HPExp
#$d8e3 = wEnemyMon2AttackExp
#$d8e5 = wEnemyMon2DefenseExp
#$d8e7 = wEnemyMon2SpeedExp
#$d8e9 = wEnemyMon2SpecialExp
#$d8eb = wEnemyMon2DVs
#$d8ed = wEnemyMon2PP
#$d8f1 = wEnemyMon2Level
#$d8f2 = wEnemyMon2Stats
#$d8f2 = wEnemyMon2MaxHP
#$d8f4 = wEnemyMon2Attack
#$d8f6 = wEnemyMon2Defense
#$d8f8 = wEnemyMon2Speed
#$d8fa = wEnemyMon2Special
#$d8fc = wEnemyMon3
#$d8fc = wEnemyMon3Species
#$d8fd = wEnemyMon3HP
#$d8ff = wEnemyMon3BoxLevel
#$d900 = wEnemyMon3Status
#$d901 = wEnemyMon3Type
#$d901 = wEnemyMon3Type1
#$d902 = wEnemyMon3Type2
#$d903 = wEnemyMon3CatchRate
#$d904 = wEnemyMon3Moves
#$d908 = wEnemyMon3OTID
#$d90a = wEnemyMon3Exp
#$d90d = wEnemyMon3HPExp
#$d90f = wEnemyMon3AttackExp
#$d911 = wEnemyMon3DefenseExp
#$d913 = wEnemyMon3SpeedExp
#$d915 = wEnemyMon3SpecialExp
#$d917 = wEnemyMon3DVs
#$d919 = wEnemyMon3PP
#$d91d = wEnemyMon3Level
#$d91e = wEnemyMon3MaxHP
#$d91e = wEnemyMon3Stats
#$d920 = wEnemyMon3Attack
#$d922 = wEnemyMon3Defense
#$d924 = wEnemyMon3Speed
#$d926 = wEnemyMon3Special
#$d928 = wEnemyMon4Species
#$d928 = wEnemyMon4
#$d929 = wEnemyMon4HP
#$d92b = wEnemyMon4BoxLevel
#$d92c = wEnemyMon4Status
#$d92d = wEnemyMon4Type
#$d92d = wEnemyMon4Type1
#$d92e = wEnemyMon4Type2
#$d92f = wEnemyMon4CatchRate
#$d930 = wEnemyMon4Moves
#$d934 = wEnemyMon4OTID
#$d936 = wEnemyMon4Exp
#$d939 = wEnemyMon4HPExp
#$d93b = wEnemyMon4AttackExp
#$d93d = wEnemyMon4DefenseExp
#$d93f = wEnemyMon4SpeedExp
#$d941 = wEnemyMon4SpecialExp
#$d943 = wEnemyMon4DVs
#$d945 = wEnemyMon4PP
#$d949 = wEnemyMon4Level
#$d94a = wEnemyMon4Stats
#$d94a = wEnemyMon4MaxHP
#$d94c = wEnemyMon4Attack
#$d94e = wEnemyMon4Defense
#$d950 = wEnemyMon4Speed
#$d952 = wEnemyMon4Special
#$d954 = wEnemyMon5
#$d954 = wEnemyMon5Species
#$d955 = wEnemyMon5HP
#$d957 = wEnemyMon5BoxLevel
#$d958 = wEnemyMon5Status
#$d959 = wEnemyMon5Type1
#$d959 = wEnemyMon5Type
#$d95a = wEnemyMon5Type2
#$d95b = wEnemyMon5CatchRate
#$d95c = wEnemyMon5Moves
#$d960 = wEnemyMon5OTID
#$d962 = wEnemyMon5Exp
#$d965 = wEnemyMon5HPExp
#$d967 = wEnemyMon5AttackExp
#$d969 = wEnemyMon5DefenseExp
#$d96b = wEnemyMon5SpeedExp
#$d96d = wEnemyMon5SpecialExp
#$d96f = wEnemyMon5DVs
#$d971 = wEnemyMon5PP
#$d975 = wEnemyMon5Level
#$d976 = wEnemyMon5MaxHP
#$d976 = wEnemyMon5Stats
#$d978 = wEnemyMon5Attack
#$d97a = wEnemyMon5Defense
#$d97c = wEnemyMon5Speed
#$d97e = wEnemyMon5Special
#$d980 = wEnemyMon6
#$d980 = wEnemyMon6Species
#$d981 = wEnemyMon6HP
#$d983 = wEnemyMon6BoxLevel
#$d984 = wEnemyMon6Status
#$d985 = wEnemyMon6Type1
#$d985 = wEnemyMon6Type
#$d986 = wEnemyMon6Type2
#$d987 = wEnemyMon6CatchRate
#$d988 = wEnemyMon6Moves
#$d98c = wEnemyMon6OTID
#$d98e = wEnemyMon6Exp
#$d991 = wEnemyMon6HPExp
#$d993 = wEnemyMon6AttackExp
#$d995 = wEnemyMon6DefenseExp
#$d997 = wEnemyMon6SpeedExp
#$d999 = wEnemyMon6SpecialExp
#$d99b = wEnemyMon6DVs
#$d99d = wEnemyMon6PP
#$d9a1 = wEnemyMon6Level
#$d9a2 = wEnemyMon6MaxHP
#$d9a2 = wEnemyMon6Stats
#$d9a4 = wEnemyMon6Attack
#$d9a6 = wEnemyMon6Defense
#$d9a8 = wEnemyMon6Speed
#$d9aa = wEnemyMon6Special
#$d9ac = wEnemyMonOT
#$d9ac = wEnemyMon1OT
#$d9b7 = wEnemyMon2OT
#$d9c2 = wEnemyMon3OT
#$d9cd = wEnemyMon4OT
#$d9d8 = wEnemyMon5OT
#$d9e3 = wEnemyMon6OT
#$d9ee = wEnemyMonNicks
#$d9ee = wEnemyMon1Nick
#$d9f9 = wEnemyMon2Nick
#$da04 = wEnemyMon3Nick
#$da0f = wEnemyMon4Nick
#$da1a = wEnemyMon5Nick
#$da25 = wEnemyMon6Nick
#$da30 = wTrainerHeaderPtr
#$da38 = wOpponentAfterWrongAnswer
#$da38 = wUnusedDA38
#$da39 = wCurMapScript
#$da41 = wPlayTimeHours
#$da42 = wPlayTimeMaxed
#$da43 = wPlayTimeMinutes
#$da44 = wPlayTimeSeconds
#$da45 = wPlayTimeFrames
#$da46 = wSafariZoneGameOver
#$da47 = wNumSafariBalls
#$da48 = wDayCareInUse
#$da49 = wDayCareMonName
#$da54 = wDayCareMonOT
#$da5f = wDayCareMon
#$da5f = wDayCareMonSpecies
#$da60 = wDayCareMonHP
#$da62 = wDayCareMonBoxLevel
#$da63 = wDayCareMonStatus
#$da64 = wDayCareMonType
#$da64 = wDayCareMonType1
#$da65 = wDayCareMonType2
#$da66 = wDayCareMonCatchRate
#$da67 = wDayCareMonMoves
#$da6b = wDayCareMonOTID
#$da6d = wDayCareMonExp
#$da70 = wDayCareMonHPExp
#$da72 = wDayCareMonAttackExp
#$da74 = wDayCareMonDefenseExp
#$da76 = wDayCareMonSpeedExp
#$da78 = wDayCareMonSpecialExp
#$da7a = wDayCareMonDVs
#$da7c = wDayCareMonPP
#$da80 = wMainDataEnd

# still crashes after a few steps for some reason, but it's enough to use 8f and launch the program

# d163 is where 8f jumps to (start of the party data)
# https://glitchcity.wiki/wiki/ItemDex/RB:093#Older_setups
# party data in sram is at f2c
mainDataIndex = 0xf2c
prg = [ 0x03, 0xc3, 0x22, 0xd3]
for i, b in enumerate(prg):
	bank1[mainDataIndex + i] = b

for i, b in enumerate(boxProgram):
	bank1[0x10c1 + i] = b

bank1[0x1523] = checksum(bank1[0x598:0x1523])


with open("test.sav", "wb") as f:
	print(hex(f.write(bank0)))
	print(hex(f.write(bank1)))
	print(hex(f.write(bank2)))
	print(hex(f.write(bank3)))

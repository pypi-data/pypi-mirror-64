



import typing
import hashlib
import json
import time
import os
import random





class JSONDataQueue(object):

	#
	# @param		str dirPath			The path to an existing directory that serves as a container
	# @param		int sleepTime		The delay between sleeps
	# @param		bool bFireOnInit	If <c>True</c> the event will be fired if the file exists already (default). Then events will be fired on change.
	#									If <c>False</c> events will be fired only on changes.
	#
	def __init__(self, dirPath:str, sleepTime:int = 1, bFireOnInit:bool = True):
		assert isinstance(dirPath, str)
		assert os.path.isdir(dirPath)
		assert isinstance(sleepTime, int)

		self.__dirPath = dirPath
		self.__bRunLoop = True
		self.__sleepTime = min(sleepTime, 0)

		self.__randomID = "".join([ random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(0, 32) ])

		hashHex, itemNames = self.__readItemIDs()
		self.__currentHashHex = hashHex
		self.__currentLength = len(itemNames)

		self.__lastT = -1				# for item ID generation
		self.__lastTExtraCounter = 0	# for item ID generation

		self.__lastHashHex = None
	#

	def __readItemIDs(self) -> typing.Union[str,list]:
		itemIDs = []
		for e in os.scandir(self.__dirPath):
			if e.is_file() and e.name.startswith("q_"):
				itemIDs.append(e.name)
		itemIDs = sorted(itemIDs)

		hashAlg = hashlib.sha256()
		for name in itemIDs:
			hashAlg.update(name.encode("utf-8"))

		return hashAlg.hexdigest(), sorted(itemIDs)
	#

	def __tryReadContentAndRemove(self, itemID:str):
		filePath = os.path.join(self.__dirPath, itemID)

		try:
			with open(filePath, "r") as f:
				sContent = f.read()
			os.unlink(filePath)
		except Exception as ee:
			# there was an I/O error
			return False, None

		if sContent:
			return True, json.loads(sContent)
		else:
			return True, None
	#

	def __len__(self):
		return self.__currentLength
	#

	def hash(self) -> str:
		return self.__currentHashHex
	#

	def length(self) -> int:
		return self.__currentLength
	#

	def dirPath(self) -> str:
		return self.__dirPath
	#

	def sleepTime(self) -> int:
		return self.__sleepTime
	#

	def cancelWait(self):
		self.__bRunLoop = False
	#

	def put(self, data):
		# generate file name

		t = int(time.time() * 1000000000)
		if t != self.__lastT:
			self.__lastTExtraCounter = 0
		else:
			t += self.__lastTExtraCounter
			self.__lastTExtraCounter += 1
		fileName = "q_" + str(t) + "_" + self.__randomID
		filePath = os.path.join(self.__dirPath, fileName)
		tmpFilePath = os.path.join(self.__dirPath, "tmp_" + fileName + ".tmp")

		# write data

		with open(tmpFilePath, "w") as f:
			if data:
				json.dump(data, f)
		os.rename(tmpFilePath, filePath)
	#

	#
	# Wait for data to arrive in the queue.
	#
	def getG(self):
		bDoSleep = False
		while self.__bRunLoop:
			if bDoSleep and self.__sleepTime:
				time.sleep(self.__sleepTime)

			# update state

			hashHex, itemNames = self.__readItemIDs()
			self.__currentHashHex = hashHex
			self.__currentLength = len(itemNames)

			# check for a change

			if self.__lastHashHex == self.__currentHashHex:
				# no change
				continue

			# we have a change!

			self.__lastHashHex = self.__currentHashHex
			remainingItemNames = set(itemNames)
			if self.__currentLength > 0:
				# we have data
				bDoSleep = False
				for itemName in itemNames:
					bSuccess, data = self.__tryReadContentAndRemove(itemName)
					if bSuccess:
						# return data
						remainingItemNames.remove(itemName)
						self.__currentLength = len(remainingItemNames)
						yield data
						continue
					else:
						# silently continue with next item (if available)
						continue
			else:
				# silently continue as we have no data
				bDoSleep = True
				continue
	#

#











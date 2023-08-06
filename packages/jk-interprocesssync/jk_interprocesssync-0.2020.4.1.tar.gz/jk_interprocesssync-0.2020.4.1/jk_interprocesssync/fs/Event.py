



import time
import os





class Event(object):

	#
	# @param		str filePath		The path to the event file
	# @param		int sleepTime		The delay between sleeps
	# @param		bool bFireOnInit	If <c>True</c> the event will be fired if the file exists already (default). Then events will be fired on change.
	#									If <c>False</c> events will be fired only on changes.
	#
	def __init__(self, filePath:str, sleepTime:int = 1, bFireOnInit:bool = True):
		assert isinstance(filePath, str)
		assert filePath
		assert filePath.strip() == filePath

		self.__filePath = filePath
		self.__t = -1 if bFireOnInit else self.__readFileState()
		self.__bRunLoop = True
		self.__sleepTime = sleepTime
	#

	def __readFileState(self) -> int:
		try:
			return os.stat(self.__filePath).st_mtime
		except FileNotFoundError as ee:
			# no such file
			return -1
	#

	def filePath(self) -> str:
		return self.__filePath
	#

	def sleepTime(self) -> int:
		return self.__sleepTime
	#

	def cancelWait(self):
		self.__bRunLoop = False
	#

	def signal(self):
		with open(self.__filePath, "w") as f:
			pass
	#

	#
	# Wait for a single event.
	#
	def wait(self) -> bool:
		while self.__bRunLoop:
			time.sleep(min(1, self.__sleepTime))
			t = self.__readFileState()
			if (t >= 0) and (t != self.__t):
				# file has changed
				self.__t = t
				return True
		
		return False
	#

	#
	# Wait for events.
	#
	def waitG(self):
		while self.__bRunLoop:
			time.sleep(min(1, self.__sleepTime))

			t = self.__readFileState()
			if (t >= 0) and (t != self.__t):
				# file has changed
				self.__t = t
				yield True
	#

#











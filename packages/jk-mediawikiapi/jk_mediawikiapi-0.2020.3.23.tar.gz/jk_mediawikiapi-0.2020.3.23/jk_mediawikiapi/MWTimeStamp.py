


import datetime
import dateutil

from ._dump import DumpMethod




class MWTimeStamp(DumpMethod):

	def __init__(self, timeStampText:str):
		assert isinstance(timeStampText, str)
		self.orgText = timeStampText
		self.tDateTime = dateutil.parser.parse(timeStampText)
	#

	@property
	def asTuple(self) -> tuple:
		return self.tDateTime.timetuple()
	#

	@property
	def asTimeStamp(self) -> float:
		return self.tDateTime.timestamp()
	#

	def __str__(self):
		return str(self.tDateTime)
	#

	def __repr__(self):
		return str(self.tDateTime)
	#

#









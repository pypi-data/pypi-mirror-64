


from ._dump import DumpMethod

from .MWTimestamp import MWTimestamp



class MWCreatePageResult(DumpMethod):

	def __init__(self, title:str, pageID:int, oldRevID:int, bIsNew:bool, timestamp:MWTimestamp):
		self.title = title
		self.pageID = pageID
		self.oldRevID = oldRevID
		self.bIsNew = bIsNew
		self.timestamp = timestamp
	#

	def __bool__(self):
		return self.bSuccess
	#

	"""
	def dump(self):
		print("MWCreatePageResult[")
		print("\ttitle: ", self.title)
		print("\tpageID: ", self.pageID)
		print("\toldRevID: ", self.oldRevID)
		print("\tbIsNew: ", self.bIsNew)
		print("\ttimestamp: ", self.timestamp)
		print("]")
	#
	"""

#









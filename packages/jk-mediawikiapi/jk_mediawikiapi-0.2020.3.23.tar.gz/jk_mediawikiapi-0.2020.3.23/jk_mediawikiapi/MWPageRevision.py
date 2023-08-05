


import typing

from ._dump import DumpMethod

from .MWPageContent import MWPageContent
from .MWTimeStamp import MWTimeStamp




class MWPageRevision(DumpMethod):

	def __init__(self, revisionID:int, parentRevisionID:typing.Union[int,None], content:MWPageContent, bIsMinorRevision:bool, tags:list, timeStamp:MWTimeStamp, userName:str, sha1:str, size:int):
		assert isinstance(revisionID, int)
		self.revisionID = revisionID

		if parentRevisionID is not None:
			assert isinstance(parentRevisionID, int)
		self.parentRevisionID = parentRevisionID

		if content is not None:
			assert isinstance(content, MWPageContent)
		self.content = content

		assert isinstance(bIsMinorRevision, bool)
		self.bIsMinorRevision = bIsMinorRevision

		if tags is not None:
			assert isinstance(tags, list)
		self.tags = tags

		assert isinstance(timeStamp, MWTimeStamp)
		self.timeStamp = timeStamp

		assert isinstance(userName, str)
		self.userName = userName

		assert isinstance(sha1, str)
		self.sha1 = sha1

		assert isinstance(size, int)
		self.size = size
	#

#









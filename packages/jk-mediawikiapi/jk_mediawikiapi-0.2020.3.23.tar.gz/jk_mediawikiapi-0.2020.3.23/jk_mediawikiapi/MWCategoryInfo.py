


import typing

from ._dump import DumpMethod

from .MWPageContent import MWPageContent
from .MWTimeStamp import MWTimeStamp
from .MWPageRevision import MWPageRevision
from .MWNamespaceInfo import MWNamespaceInfo




class MWCategoryInfo(DumpMethod):

	def __init__(self,
		name:str,
		nPages:int,
		nTotalPages:int,
		nSubCategories:int
		):

		assert isinstance(name, str)
		self.name = name

		assert isinstance(nPages, int)
		self.nPages = nPages

		assert isinstance(nTotalPages, int)
		self.nTotalPages = nTotalPages

		assert isinstance(nSubCategories, int)
		self.nSubCategories = nSubCategories
	#

#









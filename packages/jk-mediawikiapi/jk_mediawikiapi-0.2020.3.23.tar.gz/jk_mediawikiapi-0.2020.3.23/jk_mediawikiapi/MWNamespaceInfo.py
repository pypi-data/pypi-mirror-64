


from ._dump import DumpMethod




class MWNamespaceInfo(DumpMethod):

	def __init__(self, nsID:int, nameCanonical:str, namePublic:str, bContent:bool, bNonIncludable:bool, bAllowsSubpages:bool, nameAlias:str):
		self.nsID = nsID
		self.bContent = bContent
		self.nameCanonical = nameCanonical
		self.namePublic = namePublic
		self.bNonIncludable = bNonIncludable
		self.bAllowsSubpages = bAllowsSubpages
		self.nameAlias = nameAlias
	#

	def __str__(self):
		return "NameSpace<" + str(self.nsID) + ":" + repr(self.nameCanonical) + ">"
	#

	def __repr__(self):
		return "NameSpace<" + str(self.nsID) + ":" + repr(self.nameCanonical) + ">"
	#

#









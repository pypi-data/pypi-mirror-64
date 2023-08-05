


from ._dump import DumpMethod




class MWUserGroupInfo(DumpMethod):

	def __init__(self, name:str, privileges):
		assert isinstance(name, str)
		self.name = name

		for item in privileges:
			assert isinstance(item, str)
		self.privileges = set(privileges)
	#

#









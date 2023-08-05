


from ._dump import DumpMethod




class MWPageContent(DumpMethod):

	def __init__(self, content:str, contentformat:str, contentmodel:str, sha1:str, size:int):
		assert isinstance(content, str)
		self.content = content

		assert isinstance(contentformat, str)
		self.contentformat = contentformat

		assert isinstance(contentmodel, str)
		self.contentmodel = contentmodel

		assert isinstance(sha1, str)
		self.sha1 = sha1

		assert isinstance(size, int)
		self.size = size
	#

#









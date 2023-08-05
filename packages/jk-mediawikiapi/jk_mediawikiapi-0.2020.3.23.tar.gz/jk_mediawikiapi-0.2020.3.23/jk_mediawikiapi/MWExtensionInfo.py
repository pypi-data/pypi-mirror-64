


from ._dump import DumpMethod




#
# This class provides information about an installed and active MediaWiki extension.
#
class MWExtensionInfo(DumpMethod):

	def __init__(self, name:str, extensionType:str, author:str, licenseID:str, url:str, version:str, description:str):
		self.name = name
		self.extensionType = extensionType
		self.author = author
		self.licenseID = licenseID
		self.url = url
		self.version = version
		self.description = description
	#

	"""
	def dump(self):
		print("MWExtensionInfo[")
		print("\tname: ", self.name)
		print("\textensionType: ", self.extensionType)
		print("\tauthor: ", self.author)
		print("\tlicenseID: ", self.licenseID)
		print("\turl: ", self.url)
		print("\tversion: ", self.version)
		print("\tdescription: ", self.description)
		print("]")
	#
	"""

#









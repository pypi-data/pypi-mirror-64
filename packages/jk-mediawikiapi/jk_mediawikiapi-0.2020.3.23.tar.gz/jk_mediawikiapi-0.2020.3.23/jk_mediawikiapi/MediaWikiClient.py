


import datetime
import pytz
import requests
import dateutil
import dateutil.parser
import typing

import bs4

import jk_typing
import jk_json
import jk_version
import jk_flexdata



from .MWCreatePageResult import MWCreatePageResult
from .MWNamespaceInfo import MWNamespaceInfo
from .MWUserGroupInfo import MWUserGroupInfo
from .MWExtensionInfo import MWExtensionInfo
from .MWPageContent import MWPageContent
from .MWTimeStamp import MWTimeStamp
from .MWPageRevision import MWPageRevision
from .MWPageInfo import MWPageInfo
from .MWPage import MWPage
from .MWCategoryInfo import MWCategoryInfo





class MediaWikiClient(object):

	#
	# @var		dict __siteInfo
	# @var		dict<int,MWNamespaceInfo> __namespacesByID
	# @var		dict<str,MWUserGroupInfo> __groupsByName
	#

	__EPOCH = datetime.datetime(1970, 1, 1, 0, 0, 0, 0, pytz.UTC)

	################################################################################################################################
	#### Initialization Methods
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self, wikiURL:str, userName:str, password:str):
		self.__session = requests.Session()
		if not wikiURL.endswith("/"):
			wikiURL += "/"
		self.__apiURL = wikiURL + "/api.php"
		self.__indexURL = wikiURL + "/index.php"
		self.__userName = userName
		self.__password = password

		self.__bLoggedIn = False

		# ----

		self.__performLogin(userName, password)
		self.__siteInfo, self.__namespacesByID, self.__groupsByName = self.__performGetSiteInfo()
		#self.__siteInfoTimeZone = pytz.timezone(self.__siteInfo["timezone"])
		#self.__siteInfoTimeOffset = self.__siteInfo["timeoffset"]
		# siteInfoTime = dateutil.parser.parse(self.__siteInfo["time"])		# returns current UTC time of server
	#

	################################################################################################################################
	#### Properties
	################################################################################################################################

	@property
	def namespaces(self) -> typing.List[MWNamespaceInfo]:
		return list(self.__namespacesByID.values())
	#

	@property
	def siteInfoWriteAPIEnabled(self) -> bool:
		if self.__siteInfo:
			return not self.__siteInfo["writeapi"]
		else:
			return None
	#

	@property
	def siteInfoUploadsEnabled(self) -> bool:
		if self.__siteInfo:
			return not self.__siteInfo["uploadsenabled"]
		else:
			return None
	#

	@property
	def siteInfoReadWrite(self) -> bool:
		if self.__siteInfo:
			return not self.__siteInfo["readonly"]
		else:
			return None
	#

	@property
	def siteInfoReadOnly(self) -> bool:
		if self.__siteInfo:
			return self.__siteInfo["readonly"]
		else:
			return None
	#

	@property
	def siteInfoSiteName(self) -> str:
		if self.__siteInfo:
			return self.__siteInfo["sitename"]
		else:
			return None
	#

	@property
	def siteInfoPHPVersion(self) -> jk_version.Version:
		if self.__siteInfo:
			s = self.__siteInfo["phpversion"]
			pos = s.find("-")
			assert pos != 0
			if pos > 0:
				s = s[:pos]
			return jk_version.Version(s)
		else:
			return None
	#

	@property
	def siteInfoMaxUploadSize(self) -> int:
		if self.__siteInfo:
			return self.__siteInfo["maxuploadsize"]
		else:
			return None
	#

	@property
	def siteInfoMaxArticleSize(self) -> int:
		if self.__siteInfo:
			return self.__siteInfo["maxarticlesize"]
		else:
			return None
	#

	@property
	def siteInfoMainPage(self) -> str:
		if self.__siteInfo:
			return self.__siteInfo["mainpage"]
		else:
			return None
	#

	@property
	def siteInfoWikiVersion(self) -> jk_version.Version:
		if self.__siteInfo:
			s = self.__siteInfo["generator"]
			assert s.startswith("MediaWiki ")
			return jk_version.Version(s[10:])
		else:
			return None
	#

	################################################################################################################################
	#### Helper Methods
	################################################################################################################################

	def __performGetPageContentHTML(self, pageTitle:str, bDebug:bool = False) -> str:
		assert self.__bLoggedIn

		params = {
			"title": pageTitle
		}

		if bDebug:
			print("\n" + ("-" * 120) + "\n>>>> REQUEST >>>>")
			jk_json.prettyPrint(params)

		for key in list(params.keys()):
			v = params[key]
			if isinstance(v, bool):
				if v is False:
					del params[key]

		response = self.__session.get(url=self.__indexURL, params=params)

		if bDebug:
			print("\n<<<< RESPONSE <<<<")
			print("status code = ", response.status_code)
			print("content type = ", response.headers["Content-Type"])
			#print(dir(response))
			#print(repr(response.text))
			print("\n" + ("-" * 120))

		if response.status_code == 404:
			return None
		else:
			return response.text
	#

	def __performGetPageContentHTMLParsed(self, pageTitle:str, bDebug:bool = False) -> bs4.BeautifulSoup:
		text = self.__performGetPageContentHTML(pageTitle, bDebug)
		if text:
			htmlContent = bs4.BeautifulSoup(text, "lxml")
			""""
			<div class="mw-parser-output">........</div>
			"""
			return htmlContent.find("div", attrs={ "class" : "mw-parser-output"})
		else:
			return None
	#

	def __performGetRequest(self, params:dict, bDebug:bool = False):
		for key in list(params.keys()):
			v = params[key]
			if isinstance(v, bool):
				if v is False:
					del params[key]

		if bDebug:
			print("\n" + ("-" * 120) + "\n>>>> REQUEST >>>>")
			jk_json.prettyPrint(params)

		response = self.__session.get(url=self.__apiURL, params=params)
		jsonResponse = response.json()
		if bDebug:
			print("\n<<<< RESPONSE <<<<")
			jk_json.prettyPrint(jsonResponse)
			print("\n" + ("-" * 120))

		return jsonResponse
	#

	def __performPostRequest(self, params:dict, bDebug:bool = False):
		for key in list(params.keys()):
			v = params[key]
			if isinstance(v, bool):
				if v is False:
					del params[key]

		if bDebug:
			print("\n" + ("-" * 120) + "\n>>>> REQUEST >>>>")
			jk_json.prettyPrint(params)

		response = self.__session.post(url=self.__apiURL, data=params)
		jsonResponse = response.json()
		if bDebug:
			print("\n<<<< RESPONSE <<<<")
			jk_json.prettyPrint(jsonResponse)
			print("\n" + ("-" * 120))

		return jsonResponse
	#

	def __performLogin(self, userName:str, password:str, bDebug:bool = False):
		if bDebug:
			print("\n" + ("#" * 120))

		# Step 1: GET Request to fetch login token

		loginToken = self.__performGetLoginToken(bDebug=bDebug)

		# Step 2: POST Request to log in. Use of main account for login is not
		# supported. Obtain credentials via Special:BotPasswords
		# (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
		jsonResponse = self.__performPostRequest({
			"action": "clientlogin",
			"username": userName,
			"password": password,
			"logintoken": loginToken,
			"rememberMe": True,
			"loginreturnurl": "http://localhost",
			"format": "json",
		}, bDebug=bDebug)

		if jsonResponse["clientlogin"]["status"] != "PASS":
			raise Exception("Login failed!")

		# ----

		self.__bLoggedIn = True

		if bDebug:
			print("\n" + ("#" * 120))
	#

	def __performGetSiteInfo(self, bDebug:bool = False):
		assert self.__bLoggedIn

		if bDebug:
			print("\n" + ("#" * 120))

		# Step 1: GET Request to fetch login token

		jsonResponse = self.__performGetRequest({
			"action": "query",
			"meta": "siteinfo",
			"formatversion": "2",
			"format": "json",
			"siprop": "general|namespaces|namespacealiases|usergroups"
		}, bDebug=bDebug)

		retGeneral = {}
		for keyword in [
			"dbtype", "dbversion", "generator", "maxarticlesize", "maxuploadsize", "phpversion", "sitename", "readonly",
			"time", "timeoffset", "timezone", "uploadsenabled", "writeapi", "mainpage"
		]:
			retGeneral[keyword] = jsonResponse["query"]["general"][keyword]

		retNamespaces = {}
		for jNamespace in jsonResponse["query"]["namespaces"].values():
			ns = MWNamespaceInfo(
				jNamespace["id"],
				jNamespace.get("canonical", jNamespace["name"]),
				jNamespace["name"],
				jNamespace["content"],
				jNamespace["nonincludable"],
				jNamespace["subpages"],
				None
			)
			retNamespaces[ns.nsID] = ns
		for jNameSpaceAlias in jsonResponse["query"]["namespacealiases"]:
			ns = retNamespaces[jNameSpaceAlias["id"]]
			ns.nameAlias = jNameSpaceAlias["alias"]


		retUserGroups = {}
		for jUserGroup in jsonResponse["query"]["usergroups"]:
			ug = MWUserGroupInfo(
				jUserGroup["name"],
				jUserGroup["rights"],
			)
			retUserGroups[ug.name] = ug

		if bDebug:
			print("\n" + ("#" * 120))

		return retGeneral, retNamespaces, retUserGroups
	#

	#
	# Iterates over a query
	#
	def __queryIterate(self, listCommand:str, bDebug:bool = False):
		assert isinstance(listCommand, str)
		availableCommands = {
			"allpages": [
				"ap",
				{
				},
			],
			"allcategories": [
				"ac",
				{
					"acprop": "size|hidden",
				},
			],
		}
		assert listCommand in availableCommands
		prefix, jsonArgs = availableCommands[listCommand]

		accontinue = None

		while True:
			jsonRequest = {
				"action": "query",
				"format": "json",
				"list": listCommand,
				prefix + "dir": "ascending",
				prefix + "limit": "max",
			}
			jsonRequest.update(jsonArgs)
			if accontinue:
				jsonRequest[prefix + "continue"] = accontinue

			jsonResponse = self.__performGetRequest(jsonRequest, bDebug=bDebug)

			"""
			{
				"batchcomplete": "",
				"continue": {
						"accontinue": "Anwendungssoftware",
						"continue": "-||"
				},
				"query": {
						"allcategories": [
							....
						]
					}
				}
			}
			"""

			for item in jsonResponse["query"][listCommand]:
				yield item

			if "continue" in jsonResponse:
				accontinue = jsonResponse["continue"][prefix + "continue"]
			else:
				break
	#

	def ____performGetToken(self, tokenType:str, bDebug:bool = False) -> str:
		assert isinstance(tokenType, str)
		assert tokenType in [ "login", "csrf", "createaccount", "patrol", "rollback", "userrights", "watch" ]

		if tokenType != "login":
			assert self.__bLoggedIn

		if bDebug:
			print("\n" + ("#" * 120))

		jsonResponse = self.__performGetRequest({
			"action": "query",
			"meta": "tokens",
			"type": tokenType,
			"format": "json"
		}, bDebug=bDebug)

		if bDebug:
			print("\n" + ("#" * 120))

		return jsonResponse["query"]["tokens"][tokenType + "token"]
	#

	def __performGetCSRFToken(self, bDebug:bool = False) -> str:
		return self.____performGetToken("csrf", bDebug=bDebug)
	#

	def __performGetLoginToken(self, bDebug:bool = False) -> str:
		return self.____performGetToken("login", bDebug=bDebug)
	#

	def __performGetCreateAccountToken(self, bDebug:bool = False) -> str:
		return self.____performGetToken("createaccount", bDebug=bDebug)
	#

	################################################################################################################################
	#### Public Methods
	################################################################################################################################

	#
	# @return		MWExtensionInfo[]		Returns a list of MWExtensionInfo objects
	#
	def listExtensions(self, bDebug:bool = False) -> list:
		assert self.__bLoggedIn

		if bDebug:
			print("\n" + ("#" * 120))

		jsonResponse = self.__performGetRequest({
			"action": "query",
			"meta": "siteinfo",
			"formatversion": "2",
			"format": "json",
			"siprop": "extensions"
		}, bDebug=bDebug)

		ret = []
		for jExtension in jsonResponse["query"]["extensions"]:
			if "description" in jExtension:
				description = jExtension["description"]
			elif "descriptionmsg" in jExtension:
				divContent = self.__performGetPageContentHTMLParsed("MediaWiki:" + jExtension["descriptionmsg"], bDebug=bDebug)
				if divContent:
					""""
					<p>Erweitert den Parser um logische Funktionen
					</p>
					"""
					description = divContent.p.text.strip()
				else:
					description = None
			else:
				description = None

			ei = MWExtensionInfo(
				jExtension["name"],
				jExtension["type"],
				jExtension["author"],
				jExtension.get("license-name"),
				jExtension["url"],
				jExtension.get("version"),
				description,
			)
			ret.append(ei)

		if bDebug:
			print("\n" + ("#" * 120))

		return ret
	#

	def getPageInfo(self, pageTitle:str, bDebug:bool = False) -> typing.Union[MWPageInfo,None]:
		assert self.__bLoggedIn

		if bDebug:
			print("\n" + ("#" * 120))

		jsonResponse = self.__performGetRequest({
			"action": "query",
			"format": "json",
			"titles": pageTitle,
			"prop": "info|categories|categoryinfo|pageprops|revisions",
			"intestactions": "read",
			"inprop": "url|displaytitle|talkid|protection",
			"rvprop": "ids|timestamp|flags|user|userid|size|slotsize|sha1|slotsha1|contentmodel|comment|tags|roles",
			"formatversion": 2,
		}, bDebug=bDebug)

		if bDebug:
			print("\n" + ("#" * 120))

		if "-1" in jsonResponse["query"]["pages"]:
			return None
		else:
			if "normalized" in jsonResponse["query"]:
				_pageTitle = jsonResponse["query"]["normalized"][0]["to"]
				_searchTitle = jsonResponse["query"]["normalized"][0]["from"]
			else:
				_pageTitle = pageTitle
				_searchTitle = pageTitle

			r = jsonResponse["query"]["pages"]
			jPageInfo = r[0]
			jRevision = jPageInfo["revisions"][0]

			return MWPageInfo(
				title=_pageTitle,
				searchTitle=_searchTitle,
				namespace=self.__namespacesByID[jPageInfo["ns"]],
				pageID=jPageInfo["pageid"],
				mainRevision=MWPageRevision(
					revisionID=jRevision["revid"],
					parentRevisionID=jRevision.get("parentid"),
					content=None,
					bIsMinorRevision="minor" in jRevision and jRevision["minor"],
					timeStamp=MWTimeStamp(jRevision["timestamp"]),
					userName=jRevision["user"],
					tags=None,
					sha1=jRevision["sha1"],
					size=jRevision["size"]
				)
			)
	#

	def listPages(self, bDebug:bool = False) -> typing.Iterator[MWPageInfo]:
		assert self.__bLoggedIn

		if bDebug:
			print("\n" + ("#" * 120))

		for jPageInfo in self.__queryIterate("allpages", bDebug=bDebug):
			yield MWPageInfo(
				title = jPageInfo["title"],
				searchTitle = None,
				namespace = self.__namespacesByID[jPageInfo["ns"]],
				pageID = jPageInfo["pageid"],
				mainRevision = None,
			)

		if bDebug:
			print("\n" + ("#" * 120))
	#

	def listCategories(self, bDebug:bool = False) -> typing.Iterator[MWCategoryInfo]:
		assert self.__bLoggedIn

		if bDebug:
			print("\n" + ("#" * 120))

		for jCategoryInfo in self.__queryIterate("allcategories", bDebug=bDebug):
			yield MWCategoryInfo(
				name = jCategoryInfo["*"],
				nPages = jCategoryInfo["pages"],
				nTotalPages = jCategoryInfo["size"],
				nSubCategories = jCategoryInfo["subcats"],
			)

		if bDebug:
			print("\n" + ("#" * 120))
	#

	def logout(self, bDebug:bool = False):
		assert self.__bLoggedIn

		if bDebug:
			print("\n" + ("#" * 120))

		csrfToken = self.__performGetCSRFToken(bDebug=bDebug)

		jsonResponse = self.__performGetRequest({
			"action": "logout",
			"token": csrfToken,
			"format": "json"
		}, bDebug=bDebug)

		self.__bLoggedIn = False

		if bDebug:
			print("\n" + ("#" * 120))
	#

	def getPageContent(self, pageTitle:str, bDebug:bool = False) -> MWPage:
		assert self.__bLoggedIn

		if bDebug:
			print("\n" + ("#" * 120))

		jsonResponse = self.__performGetRequest({
			"action": "query",
			"format": "json",
			"titles": pageTitle,
			"prop": "revisions",
			"rvslots": "*",
			"rvprop": "content|ids|timestamp|flags|user|userid|size|slotsize|sha1|slotsha1|contentmodel|comment|tags|roles",
			"formatversion": 2,
			"rvlimit": 1,
		}, bDebug=bDebug)

		if bDebug:
			print("\n" + ("#" * 120))

		jPage = jsonResponse["query"]["pages"][0]
		if "revisions" not in jPage:
			return None

		if "normalized" in jsonResponse["query"]:
			_pageTitle = jsonResponse["query"]["normalized"][0]["to"]
			_searchTitle = jsonResponse["query"]["normalized"][0]["from"]
		else:
			_pageTitle = pageTitle
			_searchTitle = pageTitle

		jRevision = jPage["revisions"][0]
		ret = MWPage(
			title=_pageTitle,
			searchTitle=_searchTitle,
			namespace=self.__namespacesByID[jPage["ns"]],
			pageID=jPage["pageid"],
			mainRevision=MWPageRevision(
				revisionID=jRevision["revid"],
				parentRevisionID=jRevision.get("parentid"),
				content=MWPageContent(
					content=jRevision["slots"]["main"]["content"],
					contentformat=jRevision["slots"]["main"]["contentformat"],
					contentmodel=jRevision["slots"]["main"]["contentmodel"],
					sha1=jRevision["slots"]["main"]["sha1"],
					size=jRevision["slots"]["main"]["size"]
				),
				bIsMinorRevision="minor" in jRevision and jRevision["minor"],
				timeStamp=MWTimeStamp(jRevision["timestamp"]),
				userName=jRevision["user"],
				tags=jRevision["tags"],
				sha1=jRevision["sha1"],
				size=jRevision["size"]
			)
		)

		return ret
	#

	def getPageContentHTML(self, pageTitle:str, bDebug:bool = False) -> str:
		assert self.__bLoggedIn

		if bDebug:
			print("\n" + ("#" * 120))

		ret = self.__performGetPageContentHTML(pageTitle, bDebug)

		if bDebug:
			print("\n" + ("#" * 120))

		return ret
	#

	def getPageContentHTMLParsed(self, pageTitle:str, bDebug:bool = False) -> bs4.BeautifulSoup:
		assert self.__bLoggedIn

		if bDebug:
			print("\n" + ("#" * 120))

		ret = self.__performGetPageContentHTMLParsed(pageTitle, bDebug)

		if bDebug:
			print("\n" + ("#" * 120))

		return ret
	#

	def uploadPageContent(self,
		pageID:typing.Union[int,None],
		pageTitle:typing.Union[str,None],
		pageContent:str,
		summary:str = "",
		bIsMinor:bool = True,
		bIsBot:bool = False,
		bDontEditIfExists:bool = False,
		bDontEditIfNotExists:bool = False,
		bDebug:bool = False) -> typing.Union[MWCreatePageResult,None]:

		if pageID is not None:
			assert isinstance(pageID, int)
			assert pageTitle is None
		else:
			assert isinstance(pageTitle, str)
			assert pageTitle

		assert isinstance(pageContent, str)
		assert pageContent

		assert isinstance(summary, str)

		assert isinstance(bIsMinor, bool)

		assert isinstance(bDontEditIfExists, bool)

		assert isinstance(bDontEditIfNotExists, bool)

		# ----

		assert self.__bLoggedIn

		# ----

		if bDebug:
			print("\n" + ("#" * 120))

		csrfToken = self.__performGetCSRFToken(bDebug = bDebug)

		jsonRequest = {
			"action": "edit",
			"format": "json",
			"text": pageContent,
			"summary": summary,
			"minor": bIsMinor,
			"bot": bIsBot,
			"recreate": True,
			"createonly": bDontEditIfExists,
			"nocreate": bDontEditIfNotExists,
			"contentformat": "text/x-wiki",
			"contentmodel": "wikitext",
			"token": csrfToken,
		}
		if pageID is not None:
			jsonRequest["pageid"] = pageID
		else:
			jsonRequest["title"] = pageTitle

		jsonResponse = self.__performPostRequest(jsonRequest, bDebug=bDebug)

		jEdit = jsonResponse["edit"]
		if jEdit["result"] == "Success":
			if "nochange" in jEdit:
				# no change
				pageID = jEdit["pageid"]
				ret = MWCreatePageResult(pageTitle, pageID, None, False, None)
			else:
				# create or edit has been performed
				bIsNew = "new" in jEdit
				revID = jEdit["newrevid"]
				timestamp = MWTimeStamp(jEdit["newtimestamp"])
				pageID = jEdit["pageid"]
				oldRevID = jEdit.get("oldrevid")
				ret = MWCreatePageResult(pageTitle, pageID, oldRevID, bIsNew, timestamp)
		else:
			ret = None

		if bDebug:
			print("\n" + ("#" * 120))

		return ret
	#

#

























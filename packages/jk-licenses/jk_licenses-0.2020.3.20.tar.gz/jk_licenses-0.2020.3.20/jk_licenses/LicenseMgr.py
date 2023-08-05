

import os
import typing
import jk_json

from .License import License
from .VariableDef import VariableDef





class LicenseMgr(object):

	def __init__(self, licenseDirs:list = None):
		if licenseDirs is None:
			licenseDirs = []

			licenseDirs.append(os.path.join(os.path.dirname(__file__), "licenses"))

		self.__licenseDirs = tuple(licenseDirs)
		self.__licenses = None
		self.__licensesByMainID = None
	#

	@property
	def dirPaths(self) -> tuple:
		return self.__licenseDirs
	#

	@property
	def allLicenseIDs(self) -> typing.Sequence[str]:
		if self.__licenses is None:
			self.scan()
		return sorted(self.__licenses.keys())
	#

	@property
	def mainLicenseIDs(self) -> typing.Sequence[str]:
		if self.__licensesByMainID is None:
			self.scan()
		return sorted(self.__licensesByMainID.keys())
	#

	@property
	def licenses(self) -> typing.Sequence[License]:
		if self.__licensesByMainID is None:
			self.scan()
		mainLicenseIDs = [ l.licenseID for l in self.__licenses.values() ]
		for licenseID in sorted(self.__licensesByMainID.keys()):
			yield self.__licensesByMainID[licenseID]
	#

	def scan(self):
		self.__licenses = {}
		self.__licensesByMainID = {}
		for dirPath in self.__licenseDirs:
			if os.path.isdir(dirPath):
				for entry in os.listdir(dirPath):
					if entry.endswith(".json"):
						fullPath = os.path.join(dirPath, entry)
						self.__loadLicense(fullPath)
	#

	def __loadLicense(self, fullPath:str):
		licenseRawFilePath = fullPath[:-5] + ".txt"
		if not os.path.isfile(licenseRawFilePath):
			licenseRawFilePath = None

		jLicenseInfo = jk_json.loadFromFile(fullPath)

		if "identifiers" in jLicenseInfo:
			identifiers = jLicenseInfo["identifiers"]
		else:
			identifiers = []
		if "identifier" in jLicenseInfo:
			mainIdentifier = jLicenseInfo["identifier"]
			identifiers.insert(0, mainIdentifier)
		mainIdentifier = identifiers[0]

		name = jLicenseInfo["name"]

		url = jLicenseInfo.get("url")

		classifier = jLicenseInfo.get("classifier")

		variableDefs = {}
		if "variables" in jLicenseInfo:
			for jVarDefs in jLicenseInfo["variables"]:
				varName = jVarDefs["name"]
				varType = jVarDefs.get("type", "str")
				assert varType in [ "bool", "str", "int" ]
				varDescr = jVarDefs.get("description")
				variableDefs[varName] = VariableDef(varName, varType, varDescr)

		#

		lic = License(mainIdentifier, identifiers, name, url, classifier, licenseRawFilePath, variableDefs)

		self.__licensesByMainID[lic.licenseID] = lic
		self.__licenses[lic.licenseID] = lic
		for licenseID in lic.licenseIDs:
			self.__licenses[licenseID] = lic
	#

	def getLicense(self, identifier:str):
		if self.__licenses is None:
			self.scan()
		return self.__licenses[identifier]
	#

#










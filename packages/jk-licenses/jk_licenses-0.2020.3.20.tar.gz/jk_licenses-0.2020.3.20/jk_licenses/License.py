

import os
from typing import Union, List

import jk_typing

from .VariableDef import VariableDef




#
# This class represents a license.
#
class License(object):

	#
	# Constructor.
	#
	# @param	str mainIdentifier					(required) The unique identifier of the license.
	# @param	str[] allIdentifiers				(required) The unique identifier of the license.
	# @param	str name							(required) The human readable name of the license.
	# @param	str url								(required) An URL with information about this license (if exists).
	# @param	str classifier						(optional) The python classifier such as "License :: OSI Approved :: MIT License".
	# @param	str rawLicenseFilePath				(optional) The file containing the license text in plaintext format.
	# @param	VariableDef[] rawLicenseFilePath	(optional) The placeholders for this license text.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, mainIdentifier:str, allIdentifiers:Union[list,tuple], name:str, url:str, classifier:Union[str,None], rawLicenseFilePath:Union[str,None], varDefs:Union[dict,None]):
		self.__licenseID = mainIdentifier
		self.__licenseIDs = tuple(sorted(set(allIdentifiers)))
		self.__name = name
		self.__url = url
		self.__classifier = classifier
		self.__variableDefs = varDefs
		self.__rawLicenseFilePath = rawLicenseFilePath
		self.__rawTextCached = None
	#

	@property
	def variableDefinitions(self) -> tuple:
		return tuple(self.__variableDefs.values())
	#

	@property
	def name(self) -> str:
		return self.__name
	#

	@property
	def licenseIDs(self) -> tuple:
		return self.__licenseIDs
	#

	@property
	def classifier(self) -> str:
		return self.__classifier
	#

	@property
	def licenseID(self) -> str:
		return self.__licenseID
	#

	@jk_typing.checkFunctionSignature()
	def __extractVars(self, rawText:str) -> set:
		ret = set()
		for m in re.findall(r"{{([a-zA-Z_][a-zA-Z_0-9-]*?)}}", rawText):
			ret.add(m)
		return ret
	#

	@jk_typing.checkFunctionSignature()
	def __replace(self, text:str, substMatrix:dict) -> str:
		for substKey, substValue in substMatrix.items():
			text = text.replace(substKey, substValue)
		return text
	#

	@jk_typing.checkFunctionSignature()
	def produceText(self, variableAssignments:dict = None) -> str:
		if variableAssignments is None:
			variableAssignments = {}

		# load license text

		if self.__rawTextCached is None:
			self.__rawTextCached = self.__loadLicenseText()

		# build substitution matrix

		self.validateVariableAssignments(variableAssignments)

		substMatrix = {}
		for varName in self.__variableDefs:
			substMatrix["{{" + varName + "}}"] = str(variableAssignments.get(varName, ""))

		# create output data

		text = self.__replace(self.__rawTextCached, substMatrix)

		# ----

		return text
	#

	@jk_typing.checkFunctionSignature()
	def validateVariableAssignments(self, variableAssignments:dict):
		missingVariables = set(self.__variableDefs.keys()) - set(variableAssignments.keys())
		if missingVariables:
			raise Exception("No value specified for variable(s): " + repr(list(missingVariables))[1:-1])
	#

	def __loadLicenseText(self) -> str:
		if self.__rawLicenseFilePath:
			with open(self.__rawLicenseFilePath, "r", encoding="UTF-8-sig") as f:
				return f.read().rstrip()
		else:
			return "(license text not available)"
	#

#




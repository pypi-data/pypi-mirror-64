from prot.functions import *
from prot import protPath
import json
import os

settingFilePath = protPath+'/settings'
localSets = False
settingVals = {
				'repo':'default',
				'ui':'normall'
				}

settingData = None

def load():
	global settingData
	if localSets:
		printWarn("can't create settings file because permission denied, using default settings")
		settingData = settingVals
		return settingVals
	if not os.path.exists(settingFilePath):
		raise FileNotFoundError('settings file not found.')
	else:
		settingFile = open(settingFilePath)
		data = read(settingFile.read().splitlines())
		settingFile.close()
		settingData = data
		return data

def read(data):
	out = {}
	for d in data:
		extract = d.split(':')
		out[extract[0]] = extract[1]
	return out

def convert(data):
	string = ''
	for s in data:
		string += s + ':' + str(data[s]) + '\n'
	return string

def setup():
	global localSets
	if not os.path.exists(settingFilePath):
		try:
			settingFile = open(settingFilePath, 'w')
			settingFile.write(convert(settingVals))
			settingFile.flush()
			settingFile.close()
		except PermissionError:
			localSets = True
	else:
		data = load()
		updated = False
		for s in settingVals:
			if not s in data:
				data[s] = settingVals[s]
				updated = True
		if updated:
			try:
				settingFile = open(settingFilePath, 'w')
				settingFile.write(convert(data))
				settingFile.flush()
				settingFile.close()
			except PermissionError:
				localSets = True

class Settings(object):
	def __init__(self):
		if settingData:
			self._data = settingData
		else:
			self._data = load()

	def _write(self):
		global localSets
		try:
			self._file = open(settingFilePath, 'w')
			self._file.write(convert(self._data))
			self._file.flush()
			self._file.close()
		except PermissionError:
			localSets = True

	def __getattr__(self, key):
		if not key.startswith('_'):
			try:
				return self._data[key]
			except KeyError:
				return 'KeyError: ' + "'" + key + "'"
		else:
			return object.__getattribute__(self, key)

	def __setattr__(self, key, val):
		if not key.startswith('_'):
			self._data[key] = val
			self._write()
		else:
			object.__setattr__(self, key, val)

setup()
settings = Settings()

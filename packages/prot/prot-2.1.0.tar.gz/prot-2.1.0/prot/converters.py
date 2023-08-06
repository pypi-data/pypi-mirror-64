import os
from prot.functions import *
try:
	from docutils.core import publish_file as pf
except:
	pf = None

def rst2html(path, subdirs=False):
	if pf is None:
		printErr('docutils package needed.')
		return
	if os.path.isdir(path):
		for p in os.listdir(path):
			if os.path.isdir(path+'/'+p):
				if subdirs:
					rst2html(path+'/'+p, True)
			else:
				rst2html(path+'/'+p)
	if os.path.exists(path):
		if path.endswith('.rst'):
			try:
				pf(source_path=path, destination_path=path.split('.rst')[0]+'.html', writer_name='html')
			except:
				import traceback
				traceback.print_stack()
				traceback.print_exc()
	else:
		printErr('file or folder '+path+' not found.')
		return

def dict2matrix(obj):
	if not type(obj) == dict:
		raise TypeError('dict object is required.')
	matrix = []
	for m in obj:
		if type(obj[m]) == dict:
			matrix.append(dict2matrix(obj[m]))
		else:
			matrix.append([obj[m]])
	return matrix

def str2list(string):
	if not type(string) == str:
		raise TypeError('str object is required.')
	strList = []
	for s in string:
		strList.append(s)
	return strList

def list2str(listObj, space=''):
	if not type(listObj) == list:
		raise TypeError('list object is required.')
	string = ''
	for s in listObj:
		if string:
			string += space
		string += str(s)
	return string

def matrix2str(mat, space=''):
	if not type(mat) == list:
		raise TypeError('list object is required.')
	string = ''
	for m in mat:
		if string:
			string += space
		if type(m) == list:
			string += str(matrix2str(m))
		elif type(m) == dict:
			string += str(matrix2str(dict2matrix(m)))
		else:
			string += str(m)
	return string

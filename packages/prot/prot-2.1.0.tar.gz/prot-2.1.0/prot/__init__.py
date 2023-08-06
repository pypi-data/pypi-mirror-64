import runpy as _r
import sys
from prot.classes import *
from prot.converters import *
from prot.functions import *

__version__ = '2.1.0'
protPath = __path__[0]

def settings():
	return __import__('prot.settings').settings
	
def prot(args=None):
	if type(args) == list:
		args = ['prot'] + args
	elif type(args) == str:
		args = ['prot'] + args.split(' ')
	else:
		args = sys.argv
	if not args[0] == 'prot':
		args[0] = 'prot'
	sys.argv = args
	_r._run_module_as_main(sys.argv[0])

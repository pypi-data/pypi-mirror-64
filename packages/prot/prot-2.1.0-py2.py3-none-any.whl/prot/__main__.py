import sys
import prot as p
from prot.settings import settings
from prot.functions import *

if __name__ == '__main__':
	for a in sys.argv[1:]:
		if a in ['version', 'ver', '__version__', 'v']:
			printMsg(p.__version__)
			break
		elif a in ['speedTest', 'speedtest', 'speed', 'test', 't']:
			try:
				c = int(sys.argv[2])
			except:
				c = 1000
			testSpeed(c)
			break
		elif a in ['setting', 'set', 's']:
			if len(sys.argv) == 3:
				printMsg(getattr(settings, sys.argv[2]))
			elif len(sys.argv) == 4:
				setattr(settings, sys.argv[2], sys.argv[3])
				printMsg(sys.argv[2] + ' : ' + sys.argv[3])
			else:
				printErr('argument is invalid.')
			break
		else:
			printErr('argument is invalid.')
			break
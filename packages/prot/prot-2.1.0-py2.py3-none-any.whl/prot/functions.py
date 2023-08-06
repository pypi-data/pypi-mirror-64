import hashlib
import sys
import os
import runpy as _r
import random
from prot.converters import str2list
from prot.color.ansi import *
try:
	import prot.color as _c
	errWin32 = _c.ansitowin32.AnsiToWin32(sys.stderr, convert=True)
	outWin32 = _c.ansitowin32.AnsiToWin32(sys.stdout, convert=True)
except:
	_c = None

colors = {
			'foreground': {
							'black':Fore.BLACK,
							'red':Fore.RED,
							'green':Fore.GREEN,
							'yellow':Fore.YELLOW,
							'blue':Fore.BLUE,
							'magenta':Fore.MAGENTA,
							'cyan':Fore.CYAN,
							'white':Fore.WHITE,
							'reset':Fore.RESET
							},
			'background': {
							'black':Back.BLACK,
							'red':Back.RED,
							'green':Back.GREEN,
							'yellow':Back.YELLOW,
							'blue':Back.BLUE,
							'magenta':Back.MAGENTA,
							'cyan':Back.CYAN,
							'white':Back.WHITE,
							'reset':Back.RESET
							},
			'style': {
						'bright':Style.BRIGHT,
						'dim':Style.DIM,
						'normal':Style.NORMAL,
						'end':Style.RESET_ALL,
						'clearline':clear_line(),
						'clear':clear_screen(),
						}
		}

colorSymbols = {'foreground':'-', 'background':'+', 'style':'*'}

charDict = {
				'lowers' : 'abcdefghijklmnopqrstuvwxyz',
				'uppers' : 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
				'symbols' : './~!@#$%&*-_=+?',
				'numbers' : '0123456789'
				}

def verifyColor(color, exceptionOnNot=True):
	for c in colors['foreground']:
		if color == c:
			return True
	if exceptionOnNot:
		raise ValueError('color not found.')
	else:
		return False

def insertColor(string):
	for c in colors:
		for sc in colors[c]:
			string = string.replace(colorSymbols[c]+sc, colors[c][sc])
	return string

def getRandomPassword(passwordLen=4, types=['lowers', 'uppers', 'symbols', 'numbers']):
	password = ''
	for r in range(passwordLen):
		password += random.choice(str2list(charDict[random.choice(types)]))
	return password

def testSpeed(count):
	from prot.classes import Progress, TimeWidget
	progress = Progress(maxVal=count, msgForm='($VAL/$MAX) $TIME $PERC% completed', replaces=[['$TIME', TimeWidget(milisec=True)]], inline=True)
	for c in range(count):
		progress.next()
	progress.newline()

def getVarFromFile(f, v):
	templates = [
			'%s =',
			'%s=',
			'as %s',
			'import %s',
			'%s,'
			]
	if type(f) == str:
		f = open(f).read()
	fileMap = f.splitlines()
	for f in fileMap:
		if f:
			for t in templates:
				ct = t % v
				if ct in f:
					class tempCls:
						exec(f)
					res = getattr(tempCls, v)
					return res

def checkMethods(f):
	for s in dir(f):
		printMsg(s+' : '+str(getattr(f, s)))

def callMethods(f):
	for s in dir(f):
		try:
			printMsg('result of '+s+'() is '+str(getattr(f, s)()))
		except:
			printMsg('error in '+str(s)+'()')

def callMethodsWithArg(f, a):
	for s in dir(f):
		try:
			printMsg('result of '+s+'('+str(a)+') is '+str(getattr(f, s)(a)))
		except:
			printMsg('error in '+str(s)+'('+str(a)+')')

def checkFileSame(f1, f2):
	try:
		md5s = [hashlib.md5(), hashlib.md5()]
		fs = [f1, f2]
		for i in range(2):
			f = open(fs[i], 'rb')
			block_size = 2 ** 20
			while True:
				data = f.read(block_size)
				if not data: break
				md5s[i].update(data)
			f.close()
			md5s[i] = md5s[i].hexdigest()
		return md5s[0] == md5s[1]
	except:
		return False

def splitStr(s, l):
	out = []
	try:
		if len(s) > l:
			splitDelay = len(s) // l
			for i in range(splitDelay):
				out.append(s[:l])
				s = s[l:]
			if not s == '':
				out.append(s)
		else:
			out = [s]
	except:
		out = []
	return out

def runAsMain(args=None):
	if type(args) == list:
		pass
	elif type(args) == str:
		args = args.split(' ')
	else:
		args = sys.argv
	sys.argv = args
	_r._run_module_as_main(sys.argv[0])

def printMsg(msg, type='msg', color=None, end='\n', file=sys.stdout):
	msg = str(msg)
	if color and verifyColor(color):
		msg = '-' + color + msg + '*end'
	if type == 'msg':
		if not os.name == 'nt' or _c:
			msg = insertColor(msg)
		out = file
		if os.name == 'nt' and _c:
			out = outWin32
		out.write(msg+end)
	elif type == 'warn':
		if not os.name == 'nt' or _c:
			msg = insertColor('-yellow'+msg+'*end')
		out = file
		if os.name == 'nt' and _c:
			out = outWin32
		out.write(msg+end)
	elif type == 'err':
		if not os.name == 'nt' or _c:
			msg = insertColor('-red'+msg+'*end')
		err = sys.stderr
		if os.name == 'nt' and _c:
			err = errWin32
		err.write(msg+end)
	else:
		printErr('type is invalid.')

def printErr(msg):
	printMsg('ERROR: '+str(msg), 'err')

def printWarn(msg):
	printMsg('WARNING: '+str(msg), 'warn')

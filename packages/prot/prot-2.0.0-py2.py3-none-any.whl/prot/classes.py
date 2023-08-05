from prot.functions import *
import time

class Widget(object):
	def __init__(self, progressNeeded=False):
		self.reprMsg = '<$name Widget>'.replace('$name', str(self.__class__.__name__))
		self.progress = None
		self.progressNeeded = progressNeeded

	def _set_progress(self, progress):
		if not isinstance(progress, Progress):
			raise TypeError(str(Progress)+' must be instance of Progress')
		self.progress = progress

	def __repr__(self):
		return self.reprMsg

	def __call__(self):
		if self.progressNeeded and self.progress is None:
			raise Exception('progress instance needed.')

class TimeWidget(Widget):
	def __init__(self, milisec=False, min=True, hour=True):
		Widget.__init__(self)
		self.milisec = milisec
		self.min = min
		self.hour = hour
		self._startTime = time.time()
		self.startTime = int(self._startTime)

	def calc_time(self):
		_now = time.time()
		now = int(_now)
		string = ''
		if self.milisec:
			milisec = str(_now - self._startTime).split('.')[1][:3]
		sec = now - self.startTime
		min = 0
		hour = 0
		if sec >= 60:
			for m in range(sec // 60):
				sec -= 60
				min += 1
		if min >= 60:
			for m in range(min // 60):
				min -= 60
				hour += 1
		if len(str(hour)) <= 1:
			hour = '0' + str(hour)
		if len(str(min)) <= 1:
			min = '0' + str(min)
		if len(str(sec)) <= 1:
			sec = '0' + str(sec)
		if self.hour:
			string += str(hour)+':'
		if self.min:
			string += str(min)+':'
		if self.milisec:
			sec = str(sec) + '.' + milisec
		string += str(sec)
		return string

	def __call__(self):
		Widget.__call__(self)
		return self.calc_time()

class BarWidget(Widget):
	def __init__(self, fill='█', empty='░', fillPerPercent=5, color=None):
		Widget.__init__(self, True)
		self.fill = fill
		self.empty = empty
		self.fpp = fillPerPercent
		self.color = color

	def __call__(self):
		Widget.__call__(self)
		return self.createBar()

	def createBar(self):
		perc = int(self.progress.calc_perc().split('.')[0])
		bar = ''
		filled = 0
		if perc >= self.fpp:
			for c in range(perc // self.fpp):
				bar += self.fill
				filled += 1
		for f in range(100//self.fpp-filled):
			bar += self.empty
		if self.color and verifyColor(self.color, False):
			bar = '-' + self.color + bar + '*end'

		return bar

class TaskWidget(Widget):
	def __init__(self, tasks={}):
		Widget.__init__(self, True)
		self.tasks = tasks
		self.checkTasks()
		self.percTasks = {}

	def checkTasks(self):
		for t in self.tasks:
			if t == 'perc':
				self.percTasks = self.tasks[t]

	def __call__(self):
		Widget.__call__(self)
		return calc_task()

	def calc_task(self):
		if self.percTasks:
			perc = int(self.progress.calc_true_perc())
			for p in self.percTasks:
				if perc <= p:
					return self.percTasks[p]
		return ''

class CallWidget(Widget):
	def __init__(self, call, progressNeeded=False):
		Widget.__init__(self, progressNeeded)
		self.call = call

	def __call__(self):
		Widget.__call__(self)
		if self.progressNeeded:
			return self.call(self.progress)
		else:
			return self.call()

class ValueWidget(Widget):
	def __init__(self, value):
		Widget.__init__(self)
		self.value = value

	def __call__(self):
		Widget.__call__(self)
		return self.value

class LockedDict(dict):
	def __delitem__(self, val):
		raise AttributeError('dict is locked.')

class Progress(object):
	_deafultForm = '($VAL/$MAX) $PERC% $MSG'

	def __init__(self, val=0, minVal=0, maxVal=100, msg='completed', msgForm=None, replaces=[], color=None, inline=False):
		self.val = val
		self.min = minVal
		self.max = maxVal
		self.msg = msg
		self.inline = inline
		self.color = color
		if not msgForm:
			self.msgForm = self.get_default_form()
		else:
			self.msgForm = msgForm
		if replaces:
			for r in replaces:
				if not isinstance(r[1], Widget):
					raise TypeError(str(r[1])+' must be instance of Widget')
				r[1]._set_progress(self)
			self.extraReplaces = replaces
		else:
			self.extraReplaces = []
		self.show()

	def show(self):
		replaces = self.getDefaultReplaces()
		msg = self.do_replace(replaces)
		if self.color and verifyColor(self.color, False):
			msg = '-' + self.color + msg + '*end'
		if self.inline:
			self.printInline(msg)
		else:
			printMsg(msg)

	def getDefaultReplaces(self):
		return [
					['$VAL', self.val],
					['$MIN', self.min],
					['$MAX', self.max],
					['$PERC', self.calc_perc()],
					['$TRUE_PERC', self.calc_true_perc()],
					['$MSG', self.msg]
					]

	def clear(self):
		printMsg('\r\x1b[K', end='')

	def printInline(self, msg):
		self.clear()
		printMsg(msg, end='')
		sys.stdout.flush()

	def write(self, msg=''):
		if self.inline:
			printMsg('\n' + msg)
		else:
			printMsg(msg)

	def newline(self):
		if self.inline:
			printMsg('')

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.newline()

	def get_default_form(self):
		return self._deafultForm

	def calc_perc(self):
		perc = str(100/self.max*self.val).split('.')
		perc[1] = perc[1][:3]
		return perc[0]+'.'+perc[1]

	def calc_true_perc(self):
		perc = str(100/self.max*self.val).split('.')[0]
		return perc

	def do_replace(self, rl):
		cf = self.msgForm if not hasattr(self, 'tempMsg') else self.tempMsg
		for r in rl:
			cf = cf.replace(r[0], str(r[1]))
		for r in self.extraReplaces:
			cf = cf.replace(r[0], str(r[1]()))
		if '$' in cf and not hasattr(self, 'tempMsg'):
			self.tempMsg = cf
			self.do_replace(rl)
		else:
			try:
				del self.tempMsg
			except: pass
			return cf

	def update(self, val):
		self.val = max(self.min, min(self.max, val))
		self.show()

	def next(self, val=1):
		self.val = max(self.min, min(self.max, self.val + val))
		self.show()

StepForm = ' Step $VAL of $MAX: $TASK'

class ProgressBar(Progress, BarWidget):
	def __init__(self, val=0, minVal=0, maxVal=100, msg='completed', msgForm=None, replaces=[], color=None, inline=False, fill='█', empty='░', fillPerPercent=5):
		BarWidget.__init__(self, fill=fill, empty=empty, fillPerPercent=fillPerPercent)
		Progress.__init__(self, val=val, minVal=minVal, maxVal=maxVal, msg=msg, msgForm=msgForm, replaces=replaces, color=color, inline=inline)
		self.progress = self

	def getDefaultReplaces(self):
		Progress.getDefaultReplaces(self) + [['$BAR', self.createBar()]]

class Database(object):
	def __getattribute__(self, val):
		try: return object.__getattribute__(self, val)
		except: return self.dict[val]

	def __setattr__(self, key, val):
		if str(key).startswith('_') or str(key) in ['append', 'add', 'remove','dict','list']: object.__setattr__(self, key, val)
		else: self.dict[key] = val

	def __delattr__(self, val):
		try: del self.dict[val]
		except: object.__delattr__(self, val)

	def __getitem__(self, val):
		return self.list[val] if type(val) == int else self.dict[val]

	def __setitem__(self, key, val):
		self.dict[key] = val

	def __delitem__(self, val):
		del self.dict[val]

	def __repr__(self):
		return str(object.__repr__(self)).replace(str(str(object.__repr__(self)).split()[0]), '<Database')

	def __init__(self, update=None):
		self.dict = {} if not type(update) == dict else update
		self.list = [] if not type(update) == list else update

	def append(self, val):
		self.list.append(val)

	def add(self, val):
		if len(str(val).split(':')) == 1:
			self.list.append(val)
		else:
			self.dict[str(val).split(':')[0]] = str(val).split(':')[1]

	def remove(self, val):
		self.list.remove(val)

class OptionsDatabase(Database):
	def __getitem__(self, val):
		return self.dict[val]

	def __repr__(self):
		return str(object.__repr__(self)).replace(str(str(object.__repr__(self)).split()[0]), '<OptionsDatabase')

	def __init__(self, update=None, rules=None):
		self.dict = {} if not type(update) == dict else update
		if rules and update:
			for o in rules:
				if not o['key'] in self.dict:
					self.dict[o['key']] = o.get('default', None)

class Str(str):
	def extract(self):
		splittedList = self.split(',')
		splittedDict = {}
		splittedListNew = []
		for i in splittedList:
			if len(i.split(':')) > 1:
				splittedDict[i.split(':')[0]] = i.split(':')[1]
		for i in splittedList:
			if len(i.split(':')) > 1:
				for s in i.split(':'):
					splittedListNew.append(s)
			else:
				splittedListNew.append(i)
		if len(splittedListNew) == 0 and len(splittedDict) == 0:
			raise ValueError('this string is not encoded.')
		else:
			data = Database()
			for i in splittedListNew:
				data.append(i)
			for i in splittedDict:
				data[i] = splittedDict[i]
			return data

	def __setitem__(self, index, val):
		stringList = []
		for string in self:
			stringList.append(string)
		stringList[index] = str(val)
		compiledString = ''
		for string in stringList:
			compiledString += string
		self = Str(compiledString)

	def __div__(self, other):
		out = []
		try:
			if len(self) > other:
				splitDelay = len(self) // other
				tStr = str(self)
				for i in range(splitDelay):
					out.append(tStr[:other])
					tStr = tStr[other:]
				if not tStr == '':
					out.append(tStr)
			else:
				out = [self]
		except:
			out = []
		return out

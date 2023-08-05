import setuptools, os, sys
fMap = open('prot/__init__.py').read().splitlines()
for i, m in enumerate(fMap):
	if m.startswith('__version__ = '):
		verS = m
		verI = i
		break
exec(verS)
vli = []
for vv in __version__:
	vli.append(vv)
if '--upgrade' in sys.argv:
	if int(vli[2]) == 9:
		vli[0] = str(int(vli[0]) + 1)
		vli[2] = str(0)
	else:
		vli[2] = str(int(vli[2]) + 1)
	sys.argv.remove('--upgrade')
ver = ''
for v in vli:
	ver += v
fMap[verI] = '__version__ = '+repr(ver)
ns = ''
for g in fMap:
	ns += g+'\n'
f = open('prot/__init__.py', 'w')
f.write(ns)
f.flush()
f.close()
if len(sys.argv) <= 1:
	sys.argv += ['sdist', 'bdist_wheel']
long_description = open('README.md').read() + '\n\n' + open('CHANGELOG.md').read()

setuptools.setup(
	name="prot",
	version=ver,
	description='A Simple Tool That Contains Advance Functions.',
	long_description=long_description, long_description_content_type='text/markdown',
	author="Alireza Poodineh",
	author_email='pa789892@gmail.com', url='https://www.pypi.org/user/Ali_p1986',
	keywords='ptools protools pip',
	packages=setuptools.find_packages(),
	entry_points={"console_scripts": ["prot=prot:prot", "ptools=prot:prot", "prot.pip=prot.pip:pip", "ptools.pip=prot.pip:pip"]})
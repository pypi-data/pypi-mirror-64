import numpy as np
import pandas as pd
import os
import re
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
valid_types = ['csv', 'xls', 'xlsx', 'txt']
excel_types = ['xls', 'xlsx']
csv_types = ['csv', 'txt']
dlm_default = '\t'

label_dict = {'v':'v', 'ma':'i', 'a':'i', 's':'t', 'mv':'v',
				'v vs. sce':'v', 'mv vs. sce':'v', 'v vs. she':'v', 'mv vs. she':'v'}
default_labels = ['tintin', 'snowy', 'haddock', 'calculus', 'castafiore', 'thomson', 'thompson']

def check_type(filetype):
	filetype = filetype.lower().replace('.', '')
	if filetype not in valid_types:
		raise ValueError('Supported filetypes ' + ', '.join(valid_types))
	return filetype

def check_list(var):
	return (type(var) == list) or (type(var) == np.ndarray)

def check_dict(var):
	return type(var) == dict

def check_scalar(var):
	try:
		len(var)
		return False
	except:
		return True

def check_labels(data):
	cols = [c.lower() for c in data.columns]
	newcols = [];
	for c in cols:
		try:
			units = c.split('/')[1]
			if units in label_dict.keys():
				newcols.append(label_dict[units])
			else:
				newcols.append(c)
		except:
			newcols.append(c)
	return newcols

def get_files(path=None, pattern='', filetype=''):
	files = os.listdir(path)
	if pattern:
		files = [f for f in files if re.match(pattern, f)]
	if filetype:
		filetype = filetype.lower().replace('.', '')
		files = [f for f in files if re.match(r'.*\.'+filetype, f)]
	return files

def read_file(filename, dlm=dlm_default):
	data = None
	name = None
	try:
		name = os.path.basename(filename)
		name, filetype = name.split('.')
		filetype = check_type(filetype)
		if filetype in excel_types:
			data = pd.read_excel(filename)
		elif filetype in csv_types:
			if filetype == 'csv':
				data = pd.read_csv(filename)
			elif filetype == 'txt':
				data = pd.read_csv(filename, delimiter=dlm)
		return name, data
	except:
		if not os.path.isdir(filename):
			logging.info(f'Unable to read {os.path.basename(filename)}')
	return name, data

def get_testdir():
	fcdir = os.path.dirname(os.path.realpath(__file__))
	datapath = os.path.join(fcdir, 'testdata')
	return datapath

def buildfilename(cellid, test, num=None, filetype='csv'):
	if num:
		filename = cellid + '_' + test + str(num) + '.' + filetype
	else:
		filename = cellid + '_' + test + '.' + filetype
	return filename

def testfun():
	return ', '.join(valid_types)
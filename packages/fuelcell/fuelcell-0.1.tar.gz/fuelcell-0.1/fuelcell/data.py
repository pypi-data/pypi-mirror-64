import numpy as np
import pandas as pd
import os
import re

import utils

dlm = utils.dlm_default

def load_data(filename=None, folder=None, pattern='', expttype='', delimiter=dlm, filetype=''):
	data = None
	if filename:
		data = utils.read_file(filename, delimiter)
	else:
		if folder:
			dirpath = os.path.realpath(folder)
		else:
			dirpath = os.getcwd()
		if expttype and not pattern:
			pattern = r'.*' + expttype + r'.*'
		files = utils.get_files(dirpath, pattern, filetype)
		data = dict()
		for f in files:
			path = os.path.join(dirpath, f)
			name, df = utils.read_file(path, delimiter)
			if df is not None:
				data[name] = df
		if len(data) == 1:
			data = list(data.values())[0]
	return data

def cv_raw(filename=None, folder=None, pattern='', delimiter=dlm):
	data = load_data(filename, folder, pattern, 'cv', delimiter)
	return data

def cp_raw(filename=None, folder=None, pattern='', delimiter=dlm):
	data = load_data(filename, folder, pattern, 'cp', delimiter)
	return data

def cv_process(data=None, area=5, current_column=1, filename=None, folder=None, pattern='', delimiter=dlm):
	if data is None:
		data = cv_raw(filename, folder, pattern, delimiter)
	if not utils.check_dict(data):
		data = {'key': data}
	newdata = dict()
	for k, df in data.items():
		newdf = df.copy()
		newdf.columns = utils.check_labels(newdf)
		if 'i' in newdf.columns:
			newdf['i'] = newdf['i'] / area
		else:
			newdf.iloc[:,current_column] = newdf.curr[:,current_column] / area
		newdata[k] = newdf
	if len(newdata) == 1:
		newdata = list(newdata.values())[0]
	return newdata

def cp_process(data=None, area=5, current_column=1, potential_column=2, aoi=True, filename=None, folder=None, pattern='', delimiter=dlm):
	if data is None:
		data = cp_raw(filename, folder, pattern, delimiter)
	if not utils.check_dict(data):
		data = {'key': data}
	newdata = dict()
	for k, df in data.items():
		newdf = df.copy()
		newdf.columns = utils.check_labels(newdf)
		# time = np.array(newdf['t'])
		if 'i' in newdf.columns and 'v' in newdf.columns:
			current = np.array(newdf['i'])
			potential = np.array(newdf['v'])
		else:
			current = np.array(newdf.iloc[:, current_column])
			potential = np.array(newdf[:, current_column])
		split_pts = findsteps(current, threshold=5)
		current_steps = split_and_filter(current, split_pts, min_length=100)
		potential_steps = split_and_filter(potential, split_pts, min_length=100)
		# time_steps = split_and_filter(potential, split_pts, min_length=100)
		current_avg = np.array([avg_last_pts(s) for s in current_steps])
		potential_avg = np.array([avg_last_pts(s) for s in potential_steps])
		if aoi:
			current_avg = avg_outside_in(current_avg)
			potential_avg = avg_outside_in(potential_avg)
		current_avg = current_avg / 5
		cp_processed = pd.DataFrame({'i':current_avg, 'v':potential_avg})
		newdata[k] = cp_processed
	if len(newdata) == 1:
		newdata = list(newdata.values())[0]
	return newdata

def findsteps(data, threshold=5):
	diffs = np.abs(np.diff(data))
	splits = np.where(diffs > threshold)[0] + 1
	return splits

def split_and_filter(data, split_pts, min_length=0):
	steps = np.split(data, split_pts)
	steps_tokeep = np.array([s for s in steps if len(s) > min_length])
	return steps_tokeep

def avg_last_pts(arr, numpts=300):
	avg = np.mean(arr[-numpts:])
	return avg

def avg_outside_in(arr):
	l = len(arr)
	avg = np.array([(arr[i]+arr[l-1-i])/2 for i in np.arange(l//2 + l%2)])
	return avg
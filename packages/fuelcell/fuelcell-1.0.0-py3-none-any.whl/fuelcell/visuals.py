import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import utils

def plot_cv(data=None, labels=None, line=True, scatter=True, current_column=1, potential_column=0, xunits='V', yunits=r'$mA/cm^2$', export_name=None, export_type='png', figsize=(5,5), dpi=600):
	"""
	Plots cyclic voltammetry files

	Function to plot data from one or more CV tests

	Parameters
	__________
	data : DataFrame or dict
		   Either a DataFrame containing CV data or a dict with CV DataFrames as
		   values
	labels : list
			 Currently unsupported. List of labels to be used in place of dict
			 keys
	line : bool
		   Unused; only present to maintain continuity of function signatures
	scatter : bool
			  Unused; only present to maintain continuity of function signatures
	current_column : int (default=1)
					 Index of the column with current data. Used if automatic
					 column label parsing fails
	potential_column : int (default=0)
					   Index of the column with potential data. Used if
					   automatic column label parsing fails
	xunits : str (default='V')
			 units to use in the x-axis label
	yunits : str (default=r'$mA/cm^2$')
			 units to use in the y-axis label
	export_name : str or path-like
				  Filename used to save the figure. If export_name is specified,
				  figure will be saved in the current directory (or specified
				  directory if pathlike)
	export_type : str (default='png')
				  Image type to save figure as. Only used if export_name is
				  specified and export_name does not include a filetype
	figsize : list or tuple (default=(5,5))
			  Figure dimensions (inches) if figure is to be exported. Only used
			  if export_name is specified
	dpi : int (default=600)
		  Resolution (dots per inch) of exported figure. Only used if
		  export_name is specified

	Returns
	_______
	Figure
		Object containing all plot elements
	Axes
		Object cotaining the plotted data
	"""
	if not utils.check_dict(data):
		data = {'key': data}
	if export_name:
		fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
	else:
		fig, ax = plt.subplots()
	for k, df in data.items():
		df.columns = utils.check_labels(df)
		if 'i' in df.columns and 'v' in df.columns:
			x = df['v']
			y = df['i']
		else:
			x = df.iloc[:, potential_column]
			y = df.iloc[:, current_column]
		ax.plot(x, y, label=k)
	if len(data) > 1:
		ax.legend(loc='best')
	ax.set_xlabel('Potential [' + xunits + ']')
	ax.set_ylabel(r'Current Density [' + yunits + ']')
	if export_name:
		export_type = export_type.replace('.', '')
		if len(export_name.split('.')) == 1:
			export_name = export_name + '.' + export_type
		plt.savefig(export_name)
	return fig, ax

def polcurve(data=None, labels=None, line=True, scatter=True, current_column=0, potential_column=1, xunits='V', yunits=r'$mA/cm^2$', export_name=None, export_type='png', figsize=(5,5), dpi=600):
	"""
	Plots polarization curves

	Function to plot polarization curves

	Parameters
	__________
	data : DataFrame or dict
		   Either a DataFrame a dict with CV DataFrames as values
	labels : list
			 Currently unsupported. List of labels to be used in place of dict
			 keys
	line : bool (default=True)
		   Specifies if a line connecting the points will be drawn
	scatter : bool (default=True)
			  Specifies if a marker will be drawn at each data point
	current_column : int (default=1)
					 Index of the column with current data. Used if automatic
					 column label parsing fails
	potential_column : int (default=0)
					   Index of the column with potential data. Used if
					   automatic column label parsing fails
	xunits : str (default='V')
			 units to use in the x-axis label
	yunits : str (default=r'$mA/cm^2$')
			 units to use in the y-axis label
	export_name : str or path-like
				  Filename used to save the figure. If export_name is specified,
				  figure will be saved in the current directory (or specified
				  directory if pathlike)
	export_type : str (default='png')
				  Image type to save figure as. Only used if export_name is
				  specified and export_name does not include a filetype
	figsize : list or tuple (default=(5,5))
			  Figure dimensions (inches) if figure is to be exported. Only used
			  if export_name is specified
	dpi : int (default=600)
		  Resolution (dots per inch) of exported figure. Only used if
		  export_name is specified

	Returns
	_______
	Figure
		Object containing all plot elements
	Axes
		Object cotaining the plotted data
	"""
	if not utils.check_dict(data):
		data = {'key': data}
	if export_name:
		fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
	else:
		fig, ax = plt.subplots()
	for k, df in data.items():
		df.columns = utils.check_labels(df)
		if 'i' in df.columns and 'v' in df.columns:
			y = df['v']
			x = df['i']
		else:
			y = df.iloc[:, potential_column]
			x = df.iloc[:, current_column]
		if line and scatter:
			ax.plot(x, y, label=k, marker='.')
		elif line:
			ax.plot(x, y, label=k)
		else: 
			ax.scatter(x, y, label=k)
	if len(data) > 1:
		ax.legend(loc='best')
	ax.set_xlabel('Potential [' + xunits + ']')
	ax.set_ylabel(r'Current Density [' + yunits + ']')
	ax.set_title('Polarization Curves')
	if export_name:
		export_type = export_type.replace('.', '')
		if len(export_name.split('.')) == 1:
			export_name = export_name + '.' + export_type
		plt.savefig(export_name)
	return fig, ax

def plot_general(data=None, labels=None, line=True, scatter=True, xcolumn=0, ycolumn=1, xlabel='x', ylabel='y', export_name=None, export_type='png', figsize=(5,5), dpi=600):
	"""
	General plotting function

	Function to plot any data you like

	Parameters
	__________
	data : DataFrame or dict
		   Either a DataFrame a dict with CV DataFrames as values
	labels : list
			 Currently unsupported. List of labels to be used in place of dict
			 keys
	line : bool (default=True)
		   Specifies if a line connecting the points will be drawn
	scatter : bool (default=True)
			  Specifies if a marker will be drawn at each data point
	xcolumn : int (default=1)
			  Index of the column containing x values
	ycolumn : int (default=1)
			  Index of the column containing y values
	xlabel : str (default='x')
			 x-axis label
	ylabel : str (default='y')
			 y-axis label
	export_name : str or path-like
				  Filename used to save the figure. If export_name is specified,
				  figure will be saved in the current directory (or specified
				  directory if pathlike)
	export_type : str (default='png')
				  Image type to save figure as. Only used if export_name is
				  specified and export_name does not include a filetype
	figsize : list or tuple (default=(5,5))
			  Figure dimensions (inches) if figure is to be exported. Only used
			  if export_name is specified
	dpi : int (default=600)
		  Resolution (dots per inch) of exported figure. Only used if
		  export_name is specified

	Returns
	_______
	Figure
		Object containing all plot elements
	Axes
		Object cotaining the plotted data
	"""
	if not utils.check_dict(data):
		data = {'key': data}
	if export_name:
		fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
	else:
		fig, ax = plt.subplots()
	for k, df in data.items():
		x = df.iloc[:, xcolumn]
		y = df.iloc[:, ycolumn]
		if line and scatter:
			ax.plot(x, y, label=k, marker='.')
		elif line:
			ax.plot(x, y, label=k)
		else: 
			ax.scatter(x, y, label=k)
	if len(data) > 1:
		ax.legend(loc='best')
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	ax.set_title('Polarization Curves')
	if export_name:
		export_type = export_type.replace('.', '')
		if len(export_name.split('.')) == 1:
			export_name = export_name + '.' + export_type
		plt.savefig(export_name)
	return fig, ax

def plot_cp_raw(data=None, labels=None, line=True, scatter=True, current_column=2, potential_column=1, time_column=0, xunits='s', yunits=('mA', 'V'), export_name=None, export_type='png', figsize=(5,5), dpi=600):
	"""
	Plots raw chronopotentiometery data

	Function to plot cp data as it would appear in EC lab.

	Parameters
	__________
	data : DataFrame or dict
		   Either a DataFrame a dict with CV DataFrames as values. Using a dict
		   is supported to preserve continuity accross all visualization 
		   functions, but it is strongly reccomended to pass in a single
		   DataFrame for visual clarity
	labels : list
			 Currently unsupported. List of labels to be used in place of dict
			 keys
	line : bool (default=True)
		    Unused; only present to maintain continuity of function signatures
	scatter : bool (default=True)
			   Unused; only present to maintain continuity of function
			   signatures
	current_column : int (default=2)
					 Index of the column with current data. Used if automatic
					 column label parsing fails
	potential_column : int (default=1)
					   Index of the column with potential data. Used if
					   automatic column label parsing fails
	time_column : int (default=0)
				  Index of the column with time data. Used if automatic column
				  label parsing fails
	xunits : str (default='V')
			 units to use in the x-axis label
	yunits : tuple or list (default=('mA', 'V'))
			 units to use in the y-axis labels.
			 Passed in the order('current units', 'potential units')
	export_name : str or path-like
				  Filename used to save the figure. If export_name is specified,
				  figure will be saved in the current directory (or specified
				  directory if pathlike)
	export_type : str (default='png')
				  Image type to save figure as. Only used if export_name is
				  specified and export_name does not include a filetype
	figsize : list or tuple (default=(5,5))
			  Figure dimensions (inches) if figure is to be exported. Only used
			  if export_name is specified
	dpi : int (default=600)
		  Resolution (dots per inch) of exported figure. Only used if
		  export_name is specified

	Returns
	_______
	Figure
		Object containing all plot elements
	tuple
		tuple of two Axes objects: one each for the potential vs. time and 
		current vs. time plots
	"""
	if not utils.check_dict(data):
		data = {'key': data}
	if export_name:
		fig, ax1 = plt.subplots(figsize=figsize, dpi=dpi)
	else:
		fig, ax1 = plt.subplots()
	ax2 = ax1.twinx()
	color1 = 'tab:red'
	color2 = 'tab:blue'
	for k, df in data.items():
		if 'i' in df.columns and 'v' in df.columns and 't' in df.columns:
			x = df['t']
			y1 = df['i']
			y2 = df['v']
		else:
			x = df.iloc[:, time_column]
			y1 = df.iloc[:, current_column]
			y2 = df.iloc[:, potential_column]
		ax1.scatter(x, y1, s=1, color=color1, label=k)
		ax2.scatter(x, y2, s=1, color=color2, label=k)
	if len(data) > 1:
		ax1.legend(loc='best')
	# color = 'tab:red'
	ax1.set_xlabel('Potential [' + xunits + ']')
	ax1.set_ylabel('Current Density [' + yunits[0] + ']')
	ax2.set_ylabel('Potential [' + yunits[1] + ']')
	ax1.tick_params(axis='y', labelcolor=color1)
	ax2.tick_params(axis='y', labelcolor=color2)
	if export_name:
		export_type = export_type.replace('.', '')
		if len(export_name.split('.')) == 1:
			export_name = export_name + '.' + export_type
		plt.savefig(export_name)
	return fig, (ax1, ax2)
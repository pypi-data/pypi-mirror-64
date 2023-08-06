import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import utils

def plot_cv(data=None, labels=None, line=True, scatter=True, potential_column=0, current_column=1, xunits='V', yunits=r'$mA/cm^2$', export_name=None, export_type='png', figsize=(5,5), dpi=600):
	if not utils.check_dict(data):
		data = {'key': data}
	if export_name:
		fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
	else:
		fig, ax = plt.subplots()
	for k, df in data.items():
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

def plot_cp_raw(data=None, scatter=True, export_name=None, export_type='png', figsize=(5,5), dpi=600):
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
		x = df['t']
		y1 = df['i']
		y2 = df['v']
		ax1.scatter(x, y1, s=1, color=color1, label=k)
		ax2.scatter(x, y2, s=1, color=color2, label=k)
	if len(data) > 1:
		ax1.legend(loc='best')
	# color = 'tab:red'
	ax1.set_xlabel('Time [s]')
	ax1.set_ylabel('Current [mA]')
	ax1.tick_params(axis='y', labelcolor=color1)
	# color = 'tab:blue'
	ax2.set_ylabel('Potential [V]')
	ax2.tick_params(axis='y', labelcolor=color2)
	if export_name:
		export_type = export_type.replace('.', '')
		if len(export_name.split('.')) == 1:
			export_name = export_name + '.' + export_type
		plt.savefig(export_name)
	return fig, ax1, ax2

def polcurve(data=None, labels=None, line=True, scatter=True, potential_column=0, current_column=1, xunits='V', yunits=r'$mA/cm^2$', export_name=None, export_type='png', figsize=(5,5), dpi=600):
	if not utils.check_dict(data):
		data = {'key': data}
	if export_name:
		fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
	else:
		fig, ax = plt.subplots()
	for k, df in data.items():
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

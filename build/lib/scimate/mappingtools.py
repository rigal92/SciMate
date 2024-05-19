import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats  import chisquare
from matplotlib.widgets import Slider
import matplotlib.pyplot as plt 


def pol0(x,a0):
	return a0
def pol1(x,a0,a1):
	return a0 + a1 *x
def pol2(x,a0,a1,a2):
	return a0 + a1 * x + a2 * x**2




def chiTest(x,y, background, p0 = None):
	"""
	Fits the data using background and return reduce chi square value.

	Input
	-----------------------------------------------------------------
	x,y: arraylike 
	background: callable
		fitting function 
	"""
	popt,_ = curve_fit(background,x,y, p0 = p0)
	n = len(y) - 1 - len(popt)
	return chisquare(background(x,*popt),y)[0]/n


def test_dataset(df, chi_threshold, background, p0 = None):
	"""
	Test dataset where first column is the x axis and the others are
	one spectrum per column. Only specra where the fit "fails" 
	(chi higher then threshold) are accepted.

	Input
	-----------------------------------------------------------------
	data: DataFrame
	chi_threshold: float
		minimum value of accepted chi square 
	background: callable
		fitting function
	p0: float
		initial parameters for fitting

	Return
	-----------------------------------------------------------------
	DataFrame:
		Dataframe containg the x values as the first columns and the 
		accepted y values

	"""
	x = df.iloc[:,0]

	df_out = pd.DataFrame()

	df_out["x"] = x
	index = []

	for i,col in enumerate(df.iloc[:,1:]):
		y = df[col]
		chi = chiTest(x, y, background, p0)
		if(chi > chi_threshold):
			df_out[col] = y
			index += [i]

	return df_out,index



def sliderplot(data, ax = None):
	"""
	Plot columns of dataframe with a slider. First column is the x 
	axis.
	"""
	def col_select(index):
		ax.set_ydata(data.iloc[:,index])
		ax.figure.canvas.draw_idle()

	if ax == None:
		ax = plt.axes()

	x = data.iloc[:,0]

	# initialize plot
	line, = plt.plot(x,data.iloc[:,1])
		
	slider = Slider(ax,"index",1, len(data.columns), 1, valstep = 1)
	slider.on_changed(col_select)
	return ax


# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# PLOTTING
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------


def contourf_simple(x, y, z, nx, ny, ax = None, fig=None, cbar = True, **kwargs):
	"""
	Contour plot using 1D arrays instead of 2D.
	
	Input
	-----------------------------------------------------------------
	x, y, z: 1D array
	**kwargs:
		arguments to pass to contourf

	Return
	-----------------------------------------------------------------
	matplotlib.contour.QuadContourSet

	"""

	x,y,z = (i.values.reshape(ny,nx) for i in (x,y,z))

	if(ax):
		cp = ax.contourf(x, y, z, **kwargs)
	else:
		cp = plt.contourf(x, y, z, **kwargs)


	if (cbar):
		if(not fig):
			print("WARNING: Missing figure argument. The colorbar can not be plotted!")
		else:
			fig.colorbar(cp)
			fig.tight_layout()

	return cp






def contour_simple(x, y, z, nx, ny, ax = None, fig=None, cbar = True, **kwargs):
	"""
	See contourf_simple

	"""

	x,y,z = (i.values.reshape(ny,nx) for i in (x,y,z))

	if(ax):
		cp = ax.contour(x, y, z, **kwargs)
	else:
		cp = plt.contour(x, y, z, **kwargs)


	if (cbar):
		if(not fig):
			print("WARNING: Missing figure argument. The colorbar can not be plotted!")
		else:
			fig.colorbar(cp)
			fig.tight_layout()

	return cp






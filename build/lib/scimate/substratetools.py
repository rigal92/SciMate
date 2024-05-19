import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def FPreflected(wl, n1, n2 , d):
	"""
	Returns the intensity of the reflected light from parallel plates
	(Fabry-Perrot) with a medium of dielectric constant n2 between. 

	Input s
	-----------------------------------------------------------------
	wl: float
		wavelenght
	n1: float
		refractive index of the medium outside
	n2: float
		refractive index of the medium inside
	d: float
		separation

	Returns
	-----------------------------------------------------------------
	float:
		intensity value

	"""
	r = (n1 - n2) / (n1 + n2)
	g = 4 * r **2 /(1- r **2) **2
	delta = 2 * np.pi * n2 * 2 * d / wl
	return g ** 2 * (np.sin(delta/2)) ** 2 /(1 + g**2 * (np.sin(delta/2))**2)

def gasketthickness(n1, n2 , dWL):
	"""
	Compute the gasket thickness from the separation between the 
	fringes in the DAC for whitelight. 

	Input
	-----------------------------------------------------------------
	n1: float
		refractive index of the medium outside
	n2: float
		refractive index of the medium inside
	dWL: float
		separation between the fringes
	Return
	-----------------------------------------------------------------
	float:
		gasket thickness

	"""

	return g ** 2 * (np.sin(delta/2)) ** 2 /(1 + g**2 * (np.sin(delta/2))**2)





if __name__ == "__main__":
	x = np.arange(532,550,.01)/1000
	y = FPreflected(x,2.4,1.5,100)
	plt.plot(x,y,".-")
	# plt.plot(1e2*(1/532-1/x),y,".-")
	plt.show()

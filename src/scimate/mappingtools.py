import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats  import chisquare
from sklearn.metrics.pairwise import pairwise_distances_argmin
from scipy.stats import pearsonr
from scipy.signal import savgol_filter

def pol0(x,a0):
    return a0
def pol1(x,a0,a1):
    return a0 + a1 *x
def pol2(x,a0,a1,a2):
    return a0 + a1 * x + a2 * x**2

def read_map(filename, file_format="jasco"):
    """
    Read a map file.

    Input
    -----
    filename: str
        name of the file
    file_format: str, default="jasco"
        defines the format of the file to read
        Accepted values:
            "jasco": Jasco spectrometer
    Return
    ------
    pd.DataFrame: 
        data (Multicolumns header with xcoord,ycoord) 
    """
    if file_format == "jasco":
        i=0
        with open(filename) as f:
            while(f.readline().startswith("XPOSITION")==False):
                i+=1
        df = pd.read_table(filename, header = [i,i+1])
        return df


def match_template(data_y, template_data, metric="sqeuclidean", normalize=True, smooth=True, baseline=True):
    """
    Finds the spectrum in template_data that is most similar to each one in 
    data_y. Metric is the method used for the matching.

    Input
    ------
    data_y: np.array (n_spectra, spectrum_y)
        the spectra to be matched
    template_data: np.array (n_spectra, spectrum_y)
        the template spectra used for matching
    metric: str, default="sqeuclidean"
        the metric used to calculate the distances.
        Possible values:
        - from manual implementation:
            ['pearsonr']

        - from scikit-learn: ['cityblock', 'cosine', 'euclidean', 'l1', 'l2',
         'manhattan', 'nan_euclidean']

        - from :mod:`scipy.spatial.distance`: ['braycurtis', 'canberra', 'chebyshev',
          'correlation', 'dice', 'hamming', 'jaccard', 'kulsinski',
          'mahalanobis', 'minkowski', 'rogerstanimoto', 'russellrao',
          'seuclidean', 'sokalmichener', 'sokalsneath', 'sqeuclidean',
          'yule']
    baseline: bool, default=True
        remove a costant baseline before computing the distance
    smooth: bool, default=True
        smooth data before computing the distance
    normalize: bool, default=True
        normalize the data before computing the distance
    Return
    ------
    numpy.array
        array of closest matches of template_data for each data_y
    """
    if baseline:
        template_data = np.array([s-s.min()for s in template_data])
        data_y = np.array([s-s.min()for s in data_y])
    if smooth:
        win = 50
        template_data = savgol_filter(template_data, window_length=win, polyorder=2, mode='interp')
        data_y = savgol_filter(data_y, window_length=win, polyorder=2, mode='interp')
    if normalize:
        template_data = np.array([s/s.max()for s in template_data])
        data_y = np.array([s/s.max()for s in data_y])

    #compute distance
    if metric == "pearsonr":
        return np.array([np.argmin([1 - pearsonr(y, ref)[0] for ref in template_data]) for y in data_y]) 
    else:
        return pairwise_distances_argmin(data_y, template_data, metric=metric)


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



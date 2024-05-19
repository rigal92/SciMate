import numpy as np 
import pandas as pd


def normalize(data,ref = None):
    """
    Normalize data to its maximum value. Ref can be used to notmalize to the maximum of a specific column of a DataFrame.

    Input
    -----------------------------------------------------------------
    data: array, DataFrame
        data to be normalized.
    ref: None or string, default None
        for DataFrames a specific column can be selected giving the column name in ref. If None is given the maximumm of the data frame will be used.

    """

    if(isinstance(data,pd.DataFrame)):
        if(ref is None):
            return data/data.max(axis = None)
        else:
            try:
                return data/data[ref].max(axis = None)
            except KeyError as er:
                print("Impossible to normalize the data, key not found in the DataFrame.",er)
                return None

    else:
        return data/data.max(axis = None)

def lorentzian(x,x0,A,HWHM):
    return A/(1+(x-x0)**2/HWHM**2)


# -----------------------------------------------------------------
#Tests
# -----------------------------------------------------------------
if __name__ == '__main__':
    #testing example
    import matplotlib.pyplot as plt
    x = np.arange(40)
    a1 = 100
    a2 = 200
    x01 = 20
    x02 = 10
    y1 = a1/(1 + (x-x01)**2)
    y2 = a2/(1 + (x-x02)**2)
    normalize = "y1"

    df = pd.DataFrame({"x":x,"y1":y1,"y2":y2})
    dd = normalize(df.iloc[:,1:],normalize)
    if(dd is not None):
        plt.plot(x,dd)
        plt.show()

import numpy as np 
import pandas as pd

def break_axis(axes, direction = "x"):
    """
    Insert brake axis slashes to join axes along one direction. 
    -----------------------------------------------------------------

    Inputs
    -------
    axes: array-like
        Array of axes to edit
    direction: {'x','y'}, default: 'x'
        allowed values are 'x' and 'y' indicating which axis will be 
        modified

    """


    d = .5  # proportion of vertical to horizontal extent of the slanted line (angle of the slanted line)
    if(direction == "x"):
        l = ["right","left"]
        [a.tick_params('y',length = 0) for a in axes[1:]]
        [a.tick_params('y',length = 0) for a in axes[1:]]
        marker = [(-d, -1), (d, 1)]
        slanted_positions = [
             [[1,1],[0,1]],
             [[0,0],[0,1]],
        ]

    else:
        l = ["bottom","top"]
        [a.tick_params('x',length = 0) for a in axes[:-1]]
        marker = [(-1, -d), (1, d)]
        slanted_positions = [
             [[0,1],[0,0]],
             [[0,1],[1,1]],
        ]


    kwargs = dict(marker=marker, markersize=12,
                  linestyle="none", color='k', mec='k', mew=1, clip_on=False)



    axes[0].spines[l[0]].set_visible(False)
    axes[0].plot(*slanted_positions[0], transform=axes[0].transAxes, **kwargs)
    axes[-1].spines[l[1]].set_visible(False)
    axes[-1].plot(*slanted_positions[1], transform=axes[-1].transAxes, **kwargs)
    for i in axes[1:-1]:
        i.spines[l[0]].set_visible(False)
        i.spines[l[1]].set_visible(False)
        i.plot(*slanted_positions[0], transform=i.transAxes, **kwargs)
        i.plot(*slanted_positions[1], transform=i.transAxes, **kwargs)

    axes[0].figure.subplots_adjust(wspace=(len(axes) - 1) * 0.05, hspace=(len(axes) - 1) * 0.05)



# -----------------------------------------------------------------
#Tests
# -----------------------------------------------------------------
if __name__ == '__main__':
    #testing example
    import matplotlib.pyplot as plt
    x = np.arange(40)
    
    # test 2 plots    
    fig,axs = plt.subplots(1, 5, sharey=True, figsize = (9,6))
    for i,a in enumerate(axs):
        a.plot(x + i*100, x * (-1) ** (i%2))
    break_axis(axs)


    # test multiple plots    
    fig,axs = plt.subplots(2,1, sharex=True, figsize = (9,6))
    for i,a in enumerate(axs):
        a.plot(x * (-1) ** (i%2), -1*(x + i*100))
    break_axis(axs,'y')

    plt.show()

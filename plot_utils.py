"""
Basic plot utils
"""
''' --------------------------------------------------------------------------------------- '''

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as plticker

''' --------------------------------------------------------------------------------------- '''
def default_plot_settings(font_size=6, font_weight='bold'):
    plt.rcParams["font.size"] = font_size
    plt.rcParams["font.weight"] = font_weight
    plt.rcParams['lines.linewidth'] = 1
    plt.rcParams["legend.loc"] = 'upper left'
    return

def format_plot(ax, title, ylim=None, style=None, yscale=None,
                x_interval=1, y_interval=None, x_format='%b'):
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=x_interval))
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
    ax.xaxis.set_major_formatter(mdates.DateFormatter(x_format))
    ax.tick_params(axis='both', which='major', labelsize=6)
    if ylim is not None:  ax.set_ylim(ylim)
    if style is not None: ax.ticklabel_format(axis='y', style=style, scilimits=(0,0))
    if yscale == 'log': ax.set_yscale('log')
    ax.set_title(title, fontsize=6, fontweight='bold')
    ax.grid(True)
    ax.legend()

    # ylims = ax.get_ylim()
    # y0 = math.floor(ylims[0] * 100)/100.0
    # y1 = math.ceil(ylims[1] * 100) / 100.0
    # ax.yaxis.set_major_locator(plticker.MultipleLocator(base=(y1-y0)/10))
    # ax.yaxis.set_major_locator(plticker.LinearLocator(numticks=10))
    if y_interval is not None:
        ax.yaxis.set_major_locator(plticker.MultipleLocator(base=y_interval))

    return
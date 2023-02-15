"""
Basic plot utils
"""
''' --------------------------------------------------------------------------------------- '''

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

''' --------------------------------------------------------------------------------------- '''
def default_plot_settings(font_size=6, font_weight='bold'):
    plt.rcParams["font.size"] = font_size
    plt.rcParams["font.weight"] = font_weight
    plt.rcParams['lines.linewidth'] = 1
    return

def format_plot(ax, title, ylim=None, style=None, yscale=None, x_interval=1):
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=x_interval))
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.tick_params(axis='both', which='major', labelsize=6)
    ax.set_title(title, fontsize=6, fontweight='bold')
    ax.grid(True)
    ax.legend()
    if ylim is not None:  ax.set_ylim(ylim)
    if style is not None: ax.ticklabel_format(axis='y', style=style, scilimits=(0,0))
    if yscale == 'log': ax.set_yscale('log')
    return
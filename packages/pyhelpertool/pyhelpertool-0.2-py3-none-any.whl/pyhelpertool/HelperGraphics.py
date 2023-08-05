import matplotlib.pyplot as plt
import seaborn as sns

def set_rcparams(width=6.69291, fontsize=16, for_article=True, for_beamer=False):
    """
    Setting rcparams of matplotlib ready for publishing
    """

    height = width / 1.618

    if for_article or for_beamer:
        params = {
            #'backend': 'pdf',
            'axes.labelsize': fontsize,
            'font.size': fontsize,
            'figure.figsize': (width, height),
            'legend.fontsize': fontsize,
            'axes.titlesize': fontsize,
            'xtick.labelsize': fontsize,
            'ytick.labelsize': fontsize,
            'xtick.major.pad': fontsize,
            'xtick.major.pad': fontsize,
            'text.usetex': True,
            'font.sans-serif' : 'Helvetica Neue',
            'font.family': 'sans-serif',
            'image.cmap' : 'viridis',
            'image.interpolation'  : 'bilinear',
            'image.resample'  : False }
            #'font.serif': 'Times New Roman',
            #'font.sans-serif': 'Times New Roman'}
#            'ps.usedistiller': 'xpdf'}

    if for_beamer:
#       params['font.family'] = 'sans-serif'
        preamble = r'''\usepackage[cm]{sfmath}'''
        plt.rc('text.latex', preamble=preamble)

    if for_article or for_beamer:
        plt.rcParams.update(params)

def set_style():
    # This sets reasonable defaults for font size for
    # a figure that will go in a paper
    sns.set_context("paper")

    # Set the font to be serif, rather than sans
    sns.set(font='serif',style="ticks")

    # Make the background white, and specify the
    # specific font family
    sns.set_style("white", {
        "font.family": "serif",
        "font.serif": ["Times", "Palatino", "serif"]
    })
    sns.set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})
    sns.set_style({"xtick.direction": "in","ytick.direction": "in"})

def set_size(fig):
    fig.set_size_inches(8, 5)
    fig.tight_layout()

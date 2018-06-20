import numpy as np


def calc_opacity(v, logtau, vref, aux):
    """ Calculate Cobolev Opacity as in eq 2 of http://iopscience.iop.org/article/10.1086/658673/pdf"""
    opacity = logtau * (float(vref) - v) / aux

    return opacity

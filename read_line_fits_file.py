from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np


lineDirectory = '/Users/danmuth/local/share/es/lines/'
hdulist = fits.open(lineDirectory + 'line.kurucz.0100.fits')

hdulist.info()

hdu = hdulist[0]
hdu1 = hdulist[1]


def column(matrix, i):
    return [row[i] for row in matrix]

plt.plot(column(hdu1.data, 0))

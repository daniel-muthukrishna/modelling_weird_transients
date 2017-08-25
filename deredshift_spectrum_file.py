"""
Usage:
    python deredshift_spectrum_file.py FILENAME REDSHIFT

Example:
    python deredshift_spectrum_file.py spectrum_file.dat 0.12
"""

import numpy as np
import sys
from scipy.signal import medfilt


def read_file(filename):
    spectrum = np.loadtxt(filename)
    wave = spectrum[:,0]
    flux = spectrum[:,1]
    if np.shape(spectrum)[1] == 3:
        fluxErr = spectrum[:,2]
    elif np.shape(spectrum)[1] == 2:
        fluxErr = flux * 0.03  # Set Error to 3% of flux if there is no 3rd column
    return wave, flux, fluxErr


def deredshift_spectrum(wave, z):
    waveRest = wave/(z+1)

    return waveRest


def normalise_flux(flux, fluxErr):
    print(flux)

    fluxNorm = 4 * (flux - min(flux)) / (max(flux) - min(flux))
    fluxNormErr = 4 * fluxErr / (max(flux) - min(flux))

    return fluxNorm, fluxNormErr


def smooth_spectrum(flux, filterSize):
    smoothedFlux = medfilt(flux, kernel_size=filterSize)

    return smoothedFlux


def save_spectrum_file(outFilename, outWave, outFlux, outFluxErr):
    outArray = np.array([outWave, outFlux, outFluxErr]).transpose()
    print(outArray)
    np.savetxt(outFilename, outArray)


def make_rest_spectrum_file(inFilename, outFilename, z, smooth=3):
    wave, flux, fluxErr = read_file(inFilename)
    waveRest = deredshift_spectrum(wave, z)
    # fluxNorm, fluxNormErr = normalise_flux(flux, fluxErr)
    smoothedFlux = smooth_spectrum(flux, smooth)
    smoothedFluxNorm, fluxNormErr = normalise_flux(smoothedFlux, fluxErr)
    save_spectrum_file(outFilename, waveRest, smoothedFluxNorm, fluxNormErr)

    import matplotlib.pyplot as plt
    plt.figure()
    # plt.plot(wave, flux)
    plt.plot(wave, flux)
    # plt.errorbar(wave, flux, yerr=fluxErr)

    plt.figure()
    plt.plot(waveRest, smoothedFluxNorm)
    # plt.errorbar(waveRest, fluxNorm, yerr=fluxNormErr)
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) == 3 or len(sys.argv) == 4:
        inFile = str(sys.argv[1])
        try:
            redshift = float(sys.argv[2])
        except ValueError:
            print("Error: Invalid redshift argument. Redshift must be a float")
            exit(1)
        if len(sys.argv) == 4:
            smooth = int(sys.argv[3])
        else:
            smooth = 1
        extension = inFile.split('.')[-1]
        outFile = "{0}_restFrame_smooth{1}.{2}".format(inFile.strip("."+extension), smooth, extension)
        try:
            make_rest_spectrum_file(inFile, outFile, redshift, smooth)
        except:
            print("Error: Invalid input file")
            exit(1)
        if len(sys.argv) == 4:
            smooth = int(sys.argv[3])
    else:
        print("Enter only two or three arguments: filename redshift smooth")

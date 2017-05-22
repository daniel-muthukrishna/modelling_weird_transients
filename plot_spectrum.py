import numpy as np
import matplotlib.pyplot as plt


def read_file(filename):
    spectrum = np.loadtxt(filename)
    wave = spectrum[:,0]
    flux = spectrum[:,1]
    fluxErr = spectrum[:,2]

    return wave, flux, fluxErr


def plot_spectrum(filename, label=''):
    wave, flux, fluxErr = read_file(filename)
    plt.plot(wave, flux, label=label)
    plt.xlabel("Wavelength ($\AA$)")
    plt.ylabel("Relative Flux")
    plt.title(filename)
    #plt.errorbar(wave, flux, yerr=fluxErr)
    if label is not None:
        plt.legend()

    return

if __name__ == "__main__":
    # plt.figure()
    # plot_spectrum("demo.dat")
    # plot_spectrum("demo.fit")
    # plt.savefig("demo.png")

    plt.figure()
    plot_spectrum("DES16X3bdj_VLT_20160924_rest_frame.txt")
    plot_spectrum("DES16X3bdj_VLT_20160924.fit")
    plot_spectrum("DES16X3bdj_VLT_20160924.txt")
    plt.savefig("DES16X3bdj_VLT_20160924.png")

    plt.figure()
    plot_spectrum("DES16C2ayx_2016sep24_rest_frame.txt", label="Smoothed Spectrum")
    plot_spectrum("DES16C2ayx_2016sep24.fit", label="Fit from non-smoothed spectrum")
    plot_spectrum("DES16C2ayx_2016sep24_smoothed7.fit", label="Fit from smoothed spectrum")
    plt.savefig("DES16C2ayx_2016sep24.png")

    plt.show()
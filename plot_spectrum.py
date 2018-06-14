import numpy as np
import matplotlib.pyplot as plt
import os


def read_file(filename):
    spectrum = np.loadtxt(filename)
    if spectrum != []:
        wave = spectrum[:, 0]
        flux = spectrum[:, 1]
        fluxErr = spectrum[:, 2]
    else:
        wave, flux, fluxErr = np.zeros(2), np.zeros(2), np.zeros(2)

    return wave, flux, fluxErr


def plot_spectrum(filename, label='', legendNCol=1, title='', vOffset=0, yLabel='Relative Flux', bbox_to_anchor=None, loc=0):
    wave, flux, fluxErr = read_file(filename)
    plt.plot(wave, flux+vOffset, label=label)
    plt.xlabel("Wavelength ($\AA$)")
    plt.ylabel(yLabel)
    plt.title(title)
    #plt.errorbar(wave, flux, yerr=fluxErr)
    if label is not None:
        plt.legend(ncol=legendNCol, bbox_to_anchor=bbox_to_anchor, loc=loc)

    return

if __name__ == "__main__":
    # directory = "Saved_Fits/DES16X3bdj_VLT_20160924/"
    # plt.figure()
    # plot_spectrum(os.path.join(directory, "DES16X3bdj_VLT_20160924_rest_frame.txt"))
    # plot_spectrum(os.path.join(directory, "DES16X3bdj_VLT_20160924.fit"))
    # # plot_spectrum(os.path.join(directory, "all_ions.fit"))
    # for ionName in ['HI', 'BI']:
    #     plot_spectrum(os.path.join(directory, "{0}.fit".format(ionName)))
    # # plt.savefig(os.path.join(directory, "DES16X3bdj_VLT_20160924.png"))

    directory = "Saved_Fits/DES16X3bdj_VLT_20160924/"
    plt.figure()
    plot_spectrum(os.path.join(directory, "DES16X3bdj_VLT_20160924_restFrame_smooth3.txt"))
    plot_spectrum(os.path.join(directory, "DES16X3bdj_VLT_20160924.fit"))
    plot_spectrum(os.path.join(directory, "all_ions.fit"))
    # plt.savefig(os.path.join(directory, "DES16X3bdj_AAT_20161125.png"))

    # plt.figure()
    # plot_spectrum("DES16C2ayx_2016sep24_rest_frame.txt", label="Smoothed Spectrum")
    # plot_spectrum("DES16C2ayx_2016sep24_fewer.fit", label="Fit from non-smoothed spectrum")
    # # plot_spectrum("DES16C2ayx_2016sep24_smoothed7.fit", label="Fit from smoothed spectrum")
    # # plot_spectrum("DES16C2ayx_2016sep24.txt")
    # plt.savefig("DES16C2ayx_2016sep24.png")

    plt.show()

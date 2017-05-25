import numpy as np
import csv

SETUP_PARAMETERS = ["a0", "a1", "a2", "v_phot", "v_out", "t_phot"]
OPACITY_PROFILE_PARAMETERS = ["log_tau", "v_min", "v_max", "aux", "temp"]
LIST_OF_IONS = [601,    800,   1100,   1201,   1401,   1402,   1601,   2001,   2601,   2602,   2701,   2801]
X = "[ 5.44e-01 -3.99e-01  1.08e+00  1.29e+01  3.00e+01  9.23e+00  1.15e+00 -1.33e+00 -1.52e-01  5.78e-01  4.00e+00  1.07e+00  7.55e-01  2.24e+00 -2.86e+00  2.03e+00 -1.20e+00 -2.55e+00  1.29e+01  1.29e+01  1.29e+01  1.29e+01  1.29e+01  1.29e+01  1.29e+01  1.29e+01  1.29e+01  1.29e+01  1.29e+01  1.29e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  7.49e-01  9.20e+00  6.05e+00  1.12e+00  3.50e-01  1.07e+00  1.52e+00  4.54e-01  6.10e-01  5.30e-01  2.39e-01  4.75e-01  3.50e+01  4.20e+00  2.09e+00  2.00e+00  8.13e+00  1.38e+01  1.40e+01  2.54e+01  1.00e+01  2.26e+01  8.58e+00  1.21e+01 ]"


def read_synapps_solution(xStr):
    """ x is a string of a list without spaces instead of commas separating floating point values """

    setupInfo = {}
    ionInfo = {}
    numOfIons = len(LIST_OF_IONS)
    numOfSetupParams = len(SETUP_PARAMETERS)
    numOfOpacityParams = len(OPACITY_PROFILE_PARAMETERS)

    xArray = xStr.strip('[').strip(']').split()
    for i in range(numOfSetupParams):
        setupInfo[SETUP_PARAMETERS[i]] = xArray[i]

    ionVals = xArray[numOfSetupParams:]
    for i in range(numOfIons):
        ionName = LIST_OF_IONS[i]
        ionInfo[ionName] = {}
        for j in range(numOfOpacityParams):
            param = OPACITY_PROFILE_PARAMETERS[j]
            index = i + (j * numOfIons)
            ionInfo[ionName][param] = ionVals[index]

    return setupInfo, ionInfo


def print_and_save_solutions(saveFilename, xStr):
    setupInfo, ionInfo = read_synapps_solution(xStr)
    print(setupInfo)
    print(ionInfo)

    writer = csv.writer(open(saveFilename, 'w'))

    writer.writerow(["SETUP PARAMETERS"])
    writer.writerow(SETUP_PARAMETERS)
    writer.writerow([float(v) for v in setupInfo.values()])
    writer.writerow([""])
    writer.writerow(["OPACITY PROFILE PARAMETERS"])

    writer.writerow([" "] + OPACITY_PROFILE_PARAMETERS)
    for key, value in ionInfo.items():
        ln = [key]
        for ik, iv in value. items():
            iv = float(iv)
            ln.append(iv)
        writer.writerow(ln)
        print(ln)

if __name__ == "__main__":
    print_and_save_solutions("DES16C2ayx_solved_parameters.csv", X)
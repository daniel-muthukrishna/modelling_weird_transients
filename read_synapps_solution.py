import numpy as np
import csv

X = "[ 5.60e-01 -7.91e-01  1.58e+00  1.28e+01  3.00e+01  8.13e+00  9.42e-01 -9.12e-01 -2.04e-01  1.00e+00  4.00e+00  1.88e-01  1.19e+00  2.20e+00 -2.96e+00  2.58e+00 -1.20e+00 -2.02e+00  1.28e+01  1.28e+01  1.28e+01  1.28e+01  1.28e+01  1.28e+01  1.28e+01  1.28e+01  1.28e+01  1.28e+01  1.28e+01  1.28e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  1.11e+00  9.88e+00  7.25e+00  9.80e-01  3.50e-01  2.16e+00  1.30e+00  4.85e-01  3.70e-01  5.30e-01  2.70e-01  1.10e+00  3.50e+01  4.36e+00  2.50e+00  2.54e+01  6.96e+00  2.30e+01  1.60e+01  1.92e+01  1.00e+01  2.01e+01  8.57e+00  1.21e+01 ]"
LIST_OF_IONS = [601,    800,   1100,   1201,   1401,   1402,   1601,   2001,   2601,   2602,   2701,   2801]
SETUP_PARAMETERS = ["a0", "a1", "a2", "v_phot", "v_out", "t_phot"]
OPACITY_PROFILE_PARAMETERS = ["log_tau", "v_min", "v_max", "aux", "temp"]


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
            index = i + (j * numOfOpacityParams)
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



if __name__ == "__main__":
    print_and_save_solutions("DES16C2ayx_solved_parameters.csv", X)
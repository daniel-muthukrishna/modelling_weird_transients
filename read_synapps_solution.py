import numpy as np
import csv

SETUP_PARAMETERS = ["a0", "a1", "a2", "v_phot", "v_outer", "t_phot"]
OPACITY_PROFILE_PARAMETERS = ["log_tau", "v_min", "v_max", "aux", "temp"]
#LIST_OF_IONS = [601,    800,   1100,   1201,   1401,   1402,   1601,   2001,   2601,   2602,   2701,   2801]
X_FIRST = "[ 5.46e-01 -3.60e-01  1.05e+00  1.29e+01  3.00e+01  9.40e+00  1.48e+00 -1.43e+00 -1.52e-01 -7.72e-01  3.98e+00  1.50e+00  6.20e-01  2.23e+00 -2.14e+00  1.97e+00 -1.20e+00 -2.55e+00  1.29e+01  1.29e+01  1.29e+01  1.29e+01  1.29e+01  1.29e+01  1.29e+01  1.29e+01  1.29e+01  1.29e+01  1.29e+01  1.29e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  6.29e-01  1.00e+01  6.25e+00  4.70e+00  3.50e-01  8.75e-01  1.69e+00  4.34e-01  1.47e+00  5.30e-01  2.39e-01  4.25e-01  3.50e+01  4.16e+00  2.01e+00  2.00e+00  8.24e+00  1.10e+01  1.46e+01  2.80e+01  8.70e+00  2.26e+01  8.58e+00  1.21e+01 ]"
X_1 = "[ 5.46e-01 -3.30e-01  9.70e-01  1.30e+01  3.11e+01  9.54e+00  1.71e+00 -1.49e+00 -1.70e-01 -9.11e-01  4.00e+00  1.51e+00  5.40e-01  2.23e+00 -2.14e+00  1.90e+00 -1.20e+00 -2.55e+00  1.30e+01  1.30e+01  1.30e+01  1.30e+01  1.30e+01  1.30e+01  1.30e+01  1.30e+01  1.30e+01  1.30e+01  1.30e+01  1.30e+01  3.11e+01  3.07e+01  2.75e+01  3.10e+01  3.11e+01  3.11e+01  3.11e+01  3.11e+01  3.11e+01  3.07e+01  3.06e+01  3.04e+01  5.70e-01  1.00e+01  6.97e+00  6.08e+00  3.50e-01  8.40e-01  1.80e+00  1.80e-01  1.00e+01  5.30e-01  2.40e-01  4.10e-01  4.00e+01  4.12e+00  2.01e+00  2.00e+00  8.27e+00  6.55e+00  1.44e+01  2.80e+01  6.58e+00  2.25e+01  8.58e+00  1.21e+01 ]"
LIST_OF_IONS_ALL = [100,   200,   201,   300,   301,   400,   401,   402,   500,   501,   502,   503,   600,   601,   602,   603,   700,   701,   702,   703,   704,   800,   801,   802,   803,   804,   900,   901,   1000,   1100,   1200,   1201,   1300,   1301,   1302,   1400,   1401,   1402,   1403,   1500,   1501,   1502,   1600,   1601,   1602,   1700,   1800,   1801,   1900,   1901,   2000,   2001,   2100,   2101,   2202,   2300,   2301,   2302,   2400,   2401,   2402,   2500,   2501,   2502,   2600,   2601,   2602,   2603,   2700,   2701,   2702,   2703,   2800,   2801,   2802,   2803,   2901,   3002,   3801,   5600,   5601 ]
X_ALL = "[ 1.00e+01 -1.00e+01  1.00e+01  1.40e+01  3.00e+01  1.93e+01  1.00e+00  1.00e+00  3.00e+00  1.00e+00 -1.00e+00  1.00e+00  1.00e+00  1.90e-01 -1.00e+00  9.40e-01  1.00e+00  1.00e+00  1.00e+00  1.71e+00 -1.00e+00  1.00e+00  0.00e+00  0.00e+00  1.00e+00  1.00e+00  1.00e+00 -1.49e+00  1.00e+00  1.00e+00  1.00e+00  1.00e+00  1.00e+00  1.00e+00 -2.48e+00 -2.34e+00  1.00e+00 -9.10e-01  0.00e+00  1.00e+00  1.00e+00  1.00e+00  4.00e+00  1.51e+00  1.00e+00  0.00e+00 -1.00e+00  1.00e+00  1.00e+00 -4.60e-01  0.00e+00  1.00e+00  5.00e-01  4.20e-01  1.00e+00  2.00e+00  1.00e+00  2.23e+00  1.00e+00  1.00e+00  1.00e+00 -1.00e+00  1.00e+00 -2.00e+00  1.00e+00  1.00e+00 -1.00e+00  1.00e+00  0.00e+00  1.00e+00  0.00e+00 -3.00e+00 -1.00e-01  1.00e+00 -1.00e+00 -1.20e+00 -1.00e+00  1.00e+00  1.00e+00 -2.55e+00  1.00e+00  0.00e+00 -1.00e+00  1.00e+00  2.76e+00 -1.00e+00  1.00e+00  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  3.00e+01  3.00e+01  2.42e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  2.94e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  1.00e+00  1.00e-01  6.66e+00  5.00e-01  1.00e+00  1.00e-01  1.00e+00  6.20e-01  5.00e-01  6.20e-01  1.00e+00  1.00e-01  5.00e-01  1.00e-01  1.00e-01  1.00e-01  1.00e+00  1.00e-01  1.00e+00  1.00e-01  1.00e+00  1.00e+01  1.00e+00  1.00e+00  1.00e-01  1.00e-01  5.70e-01  1.00e+00  6.97e+00  6.97e+00  1.00e-01  6.08e+00  7.30e-01  4.50e-01  1.00e-01  1.00e-01  1.00e-01  1.00e-01  1.00e+00  1.00e-01  8.90e-01  1.00e-01  9.70e-01  3.00e-01  5.00e-01  1.00e-01  1.00e+00  1.28e+00  1.00e+00  1.00e-01  1.00e-01  1.80e-01  1.00e-01  1.00e-01  1.00e-01  5.00e-01  1.00e-01  1.00e-01  1.00e-01  1.00e-01  1.00e-01  1.00e-01  1.00e-01  1.00e-01  1.00e-01  9.40e-01  1.00e-01  1.00e-01  1.00e-01  2.40e-01  1.00e-01  1.00e-01  1.00e-01  4.10e-01  1.00e-01  1.00e-01  1.00e-01  1.00e-01  9.60e-01  5.00e-01  1.00e-01  1.00e+01  1.00e+01  1.10e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  4.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  5.00e+00  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  5.00e+00  1.00e+01  5.00e+00  1.00e+01  1.00e+01  1.00e+01  1.00e+01  8.27e+00  6.55e+00  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.44e+01  1.00e+01  1.00e+01  1.00e+01  7.97e+00  1.00e+01  1.00e+01  1.00e+01  2.80e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.10e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.36e+01  2.25e+01  1.00e+01  9.00e+00  8.58e+00  1.00e+01  1.00e+01  1.00e+01  1.21e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01 ]"
ACTIVE_ALL = "[     Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes ]"

LIST_OF_IONS = [100,   200,   201,   300,   301,   400,   401,   402,   500,   501,   502,   503,   600,   601,   602,   603,   700,   701,   702,   703,   704,   800,   801,   802,   803,   804,   900,   901,   1000,   1100,   1200,   1201,   1300,   1301,   1302,   1400,   1401,   1402,   1403,   1500,   1501,   1502,   1600,   1601,   1602,   1700,   1800,   1801,   1900,   1901,   2000,   2001,   2100,   2101,   2202,   2300,   2301,   2302,   2400,   2401,   2402,   2500,   2501,   2502,   2600,   2601,   2602,   2603,   2700,   2701,   2702,   2703,   2800,   2801,   2802,   2803,   2901,   3002,   3801,   5600,   5601 ]
X = "[ 5.40e+00 -6.96e+00  3.99e+00  1.42e+01  2.99e+01  2.16e+01  6.92e-01 -3.46e-01  4.00e+00  4.00e+00  1.49e+00  1.06e+00  3.63e+00  3.05e+00  3.25e+00 -9.37e-01 -2.58e+00  4.00e+00 -1.39e+00 -1.37e+00  4.00e+00  1.11e+00  4.00e+00  2.03e+00  2.00e+00  1.00e+00 -2.50e+00  9.00e-01 -3.00e+00 -3.00e+00  1.42e+01  1.42e+01  1.42e+01  1.42e+01  1.42e+01  1.42e+01  1.42e+01  1.42e+01  1.42e+01  1.42e+01  1.42e+01  1.42e+01  1.42e+01  1.42e+01  1.42e+01  1.42e+01  1.42e+01  1.42e+01  1.42e+01  1.42e+01  1.42e+01  1.42e+01  1.42e+01  1.42e+01  2.99e+01  2.88e+01  2.92e+01  2.99e+01  2.99e+01  2.99e+01  2.99e+01  2.80e+01  2.88e+01  2.99e+01  2.99e+01  2.78e+01  2.45e+01  2.97e+01  2.99e+01  2.99e+01  2.99e+01  2.65e+01  2.99e+01  2.94e+01  2.88e+01  2.80e+01  2.99e+01  2.99e+01  1.00e-01  1.00e-01  8.16e+00  5.00e-01  1.00e+00  2.37e+00  2.00e+00  6.00e-01  1.10e+00  9.75e+00  6.97e+00  1.00e+01  2.08e+00  2.30e+00  1.00e-01  1.00e-01  1.10e+00  4.60e+00  1.10e+00  1.00e-01  1.10e+00  1.00e-01  1.24e+00  4.10e-01  1.00e+01  9.50e+00  1.15e+01  1.00e+01  9.00e+00  5.00e+00  1.35e+01  9.75e+00  3.85e+01  6.00e+00  1.00e+01  7.00e+00  6.25e+00  1.42e+01  1.03e+01  2.72e+01  1.15e+01  6.00e+00  1.15e+01  1.05e+01  1.24e+01  2.50e+01  9.58e+00  1.21e+01 ]"
ACTIVE = "[     Yes,    Yes,    Yes,    Yes,     No,     No,    Yes,     No,     No,    Yes,    Yes,    Yes,     No,    Yes,     No,     No,     No,     No,     No,     No,     No,    Yes,     No,     No,     No,     No,     No,     No,    Yes,    Yes,     No,    Yes,     No,     No,     No,     No,     No,     No,     No,     No,     No,     No,     No,    Yes,     No,     No,     No,     No,     No,     No,    Yes,    Yes,    Yes,    Yes,     No,     No,     No,     No,     No,     No,     No,    Yes,     No,     No,    Yes,    Yes,    Yes,     No,     No,    Yes,     No,     No,     No,    Yes,     No,     No,     No,     No,     No,     No,     No ]"



def read_synapps_solution(xStr, activeStr):
    """ x is a string of a list without spaces instead of commas separating floating point values """

    setupInfo = {}
    ionInfo = {}
    ionsListReduced = []
    numOfSetupParams = len(SETUP_PARAMETERS)
    numOfOpacityParams = len(OPACITY_PROFILE_PARAMETERS)
    activeArray = activeStr.strip('[').strip(']').replace(',','').split()
    for i in range(len(activeArray)):
        if activeArray[i] == "Yes":
            ionsListReduced.append(LIST_OF_IONS[i])
    numOfIons = len(ionsListReduced)

    xArray = xStr.strip('[').strip(']').split()
    for i in range(numOfSetupParams):
        setupInfo[SETUP_PARAMETERS[i]] = xArray[i]

    ionVals = xArray[numOfSetupParams:]
    for i in range(numOfIons):
        ionName = ionsListReduced[i]
        ionInfo[ionName] = {}
        for j in range(numOfOpacityParams):
            param = OPACITY_PROFILE_PARAMETERS[j]
            index = i + (j * numOfIons)
            ionInfo[ionName][param] = ionVals[index]

    return setupInfo, ionInfo


def print_and_save_solutions(saveFilename, xStr, activeStr):
    setupInfo, ionInfo = read_synapps_solution(xStr, activeStr)
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
        for ik, iv in value.items():
            iv = float(iv)
            ln.append(iv)
        writer.writerow(ln)
        print(ln)


def yaml_entries(xStr, activeStr):
    numOfOpacityParams = len(OPACITY_PROFILE_PARAMETERS)
    numOfSetupParams = len(SETUP_PARAMETERS)
    ionsListReduced = []
    activeArray = activeStr.strip('[').strip(']').replace(',','').split()
    for i in range(len(activeArray)):
        if activeArray[i] == "Yes":
            ionsListReduced.append(LIST_OF_IONS[i])
    numOfIons = len(ionsListReduced)

    xArrayAll = X_ALL.strip('[').strip(']').split()
    ionValsAll = xArrayAll[numOfSetupParams:]
    xArray = xStr.strip('[').strip(']').split()
    setupParams = xArray[:numOfSetupParams]
    ionVals = xArray[numOfSetupParams:]

    print("\n\nSETUP_PARAMS")
    print(str(["{0:>6}".format(p) for p in SETUP_PARAMETERS]).replace("'", ""))
    print(str(["{0:>6}".format(float(p)) for p in setupParams]).replace("'", ""))

    print("\n\nION_NAMES")
    print(str(["{0:>6}".format(v) for v in LIST_OF_IONS]).replace("'", ""))
    print("ACTIVE")
    print(str(["{0:>6}".format(v) for v in activeArray]).replace("'", ""))
    for i in range(numOfOpacityParams):
        row = []
        print(OPACITY_PROFILE_PARAMETERS[i])
        k = 0
        for j in range(len(LIST_OF_IONS_ALL)):
            if activeArray[j] == "Yes":
                index = k + (i * numOfIons)
                entry = float(ionVals[index])
                row.append(entry)
                k += 1
            elif activeArray[j] == "No":
                index = j + (i * len(LIST_OF_IONS_ALL))
                entry = float(ionValsAll[index])
                row.append(entry)

        print(str(["{0:>6}".format("{0:0.2f}".format(v)) for v in row]).replace("'", ""))


if __name__ == "__main__":
    print_and_save_solutions("DES16C2ayx_solved_parameters_all.csv", X_ALL, ACTIVE_ALL)
    print_and_save_solutions("DES16C2ayx_solved_parameters_fewer.csv", X, ACTIVE)

    yaml_entries(X, ACTIVE)

import numpy as np
import csv

ION_NAMES = {'H_I': '100', 'He_I': '200', 'He_II': '201', 'Li_I': '300', 'Li_II': '301', 'Be_I': '400', 'Be_II': '401', 'Be_III': '402', 'B_I': '500', 'B_II': '501', 'B_III': '502', 'B_IV': '503', 'C_I': '600', 'C_II': '601', 'C_III': '602', 'N_I': '700', 'N_II': '701', 'N_III': '702', 'N_IV': '703', 'N_V': '704', 'O_I': '800', 'O_II': '801', 'O_III': '802', 'O_IV': '803', 'O_V': '804', 'F_I': '900', 'F_II': '901', 'Ne_I': '1000', 'Na_I': '1100', 'Mg_I': '1200', 'Mg_II': '1201', 'Al_I': '1300', 'Al_II': '1301', 'Al_III': '1302', 'Si_I': '1400', 'Si_II': '1401', 'Si_III': '1402', 'Si_IV': '1403', 'P_I': '1500', 'P_II': '1501', 'P_III': '1502', 'S_I': '1600',  'S_II': '1601', 'S_III': '1602', 'Cl_I': '1700', 'Ar_I': '1800', 'Ar_II': '1801', 'K_I': '1900', 'K_II': '1901', 'Ca_I': '2000', 'Ca_II': '2001', 'Sc_I': '2100', 'Sc_II': '2101', 'Ti_III': '2202', 'V_I': '2300', 'V_II': '2301', 'V_III': '2302', 'Cr_I': '2400', 'Cr_II': '2401', 'Cr_III': '2402', 'Mn_I': '2500', 'Mn_II': '2501', 'Mn_III': '2502', 'Fe_I': '2600', 'Fe_II': '2601', 'Fe_III': '2602', 'Fe_IV': '2603', 'Co_I': '2700', 'Co_II': '2701', 'Co_III': '2702', 'Co_IV': '2703', 'Ni_I': '2800', 'Ni_II': '2801', 'Ni_III': '2802', 'Ni_IV': '2803', 'Cu_II': '2901', 'Zn_I': '3002', 'Sr_I': '3801', 'Ba_I': '5600', 'Ba_II': '5601'}
ION_NUMBERS = dict((v,k) for k,v in ION_NAMES.items())  # Swap keys and values of dictionary


SETUP_PARAMETERS = ["a0", "a1", "a2", "v_phot", "v_outer", "t_phot"]
OPACITY_PROFILE_PARAMETERS = ["log_tau", "v_min", "v_max", "aux", "temp"]
#LIST_OF_IONS = [601,    800,   1100,   1201,   1401,   1402,   1601,   2001,   2601,   2602,   2701,   2801]
X_FIRST = "[ 5.46e-01 -3.60e-01  1.05e+00  1.29e+01  3.00e+01  9.40e+00  1.48e+00 -1.43e+00 -1.52e-01 -7.72e-01  3.98e+00  1.50e+00  6.20e-01  2.23e+00 -2.14e+00  1.97e+00 -1.20e+00 -2.55e+00  1.29e+01  1.29e+01  1.29e+01  1.29e+01  1.29e+01  1.29e+01  1.29e+01  1.29e+01  1.29e+01  1.29e+01  1.29e+01  1.29e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  6.29e-01  1.00e+01  6.25e+00  4.70e+00  3.50e-01  8.75e-01  1.69e+00  4.34e-01  1.47e+00  5.30e-01  2.39e-01  4.25e-01  3.50e+01  4.16e+00  2.01e+00  2.00e+00  8.24e+00  1.10e+01  1.46e+01  2.80e+01  8.70e+00  2.26e+01  8.58e+00  1.21e+01 ]"
X_1 = "[ 5.46e-01 -3.30e-01  9.70e-01  1.30e+01  3.11e+01  9.54e+00  1.71e+00 -1.49e+00 -1.70e-01 -9.11e-01  4.00e+00  1.51e+00  5.40e-01  2.23e+00 -2.14e+00  1.90e+00 -1.20e+00 -2.55e+00  1.30e+01  1.30e+01  1.30e+01  1.30e+01  1.30e+01  1.30e+01  1.30e+01  1.30e+01  1.30e+01  1.30e+01  1.30e+01  1.30e+01  3.11e+01  3.07e+01  2.75e+01  3.10e+01  3.11e+01  3.11e+01  3.11e+01  3.11e+01  3.11e+01  3.07e+01  3.06e+01  3.04e+01  5.70e-01  1.00e+01  6.97e+00  6.08e+00  3.50e-01  8.40e-01  1.80e+00  1.80e-01  1.00e+01  5.30e-01  2.40e-01  4.10e-01  4.00e+01  4.12e+00  2.01e+00  2.00e+00  8.27e+00  6.55e+00  1.44e+01  2.80e+01  6.58e+00  2.25e+01  8.58e+00  1.21e+01 ]"
LIST_OF_IONS_ALL = [100,   200,   201,   300,   301,   400,   401,   402,   500,   501,   502,   503,   600,   601,   602,   603,   700,   701,   702,   703,   704,   800,   801,   802,   803,   804,   900,   901,   1000,   1100,   1200,   1201,   1300,   1301,   1302,   1400,   1401,   1402,   1403,   1500,   1501,   1502,   1600,   1601,   1602,   1700,   1800,   1801,   1900,   1901,   2000,   2001,   2100,   2101,   2202,   2300,   2301,   2302,   2400,   2401,   2402,   2500,   2501,   2502,   2600,   2601,   2602,   2603,   2700,   2701,   2702,   2703,   2800,   2801,   2802,   2803,   2901,   3002,   3801,   5600,   5601 ]
X_ALL = "[ 1.00e+01 -1.00e+01  1.00e+01  1.40e+01  3.00e+01  1.93e+01  1.00e+00  1.00e+00  3.00e+00  1.00e+00 -1.00e+00  1.00e+00  1.00e+00  1.90e-01 -1.00e+00  9.40e-01  1.00e+00  1.00e+00  1.00e+00  1.71e+00 -1.00e+00  1.00e+00  0.00e+00  0.00e+00  1.00e+00  1.00e+00  1.00e+00 -1.49e+00  1.00e+00  1.00e+00  1.00e+00  1.00e+00  1.00e+00  1.00e+00 -2.61e+00 -2.45e+00  1.00e+00 -9.10e-01  0.00e+00  1.00e+00  1.00e+00  1.00e+00  4.00e+00  1.51e+00  1.00e+00  0.00e+00 -1.00e+00  1.00e+00  1.00e+00 -4.60e-01  0.00e+00  1.00e+00  5.00e-01  4.20e-01  1.00e+00  2.00e+00  1.00e+00  2.23e+00  1.00e+00  1.00e+00  1.00e+00 -1.00e+00  1.00e+00 -2.00e+00  1.00e+00  1.00e+00 -1.00e+00  1.00e+00  0.00e+00  1.00e+00  0.00e+00 -3.00e+00 -1.00e-01  1.00e+00 -1.00e+00 -1.20e+00 -1.00e+00  1.00e+00  1.00e+00 -2.55e+00  1.00e+00  0.00e+00 -1.00e+00  1.00e+00  2.76e+00 -1.00e+00  1.00e+00  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  1.40e+01  3.00e+01  3.00e+01  2.42e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  2.94e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  3.00e+01  1.00e+00  1.00e-01  6.66e+00  5.00e-01  1.00e+00  1.00e-01  1.00e+00  6.20e-01  5.00e-01  6.20e-01  1.00e+00  1.00e-01  5.00e-01  1.00e-01  1.00e-01  1.00e-01  1.00e+00  1.00e-01  1.00e+00  1.00e-01  1.00e+00  1.00e+01  1.00e+00  1.00e+00  1.00e-01  1.00e-01  5.70e-01  1.00e+00  6.97e+00  6.97e+00  1.00e-01  6.08e+00  6.80e-01  4.50e-01  1.00e-01  1.00e-01  1.00e-01  1.00e-01  1.00e+00  1.00e-01  8.20e-01  1.00e-01  9.00e-01  3.00e-01  5.00e-01  1.00e-01  1.00e+00  1.28e+00  1.00e+00  1.00e-01  1.00e-01  1.80e-01  1.00e-01  1.00e-01  1.00e-01  5.00e-01  1.00e-01  1.00e-01  1.00e-01  1.00e-01  1.00e-01  1.00e-01  1.00e-01  1.00e-01  1.00e-01  9.40e-01  1.00e-01  1.00e-01  1.00e-01  2.40e-01  1.00e-01  1.00e-01  1.00e-01  4.10e-01  1.00e-01  1.00e-01  1.00e-01  1.00e-01  9.60e-01  5.00e-01  1.00e-01  1.00e+01  1.00e+01  1.10e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  4.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  5.00e+00  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  5.00e+00  1.00e+01  5.00e+00  1.00e+01  1.00e+01  1.00e+01  1.00e+01  8.27e+00  6.55e+00  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.44e+01  1.00e+01  1.00e+01  1.00e+01  7.96e+00  1.00e+01  1.00e+01  1.00e+01  2.80e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.10e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.36e+01  2.25e+01  1.00e+01  9.00e+00  8.58e+00  1.00e+01  1.00e+01  1.00e+01  1.21e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01  1.00e+01 ]"
ACTIVE_ALL = "[     Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes,    Yes ]"
X_BDJ_VLT_20160924 = "[ 9.96e+00  1.00e+01  6.42e+00  1.50e+01  4.32e+01  1.93e+01  3.37e+00 -4.87e-01  3.64e+00  2.54e+00  4.10e+00  4.04e-01  7.82e-01  3.76e+00  5.83e+00  3.11e+00  1.14e+00  4.22e+00 -5.19e+00  4.66e-01  6.91e-02  3.41e+00  9.37e-01 -1.40e+00  1.75e+00  4.27e+00  5.02e-01  5.12e-01 -9.90e-01  1.05e+00  2.72e+00  7.26e-01  8.43e-01 -4.69e-01 -3.54e+00 -7.72e-02  1.58e+00 -8.50e-01 -5.08e+00 -2.00e-02  1.69e+00 -3.00e+00  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  1.50e+01  4.32e+01  2.88e+01  2.69e+01  4.32e+01  2.42e+01  3.37e+01  3.22e+01  2.87e+01  3.37e+01  2.80e+01  3.01e+01  2.01e+01  4.32e+01  2.81e+01  4.32e+01  2.81e+01  3.00e+01  2.19e+01  3.00e+01  4.32e+01  3.96e+01  4.32e+01  3.00e+01  3.00e+01  2.93e+01  3.43e+01  3.11e+01  3.29e+01  3.08e+01  2.94e+01  3.68e+01  2.80e+01  3.52e+01  2.71e+01  3.00e+01  3.01e+01  7.20e-01  1.00e-01  1.00e+01  3.95e-01  1.91e+00  1.00e+00  1.64e+00  1.40e-01  1.12e+00  1.00e-01  1.00e-01  7.15e-01  9.75e+00  1.00e+01  1.00e+01  1.00e+01  1.00e-01  2.98e+00  1.00e-01  1.00e-01  1.00e+01  6.98e+00  6.90e-01  2.00e-01  1.30e-01  6.95e+00  4.50e-01  5.10e-01  1.47e+00  1.60e-01  3.12e+00  5.30e-01  2.61e+00  5.03e+00  7.30e-01  4.30e-01  1.01e+01  9.50e+00  1.31e+01  5.00e+00  9.21e+00  6.84e+00  6.22e+00  5.63e+00  5.00e+00  9.75e+00  9.94e+00  5.00e+00  5.90e+00  5.00e+01  5.00e+00  7.17e+00  1.00e+01  5.00e+00  1.00e+01  1.09e+01  1.77e+01  5.00e+01  1.01e+01  7.96e+00  8.60e+00  1.97e+01  5.50e+00  1.18e+01  1.00e+01  5.00e+00  9.28e+00  2.30e+01  8.51e+00  5.00e+00  1.00e+01  1.25e+01 ]"
ACTIVE_BDJ_VLT_20160924 = "[     Yes,    Yes,    Yes,    Yes,     No,    Yes,    Yes,    Yes,     No,    Yes,    Yes,    Yes,    Yes,    Yes,     No,     No,     No,     No,     No,     No,     No,    Yes,     No,     No,     No,     No,    Yes,     No,    Yes,    Yes,    Yes,    Yes,     No,     No,     No,    Yes,    Yes,    Yes,     No,     No,     No,     No,     No,    Yes,     No,     No,    Yes,    Yes,     No,     No,    Yes,    Yes,    Yes,    Yes,     No,     No,     No,     No,     No,     No,     No,    Yes,     No,     No,    Yes,    Yes,    Yes,     No,    Yes,    Yes,     No,     No,    Yes,    Yes,     No,     No,     No,     No,     No,     No,     No ]"

LIST_OF_IONS = [100,   200,   201,   300,   301,   400,   401,   402,   500,   501,   502,   503,   600,   601,   602,   603,   700,   701,   702,   703,   704,   800,   801,   802,   803,   804,   900,   901,   1000,   1100,   1200,   1201,   1300,   1301,   1302,   1400,   1401,   1402,   1403,   1500,   1501,   1502,   1600,   1601,   1602,   1700,   1800,   1801,   1900,   1901,   2000,   2001,   2100,   2101,   2202,   2300,   2301,   2302,   2400,   2401,   2402,   2500,   2501,   2502,   2600,   2601,   2602,   2603,   2700,   2701,   2702,   2703,   2800,   2801,   2802,   2803,   2901,   3002,   3801,   5600,   5601 ]
X_AYX = "[ 5.41e+00 -4.91e+00  1.00e+01  1.43e+01  3.96e+01  1.88e+01  7.20e-01 -3.40e-01  4.00e+00  6.00e+00  1.25e+00  2.96e+00  4.07e+00  3.06e+00  5.87e+00 -3.75e+00 -3.56e+00  3.48e+00  3.00e+00  4.42e+00  3.35e+00  6.30e-01  5.37e+00  1.11e+00  3.99e+00  1.97e+00 -3.50e+00  1.00e+00  1.60e+00 -1.00e-01  0.00e+00 -2.00e+00  1.43e+01  1.43e+01  1.43e+01  1.43e+01  1.43e+01  1.43e+01  1.43e+01  1.43e+01  1.43e+01  1.43e+01  1.43e+01  1.43e+01  1.43e+01  1.43e+01  1.43e+01  1.43e+01  1.43e+01  1.43e+01  1.43e+01  1.43e+01  1.43e+01  1.43e+01  1.43e+01  1.43e+01  1.43e+01  1.43e+01  3.96e+01  2.88e+01  3.09e+01  3.96e+01  3.37e+01  2.61e+01  3.50e+01  2.80e+01  2.48e+01  3.96e+01  3.96e+01  3.09e+01  1.68e+01  3.91e+01  3.57e+01  3.85e+01  3.13e+01  3.12e+01  3.11e+01  3.29e+01  3.08e+01  2.94e+01  2.84e+01  2.80e+01  3.34e+01  3.01e+01  1.00e-01  1.00e-01  1.00e+01  4.00e-01  1.00e+00  1.33e+00  2.00e+00  1.00e-01  9.20e-01  9.75e+00  5.97e+00  1.00e+01  7.40e-01  2.40e-01  8.30e-01  8.43e+00  5.40e-01  1.00e-01  1.10e+00  1.91e+00  4.10e-01  1.00e-01  1.33e+00  3.50e-01  4.14e+00  4.10e-01  1.00e+01  9.50e+00  1.15e+01  2.06e+01  7.40e+00  5.29e+00  2.52e+01  9.75e+00  5.78e+00  6.00e+00  1.10e+01  1.07e+01  5.00e+00  1.14e+01  5.00e+00  2.04e+01  9.55e+00  2.72e+01  6.73e+00  1.33e+01  1.00e+01  8.50e+00  1.99e+01  2.50e+01  5.00e+00  1.26e+01 ]"
ACTIVE_AYX = "[     Yes,    Yes,    Yes,    Yes,     No,     No,    Yes,     No,     No,    Yes,    Yes,    Yes,     No,    Yes,     No,     No,     No,     No,     No,     No,     No,    Yes,     No,     No,     No,     No,     No,     No,    Yes,    Yes,     No,    Yes,     No,     No,     No,     No,    Yes,    Yes,     No,     No,     No,     No,     No,    Yes,     No,     No,     No,     No,     No,     No,    Yes,    Yes,    Yes,    Yes,     No,     No,     No,     No,     No,     No,     No,    Yes,     No,     No,    Yes,    Yes,    Yes,     No,     No,    Yes,     No,     No,     No,    Yes,     No,     No,     No,     No,     No,     No,     No ]"
X_BDJ = "[ 7.88e+00  9.81e+00  6.32e+00  1.48e+01  4.78e+01  1.72e+01  7.00e+00 -4.47e-01  3.21e+00  4.04e-01  1.80e+00  1.37e-01  6.33e-01  2.42e+00  5.06e+00  3.27e+00  1.13e+00  9.39e-01 -5.44e+00  3.51e-01  1.30e-01  3.24e+00  8.36e-01 -2.58e+00  3.45e+00  4.34e+00  4.74e-01  2.73e-01 -1.03e+00  1.03e+00  4.67e-01  4.48e+00  8.60e-01 -7.51e-01 -3.38e+00 -1.60e+00  1.56e+00 -8.50e-01 -5.08e+00 -2.00e-02  3.77e+00 -3.00e+00  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  4.32e+01  2.88e+01  2.25e+01  4.32e+01  2.22e+01  3.37e+01  3.21e+01  2.17e+01  3.36e+01  2.80e+01  3.01e+01  1.99e+01  4.32e+01  2.79e+01  4.78e+01  2.45e+01  3.00e+01  2.20e+01  3.00e+01  4.32e+01  3.64e+01  3.72e+01  3.00e+01  3.00e+01  2.93e+01  3.83e+01  3.34e+01  3.29e+01  3.08e+01  2.94e+01  3.56e+01  2.80e+01  3.52e+01  2.54e+01  3.00e+01  3.01e+01  7.20e-01  1.00e-01  1.00e+01  4.00e-01  1.30e+00  1.10e+00  1.64e+00  6.84e+00  1.12e+00  1.00e-01  2.49e+00  6.75e+00  9.75e+00  7.99e+00  1.00e+01  8.23e+00  5.70e-01  2.79e+00  6.00e-01  1.00e-01  9.32e+00  5.37e+00  6.90e-01  2.00e-01  6.16e-01  1.04e+00  5.29e+00  1.00e-01  1.47e+00  1.00e-01  3.43e+00  2.80e-01  2.61e+00  3.46e+00  7.95e-01  1.80e-01  5.00e+01  9.44e+00  1.32e+01  5.00e+00  3.00e+00  6.37e+00  5.81e+00  3.00e+00  5.00e+00  1.02e+01  3.57e+01  5.00e+00  5.65e+00  5.00e+01  8.47e+00  4.53e+00  9.50e+00  3.56e+00  3.46e+01  1.12e+01  1.80e+01  5.00e+01  9.60e+00  8.21e+00  7.60e+00  1.63e+01  9.15e+00  1.18e+01  1.00e+01  5.00e+00  9.36e+00  2.30e+01  8.76e+00  3.56e+00  5.29e+00  1.25e+01 ]"
ACTIVE_BDJ = "[     Yes,    Yes,    Yes,    Yes,     No,    Yes,    Yes,    Yes,     No,    Yes,    Yes,    Yes,    Yes,    Yes,     No,     No,     No,     No,     No,     No,     No,    Yes,     No,     No,     No,     No,    Yes,     No,    Yes,    Yes,    Yes,    Yes,     No,     No,     No,    Yes,    Yes,    Yes,     No,     No,     No,     No,     No,    Yes,     No,     No,    Yes,    Yes,     No,     No,    Yes,    Yes,    Yes,    Yes,     No,     No,     No,     No,     No,     No,     No,    Yes,     No,     No,    Yes,    Yes,    Yes,     No,    Yes,    Yes,     No,     No,    Yes,    Yes,     No,     No,     No,     No,     No,     No,     No ]"

X = X_BDJ#"[ 1.00e+01  9.34e+00  5.47e+00  1.48e+01  4.23e+01  1.93e+01  4.25e+00 -4.57e-01  3.72e+00  3.97e+00  1.97e+00  2.51e-01  9.56e-01  4.19e+00  5.81e+00  3.15e+00  1.09e+00  4.75e+00 -5.18e+00  4.40e-01 -6.34e-03  3.38e+00  9.32e-01 -1.21e+00  1.74e+00  4.23e+00  4.76e-01  5.13e-01 -9.84e-01  7.98e-01  2.70e+00  6.94e-01  8.85e-01 -4.65e-01 -3.55e+00 -9.39e-02  1.58e+00 -8.50e-01 -5.08e+00 -2.00e-02  1.75e+00 -3.00e+00  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  1.48e+01  4.23e+01  2.88e+01  2.69e+01  4.23e+01  3.00e+01  3.37e+01  3.22e+01  2.87e+01  3.39e+01  2.80e+01  3.01e+01  1.90e+01  4.23e+01  2.76e+01  4.23e+01  2.81e+01  3.00e+01  2.18e+01  3.00e+01  4.23e+01  3.91e+01  4.23e+01  3.00e+01  3.00e+01  2.93e+01  3.61e+01  3.11e+01  3.29e+01  3.08e+01  2.94e+01  3.49e+01  2.80e+01  3.52e+01  2.74e+01  3.00e+01  3.01e+01  6.62e-01  1.00e-01  9.81e+00  5.80e-01  1.00e-01  1.00e+00  1.64e+00  3.87e-01  1.12e+00  1.00e-01  1.00e-01  8.38e-01  9.75e+00  1.00e+01  1.00e+01  8.50e+00  1.00e-01  2.98e+00  1.00e-01  1.00e-01  9.96e+00  7.04e+00  6.90e-01  4.53e-01  1.30e-01  7.56e+00  4.50e-01  5.10e-01  1.41e+00  1.00e-01  3.12e+00  5.30e-01  2.61e+00  5.40e+00  4.15e-01  4.30e-01  1.00e+01  9.50e+00  1.30e+01  5.00e+00  9.97e+00  7.41e+00  6.73e+00  6.38e+00  5.00e+00  9.75e+00  1.00e+01  9.29e+00  5.90e+00  5.00e+01  5.00e+00  8.80e+00  1.00e+01  5.00e+00  1.00e+01  1.09e+01  1.84e+01  4.92e+01  1.01e+01  7.96e+00  8.60e+00  1.63e+01  5.50e+00  1.18e+01  1.00e+01  5.00e+00  8.97e+00  2.30e+01  8.51e+00  5.00e+00  1.00e+01  1.25e+01 ]"
ACTIVE = ACTIVE_BDJ#"[     Yes,    Yes,    Yes,    Yes,     No,    Yes,    Yes,    Yes,     No,    Yes,    Yes,    Yes,    Yes,    Yes,     No,     No,     No,     No,     No,     No,     No,    Yes,     No,     No,     No,     No,    Yes,     No,    Yes,    Yes,    Yes,    Yes,     No,     No,     No,    Yes,    Yes,    Yes,     No,     No,     No,     No,     No,    Yes,     No,     No,    Yes,    Yes,     No,     No,    Yes,    Yes,    Yes,    Yes,     No,     No,     No,     No,     No,     No,     No,    Yes,     No,     No,    Yes,    Yes,    Yes,     No,    Yes,    Yes,     No,     No,    Yes,    Yes,     No,     No,     No,     No,     No,     No,     No ]"


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
        ionName = ION_NUMBERS[str(ionsListReduced[i])]
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

    opacityParamsYamlStrings = []
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

        opacityParamsYamlString = str(["{0:>6}".format("{0:0.2f}".format(v)) for v in row]).replace("'", "")
        opacityParamsYamlStrings.append(opacityParamsYamlString)
        print(opacityParamsYamlString)

    return setupParams, opacityParamsYamlStrings


if __name__ == "__main__":
    # print_and_save_solutions("DES16X3bdj_solved_parameters_all.csv", X_ALL, ACTIVE_ALL)
    print_and_save_solutions("DES16X3bdj_solved_parameters_fewer2.csv", X, ACTIVE)

    yaml_entries(X, ACTIVE)

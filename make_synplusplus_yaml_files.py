from read_synapps_solution import yaml_entries
from rerun_synapps_if_stopped import update_yaml_file
from plot_spectrum import plot_spectrum, read_file
import subprocess
import os
import matplotlib.pyplot as plt
import numpy as np
from helpers import calc_opacity

ION_NAMES = {'All': None, 'All_flat': None, 'H_I': '0100', 'He_I': '0200', 'He_II': '0201', 'Li_I': '0300', 'Li_II': '0301', 'Be_I': '0400', 'Be_II': '0401', 'Be_III': '0402', 'B_I': '0500', 'B_II': '0501', 'B_III': '0502', 'B_IV': '0503', 'C_I': '0600', 'C_II': '0601', 'C_III': '0602', 'N_I': '0700', 'N_II': '0701', 'N_III': '0702', 'N_IV': '0703', 'N_V': '0704', 'O_I': '0800', 'O_II': '0801', 'O_III': '0802', 'O_IV': '0803', 'O_V': '0804', 'F_I': '0900', 'F_II': '0901', 'Ne_I': '1000', 'Na_I': '1100', 'Mg_I': '1200', 'Mg_II': '1201', 'Al_I': '1300', 'Al_II': '1301', 'Al_III': '1302', 'Si_I': '1400', 'Si_II': '1401', 'Si_III': '1402', 'Si_IV': '1403', 'P_I': '1500', 'P_II': '1501', 'P_III': '1502', 'S_I': '1600',  'S_II': '1601', 'S_III': '1602', 'Cl_I': '1700', 'Ar_I': '1800', 'Ar_II': '1801', 'K_I': '1900', 'K_II': '1901', 'Ca_I': '2000', 'Ca_II': '2001', 'Sc_I': '2100', 'Sc_II': '2101', 'Ti_III': '2202', 'V_I': '2300', 'V_II': '2301', 'V_III': '2302', 'Cr_I': '2400', 'Cr_II': '2401', 'Cr_III': '2402', 'Mn_I': '2500', 'Mn_II': '2501', 'Mn_III': '2502', 'Fe_I': '2600', 'Fe_II': '2601', 'Fe_III': '2602', 'Fe_IV': '2603', 'Co_I': '2700', 'Co_II': '2701', 'Co_III': '2702', 'Co_IV': '2703', 'Ni_I': '2800', 'Ni_II': '2801', 'Ni_III': '2802', 'Ni_IV': '2803', 'Cu_II': '2901', 'Zn_I': '3002', 'Sr_I': '3801', 'Ba_I': '5600', 'Ba_II': '5601'}
ION_NUMBERS = dict((v,k) for k,v in ION_NAMES.items())  # Swap keys and values of dictionary


def run_bash_command(bashCommandStr):
    # process = subprocess.Popen(bashCommandStr.split())
    # output, error = process.communicate()
    output = os.system(bashCommandStr)

    return output


def update_synapps_yaml_file(synappsYamlFilename, noHupFilename, saveSolutionFilename=''):
    update_yaml_file(synappsYamlFilename, noHupFilename, saveSolutionFilename)


def make_synplusplus_ion_yaml_file(synappsYamlFile, outputFilename, flatten='Yes', ionName='All', opacityMinImportant=-10):
    with open(synappsYamlFile, 'r') as file:
        data = file.readlines()
        minWave = data[22].split(', ')[1].split(']')[0]
        maxWave = data[23].split(', ')[-1].split(']')[0]
        binWidth = data[2].split(': ')[1].split('\n')[0]
        vSize = data[3].split(': ')[1].split('\n')[0]
        vOuterMax = data[4].split(': ')[1].split('\n')[0]
        lineDir = data[6].split(': ')[1].split('\n')[0]
        refFile = data[7].split(': ')[1].split('\n')[0]
        vRef = data[9].split(': ')[1].split('\n')[0]
        logTauMin = data[10].split(': ')[1].split('\n')[0]
        muSize = data[12].split(': ')[1].split('\n')[0]
        pSize = data[14].split(': ')[1].split('\n')[0]
        a0 = data[28].split(':')[3].split(',')[0]
        a1 = data[29].split(':')[3].split(',')[0]
        a2 = data[30].split(':')[3].split(',')[0]
        vPhot = data[31].split(':')[3].split(',')[0]
        vOuter = data[32].split(':')[3].split(',')[0]
        tPhot = data[33].split(':')[3].split(',')[0]
        ions = data[36].split(': ')[1].split('\n')[0]
        activeOriginal = data[37].split(': ')[1].split('\n')[0]
        logTau = data[42].split(': ')[1].split('\n')[0]
        vMin = data[48].split(': ')[1].split('\n')[0]
        vMax = data[54].split(': ')[1].split('\n')[0]
        aux = data[60].split(': ')[1].split('\n')[0]
        temp = data[66].split(': ')[1].split('\n')[0]

        activeOriginalList = activeOriginal.split(',')
        ionNumbersList = ions.replace('[', '').replace(']', '').replace(' ', '').split(',')

        if 'All' in ionName:
            active = activeOriginal
            opacity_at_vmin = 99
        elif ionName == 'important':
            activeList = ['No'] * len(activeOriginalList)
            for i in range(len(activeOriginalList)):
                if 'Yes' in activeOriginalList[i]:
                    logTauIonVal = float(logTau.strip('[').strip(']').split(',')[i])
                    vMinIonVal = float(vMin.strip('[').strip(']').split(',')[i])
                    vMaxIonVal = float(vMax.strip('[').strip(']').split(',')[i])
                    auxIonVal = float(aux.strip('[').strip(']').split(',')[i])
                    opacity_at_vmin = calc_opacity(vMinIonVal, logTauIonVal, vRef, auxIonVal)
                    if opacity_at_vmin > opacityMinImportant: #################################
                        activeList[i] = 'Yes'
                        print("Important Ion: %s" % ION_NUMBERS[ionNumbersList[i]], opacity_at_vmin)
            active = "[    {0} ]".format(",     ".join(activeList))
            opacity_at_vmin = 99
        elif type(ionName) is list:
            activeList = ['No'] * len(ionNumbersList)
            for ion in ionName:
                ionNumber = ION_NAMES[ion]
                index = ionNumbersList.index(ionNumber)
                if 'Yes' in activeOriginalList[index]:
                    activeList[index] = 'Yes'
                    print("Fitting ion {0}...".format(ion))
            active = "[    {0} ]".format(",     ".join(activeList))
            opacity_at_vmin = 99
        else:
            ionNumber = ION_NAMES[ionName]
            if ionNumber not in ionNumbersList:
                return False, None
            index = ionNumbersList.index(ionNumber)
            logTauIonVal = float(logTau.strip('[').strip(']').split(',')[index])
            vMinIonVal = float(vMin.strip('[').strip(']').split(',')[index])
            vMaxIonVal = float(vMax.strip('[').strip(']').split(',')[index])
            auxIonVal = float(aux.strip('[').strip(']').split(',')[index])
            if 'Yes' in activeOriginalList[index]:
                activeList = ['No'] * len(ionNumbersList)
                activeList[index] = 'Yes'
                active = "[    {0} ]".format(",     ".join(activeList))
                print("Fitting ion {0}...".format(ionName))
            else:
                # print("{0} not fit".format(ionName))
                return False, None

            opacity_at_vmin = calc_opacity(vMinIonVal, logTauIonVal, vRef, auxIonVal)

    with open(outputFilename, 'w') as file:
        file.write("output :\n")
        file.write("    min_wl       : {0}\n".format(minWave))
        file.write("    max_wl       : {0}\n".format(maxWave))
        file.write("    wl_step      : 5.0\n")
        file.write("grid :\n")
        file.write("    bin_width    : {0}\n".format(binWidth))
        file.write("    v_size       : {0}\n".format(vSize))
        file.write("    v_outer_max  : {0}\n".format(vOuterMax))
        file.write("opacity :\n")
        file.write("    line_dir     : {0}\n".format(lineDir))
        file.write("    ref_file     : {0}\n".format(refFile))
        file.write("    form         : exp\n")
        file.write("    v_ref        : {0}\n".format(vRef))
        file.write("    log_tau_min  : {0}\n".format(logTauMin))
        file.write("source :\n")
        file.write("    mu_size      : {0}\n".format(muSize))
        file.write("spectrum :\n")
        file.write("    p_size       : {0}\n".format(pSize))
        file.write("    flatten      : {0}\n".format(flatten))
        file.write("setups :\n")
        file.write("    -   a0       : {0}\n".format(a0))
        file.write("        a1       : {0}\n".format(a1))
        file.write("        a2       : {0}\n".format(a2))
        file.write("        v_phot   : {0}\n".format(vPhot))
        file.write("        v_outer  : {0}\n".format(vOuter))
        file.write("        t_phot   : {0}\n".format(tPhot))
        file.write("        ions     : {0}\n".format(ions))
        file.write("        active   : {0}\n".format(active))
        file.write("        log_tau  : {0}\n".format(logTau))
        file.write("        v_min    : {0}\n".format(vMin))
        file.write("        v_max    : {0}\n".format(vMax))
        file.write("        aux      : {0}\n".format(aux))
        file.write("        temp     : {0}\n".format(temp))

    return True, opacity_at_vmin


def is_zero_spectrum(filename):
    wave, flux, fluxErr = read_file(filename)
    if np.any(flux-1):
        return False
    else:
        return True


def make_plots(directory, noHupFilename, yamlFilename, dataFilename, minOpacityPlot=0, minImportantOpacity=0, plotIonsList=[]):
    update_synapps_yaml_file(synappsYamlFilename=directory + yamlFilename, noHupFilename=directory + noHupFilename, saveSolutionFilename=directory + 'ion_parameters.csv')

    if not os.path.exists(os.path.join(directory, 'ion_fits')):
        os.makedirs(os.path.join(directory, 'ion_fits'))
    synappsYamlFile1 = directory + yamlFilename
    plt.figure()
    plot_spectrum(directory + dataFilename)

    storePlotInfo = []

    offset = 0
    for ionName1 in ION_NAMES.keys():
        outputFilename1 = "{0}ion_fits/{1}.yaml".format(directory, ionName1)
        flatten = 'No' if ionName1 == 'All' else 'Yes'
        success, opacity = make_synplusplus_ion_yaml_file(synappsYamlFile=synappsYamlFile1, outputFilename=outputFilename1, flatten=flatten, ionName=ionName1)
        if success:
            run_bash_command("syn++ {0} > {1}".format(outputFilename1, outputFilename1.replace('.yaml', '.fit')))
            filename = "{0}ion_fits/{1}.fit".format(directory, ionName1)
            if not is_zero_spectrum(filename) and ionName1 != 'All_flat':
                if 'All' in filename:
                    plot_spectrum(filename=filename, label=ionName1, legendNCol=1, title=directory, vOffset=offset, yLabel='Relative Flux + Offset', bbox_to_anchor=(1, 1))
                elif opacity > minOpacityPlot: ############################################
                    storePlotInfo.append([opacity, filename, ionName1])
                else:
                    print("SMALL OPACITY: {0} for ION: {1}".format(opacity, ionName1))
            else:
                print("ZERO FLUX FOR ION: {0}".format(ionName1))

    # Plot ions in order or opacity
    storePlotInfo = sorted(storePlotInfo, key=lambda x: x[0])[::-1]
    for plotInfo in storePlotInfo:
        opacity, filename, ionName1 = plotInfo
        plot_spectrum(filename=filename, label=ionName1, legendNCol=1, title=directory, vOffset=offset, yLabel='Relative Flux + Offset', bbox_to_anchor=(1,1))
        offset -= 1

    if minImportantOpacity:
        plt.figure()
        outputFilename1 = "{0}ion_fits/important.yaml".format(directory)
        success, opacity = make_synplusplus_ion_yaml_file(synappsYamlFile=synappsYamlFile1, outputFilename=outputFilename1, flatten='Yes', ionName='important', opacityMinImportant=minImportantOpacity)
        run_bash_command("syn++ {0} > {1}".format(outputFilename1, outputFilename1.replace('.yaml', '.fit')))
        # plot_spectrum('DES16X3bdj_VLT_20160924_restFrame_smooth7.txt', label='Data')
        plot_spectrum(filename="{0}ion_fits/All_flat.fit".format(directory), label='All ions fit', yLabel='Relative Flux')
        plot_spectrum(filename="{0}ion_fits/important.fit".format(directory), label='Top ions fit', title='Important ions only fit', yLabel='Relative Flux')

    if plotIonsList:
        plt.figure()
        offset = 0
        plot_spectrum(filename="{0}ion_fits/All.fit".format(directory), label='All ions fit', yLabel='Relative Flux')
        ionNameList = plotIonsList  # ['B_III', 'B_IV']
        for ionName1 in ionNameList:
            outputFilename1 = "{0}ion_fits/{1}.yaml".format(directory, ionName1)
            success, opacity = make_synplusplus_ion_yaml_file(synappsYamlFile=synappsYamlFile1, outputFilename=outputFilename1, flatten='Yes', ionName=ionName1)
            run_bash_command("syn++ {0} > {1}".format(outputFilename1, outputFilename1.replace('.yaml', '.fit')))
            filename = "{0}ion_fits/{1}.fit".format(directory, ionName1)
            plot_spectrum(filename=filename, label=ionName1, legendNCol=1, title='Selected Ions', vOffset=offset, yLabel='Relative Flux + Offset', bbox_to_anchor=(1, 1))
            offset -= 1


if __name__ == '__main__':
    directory1 = "Saved_Fits/DES16X3bdj_VLT_20160924/"
    make_plots(directory=directory1, noHupFilename='nohup_DES16X3bdj_2.out', yamlFilename='DES16X3bdj_VLT_20160924.yaml',
               dataFilename='DES16X3bdj_VLT_20160924_restFrame_smooth7.txt', minOpacityPlot=-10, minImportantOpacity=-10,
               plotIonsList=[])
    plt.figure()
    plot_spectrum(directory1 + 'DES16X3bdj_VLT_20160924_restFrame_smooth7.txt', label='Data')
    plot_spectrum(filename="{0}ion_fits/All.fit".format(directory1), label='Best fit', yLabel='Relative Flux')


    # directory2 = "Saved_Fits/sn2002ap/"
    # make_plots(directory=directory2, noHupFilename='nohup_sn2002ap.out', yamlFilename='sn2002ap.yaml',
    #            dataFilename='sn2002ap-20020206.flm_restFrame_smooth1.txt', minOpacityPlot=-1, minImportantOpacity=-1,
    #            plotIonsList=[])
    #
    # directory2 = "Saved_Fits/sn2006jo/"
    # make_plots(directory=directory2, noHupFilename='nohup_sn2006jo.out', yamlFilename='sn2006jo.yaml',
    #            dataFilename='sn2006jo_restFrame_smooth3.txt', minOpacityPlot=-1, minImportantOpacity=-1,
    #            plotIonsList=[])

    plt.show()

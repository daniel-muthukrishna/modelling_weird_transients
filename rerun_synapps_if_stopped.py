import sys
import subprocess
from read_synapps_solution import yaml_entries, print_and_save_solutions


def tail(f, n):
    output, error = run_bash_command("tail -n " + str(n) + " " + f)
    return str(output)


def run_bash_command(bashCommandStr):
    process = subprocess.Popen(bashCommandStr.split(), stdout=subprocess.PIPE)
    output, error = process.communicate(input='\n')

    return output, error


def check_if_abrupt_ended(noHupFile):
    output = tail(f=noHupFile, n=7)

    if "WARNING" in output:
        print("Ended without conversion!")
        endState = 'Error'
    elif "Thank you" in output:
        print("Finished Program!")
        endState = 'Finished'
        with open(noHupFile, 'r') as f:
            for line in f:
                if 'Final Min' in line:
                    output = line
                    break
    else:
        print("Program still running")
        endState = 'Running'

    return output, endState


def read_last_fit(noHupFile, active, saveSolutionFilename='', vref=10):
    output, endState = check_if_abrupt_ended(noHupFile)

    print("Reading last fit...")
    lastFit = output.split('\\n\\n')[-1]
    if ("New Min" in lastFit) or ('Final Min' in lastFit):
        lastFit = lastFit.split('x=')[1].split(' step')[0]
        setupYamlEntries, opacityYamlLines = yaml_entries(lastFit, active)
        if saveSolutionFilename != '':
            print_and_save_solutions(saveSolutionFilename, lastFit, active, vref)
    else:
        # This should never happen. It means that the last line isn't a the latest fit
        "\n\nNO FIT FOUND!!!\n\n"

    return setupYamlEntries, opacityYamlLines


def update_yaml_file(yamlFilename, noHupFilename, saveSolutionFilename=''):
    with open(yamlFilename, 'r') as file:
        data = file.readlines()
        active = data[37].split(': ')[1].split('\n')[0]
        vref = float(data[9].split(': ')[1].split('\n')[0])
    setupEntries, ionInfoEntries = read_last_fit(noHupFile=noHupFilename, active=active, saveSolutionFilename=saveSolutionFilename, vref=vref)

    if 'a0' not in data[28] or 'start' not in data[42]:
        print("\n\nInconsistently formatted file!!!\n\n")
        return

    data[28] = '    a0           : { fixed:  No, start:  %6s, lower:   0.00, upper:  10.00, scale:   1.00 }\n' % (float(str(setupEntries[0])))
    data[29] = '    a1           : { fixed:  No, start:  %6s, lower: -10.00, upper:  10.00, scale:   1.00 }\n' % (float(str(setupEntries[1])))
    data[30] = '    a2           : { fixed:  No, start:  %6s, lower: -10.00, upper:  10.00, scale:   1.00 }\n' % (float(str(setupEntries[2])))
    data[31] = '    v_phot       : { fixed:  No, start:  %6s, lower:   5.00, upper:  40.00, scale:   1.00 }\n' % (float(str(setupEntries[3])))
    data[32] = '    v_outer      : { fixed:  No, start:  %6s, lower:  15.00, upper:  60.00, scale:   1.00 }\n' % (float(str(setupEntries[4])))
    data[33] = '    t_phot       : { fixed:  No, start:  %6s, lower:   5.00, upper:  60.00, scale:   1.00 }\n' % (float(str(setupEntries[5])))

    data[42] = '        start    : %s\n' % (ionInfoEntries[0])
    data[48] = '        start    : %s\n' % (ionInfoEntries[1])
    data[54] = '        start    : %s\n' % (ionInfoEntries[2])
    data[60] = '        start    : %s\n' % (ionInfoEntries[3])
    data[66] = '        start    : %s\n' % (ionInfoEntries[4])

    print(data)
    print(setupEntries)
    print(ionInfoEntries)

    with open(yamlFilename, 'w') as file:
        file.writelines(data)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Enter only two arguments: yamlFilename nohupFilename")
    else:
        yamlFile = str(sys.argv[1])
        noHupFile = str(sys.argv[2])
        try:
            update_yaml_file(yamlFilename=yamlFile, noHupFilename=noHupFile)
        except:
            print("Error: Invalid file")
            exit(1)

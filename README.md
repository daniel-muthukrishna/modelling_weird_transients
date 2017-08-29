# modelling_weird_transients
Modelling supernova with synapps

## Explanation of files and steps to model supernova

### Step 1. deredshift_spectrum_file.py
This is the first thing that should be run on a new spectrum. It deredshifts a file, normalises it, and smooths it. It takes a 3 column file with wavelength, fluxes and fluxErrors. If the errors are not given, it assumes the error is 3%o f the flux values. It should be run in the command line as follows:
```bash
python deredshift_spectrum_file.py filename redshift smooth
```
where filename is the path to the spectral data file, redshift is a float, and smooth is optional and is an odd-numbered integer which represents how much to smooth the spectrum. 1 means no smoothing. Example usage as follows:

```bash
python deredshift_spectrum_file.py spectrum_file.dat 0.12 3
```

### Step 2. Saved_Fits Directory
Create a subdirectory in Saved_Fits/ representing the name of the spectrum you are modelling (e.g. spectrum_name). In this directory, save all data files, deredshifted files, and other information to do with the particular spectrum.

Create a synapps yaml file in this new subdirectory.

### Step 3. auto_run_XXXX.sh
Run the following in the command line in the path that you will be running synapps on this spectrum:
```bash
nohup ./auto_run_XXXX.sh
```

Before this, you will need to open the corresponding run_synapps_XXXX.sh file you created and edit it to the particular synapps yaml file you are using, and the particular number of cores and processes you will be using.

Next, you should create the particular auto_run_XXXX.sh to be consistently named to the spectrum that you will be modelling. Change only lines 2, 11 and 12 in this file to correspond to your spectrum and yaml files.

This step will take several hours or days.

### Step 4. make_synplus_plus_yaml.py
After a while, the best solution so far by synapps is stored in the created nohup_XXXX.out file that has been saved by the previous steps. The make_synplusplus_yaml_files.py can read in this nohup file and produce plots and tables which make the data solution human-readable.

The only thing you will need to add are 2 lines to the bottom of this file. These are:

```python
directory1 = "Saved_Fits/spectrum_name/"
make_plots(directory=directory1, noHupFilename='nohup_XXXX.out', yamlFilename='spectrum_name.yaml',
           dataFilename='spectrum_name_restFrame_smooth1.txt', minLogTauPlot=-1, minImportantLogTau=False,
           plotIonsList=[])
```

These 2 lines will produce the following:
 1. A plot of the best fit model against the spectrum data along with the contrinution of the best fit ions. (And other plots depending on arguments - see below).
 2. It will also create a file called ion_parameters.csv which lists the opacity parameters for the model.
 3. It will also update the Synapps yaml file to be initialised to the parameters of the best fit solution in the noHup file.
 4. It also creates a subsubdirectory containing syn++ yaml files for each particular ion. Which create the ion fits that are plotted.
 
Explanation of the two line of code as follows:

directory1 is the subdirectory you created in Step 2.

Then, the make_plots function takes several arguments, and the directory, noHupFilename, yamlFilename should be consistent with the files you've been using so far. 

dataFilename should be the name of the deredshifted spectrum that was created in Step 1.

minLogTauPlot dictates how many of the ion contributions to plot along with the model. The plot will display all ion lines which have a calculated log_tau_opacity greater than this value.

minImportantLogTau is a boolean. If set to True, it will make a second plot which shows what the model would look like if it only used the ions that have a logtau above minLogTauPlot.

plotIonsList takes a list of ion names. If this is non-empty, it will create another plot showing how the model would look if you only had the ions in this list.





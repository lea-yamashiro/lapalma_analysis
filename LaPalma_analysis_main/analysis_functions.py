
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import glob
import pandas as pd 
import scipy as sp 
import scipy.stats as sps
import astropy
from astropy.io import fits
from scipy.stats import poisson
import statsmodels as sm
from scipy.special import gammaln
from matplotlib.ticker import MultipleLocator, AutoMinorLocator


def import_txts_get_arrays(folder_in_data_dir):  # this argument is a string
    '''
    This function: takes files from .txt in the data directory
    that holds the files that were output from the fits_to_txt_v3.py
    and takes those files, loads them in as numpy arrays, and then 
    creates an output of 2D wavelength arrays and flux arrays 
    
    input: 
    - exact folder where the data was originally (the "full" is included in the function) 
    output: 
    - 2 2D arrays 

    need to change per person: 
    - data_dir_path: wherever your general data folder is living 
    '''

    data_dir_path = '/Users/leayamashiro/AnA_MSc/Observations/LaPalma_analysis/data/' 
    files_glob = glob.glob(str(data_dir_path) + folder_in_data_dir + 'full/*.txt')
    wavelength_arrays = []
    flux_arrays = []
    for file in files_glob: 
        spectrum = np.loadtxt(file)
        spectrum_flux = spectrum[:,1]
        spectrum_wavelength = spectrum[:,0]
        flux_arrays.append(spectrum_flux)
        wavelength_arrays.append(spectrum_wavelength)
    return wavelength_arrays, flux_arrays


def check_length_all_spectra(wavelength_arrays): 
    ''' Just if you want to check the length of your spectra '''
    for i in range(len(wavelength_arrays)): 
        wavelength_array = wavelength_arrays[i]
        print(len(wavelength_array)) 

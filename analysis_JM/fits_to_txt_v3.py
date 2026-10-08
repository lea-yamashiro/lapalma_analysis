"""
==============================================================
FITS → text spectra converter
==============================================================

This script converts a directory of 1D spectra in FITS format into plain text files containing wavelength-flux pairs.

Outputs:
- directory/full/       : spectra with NaNs removed
- directory/rebinned/   : spectra rebinned onto a uniform linear wavelength grid
- directory/bdj_log.txt : summary of each FITS file (object, date, exposure, BJD, etc.)
- directory/bdj_list.txt: list of rebinned spectra with corresponding BJDs

Usage:
1. Adjust the directory to where you have stored your data
2. Optionally adjust rebinning parameters in the function call (rebinned_wavelength_step, min_wavelength, max_wavelength).
3. Run the script
4. Processed spectra and logs will appear in new subfolders inside your FITS directory.

Dependencies:
- numpy
- astropy
- specutils

# new 
"""

from astropy.io import fits
from astropy import units
import numpy as np
import glob
import os
from specutils import Spectrum
from specutils.manipulation import FluxConservingResampler
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument('--directory', '-d')
args = parser.parse_args()
directory = str(args.directory)

def rebin_spectrum(wavelengths, flux, wavelengths_rebinned):
    spec = Spectrum(spectral_axis=wavelengths*units.AA, flux=flux*units.Unit("erg cm-2 s-1 AA-1"))
    resampler = FluxConservingResampler()
    spec_rebinned = resampler(spec, wavelengths_rebinned*units.AA)
    return spec_rebinned.flux.value

def fits_to_txt(directory, rebinned_wavelength_step=0.1, min_rebinned_wavelength = 3800, max_rebinned_wavelength = 8900):
    # List all fits files in the given directory
    fits_file_names = glob.glob(os.path.join(directory, "*.fits"))

    # Define log file names
    log_file = open(directory + "bdj_log.txt_test", "w")
    bjd_list_file = open(directory + "bdj_list.txt", "w")
    
    log_file.write("index,full_file_name,date_avg,exposure_time,bjd,bvcor\n")

    # Define directories for txt files
    full_directory = directory + "full/"
    rebinned_directory = directory + "rebinned/"
    os.makedirs(full_directory, exist_ok=True)
    os.makedirs(rebinned_directory, exist_ok=True)

    # Go through all files
    for i, fits_file_name in enumerate(fits_file_names):
        with fits.open(fits_file_name) as fits_file:
            file_name_only = os.path.basename(fits_file_name)
            print(f"Reading {file_name_only}, {i+1}/{len(fits_file_names)}")

            header = fits_file[0].header
            flux = fits_file[0].data

            # Read observation information
            object_name = header['OBJECT']
            unseq = header['UNSEQ']
            date_avg = header['DATE-AVG']
            try: bjd = header['BJD']
            except KeyError: bjd = 0.0
            try: bvcor = header['BVCOR']
            except KeyError: bvcor = 0.0
            exposure_time = header['EXPTIME']

            # Read wavelength information
            min_wavelength = header['CRVAL1']
            wavelength_step = header['CDELT1']
            no_wavelengths = header['NAXIS1']
            wavelengths = np.exp(np.arange(no_wavelengths)*wavelength_step + min_wavelength)

            # # Remove nans from flux
            # no_nan = np.sum(np.isnan(flux))
            # wavelengths_wo_nan = wavelengths[no_nan:]
            # flux_wo_nan = flux[no_nan:]
            # data_wo_nan = np.column_stack((wavelengths_wo_nan, flux_wo_nan))

            # Rebin spectrum
            wavelengths_rebinned = np.arange(min_rebinned_wavelength, max_rebinned_wavelength, rebinned_wavelength_step)
            flux_rebinned = rebin_spectrum(wavelengths, flux, wavelengths_rebinned)
            data_rebinned = np.column_stack((wavelengths_rebinned, flux_rebinned))

            # Save data without nans
            full_file_name = object_name + "_" + str(unseq) + ".txt"
            np.savetxt(full_directory+full_file_name, data_wo_nan, fmt="%.5f %.2f", delimiter=' ')

            # Save rebinned data
            rebinned_file_name = object_name + "_" + str(unseq) + "_rebinned.txt"
            np.savetxt(rebinned_directory + rebinned_file_name, data_rebinned, fmt="%.5f %.2f", delimiter=' ')

            # Write to log files
            log_file.write(str(i+1).zfill(3) + ', ' + full_file_name + ',' + str(date_avg) + "," + str("{:5.1f}".format(exposure_time)) + ',' + str("{:14.6f}".format(bjd))+ ',' + str("{:10.6f}".format(bvcor))+"\n") # write *.txt file with all data points
            bjd_list_file.write(rebinned_file_name +' '+ str("{:14.6f}".format(bjd))+"\n")
    
    log_file.close()
    bjd_list_file.close()

args = parser.parse_args()
# The directory containing your .fits files:
fits_to_txt(directory)

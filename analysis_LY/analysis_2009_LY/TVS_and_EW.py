# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 02:51:05 2018

@author: Annelotte
"""

import pyfits as pf, numpy as np
from pysynphot import observation
from pysynphot import spectrum
import matplotlib.pyplot as plt
from astropy.modeling import models, fitting
from scipy.interpolate import interp1d, UnivariateSpline
from scipy.optimize import leastsq
from scipy.optimize import curve_fit
import glob, os
import scipy.optimize
import re
import scipy.stats

###############################################################################
############################ Files and constants ##############################
###############################################################################

# Lines 
Ha_6563 = 6562.852
Hb_4861 = 4861.332
Hg_4341 = 4340.472
Hd_4102 = 4101.734
He1_5876 = 5875.621
He1_4713 = 4713.145
He1_4471 = 4471.480
He1_4026 = 4026.191
He2_5412 = 5411.521
He2_4686 = 4685.804
He2_4542 = 4541.591
He2_4200 = 4199.87
O3_5592 = 5592.37
C4_5801 = 5801.33

# speed of light
clight = 299792.458

# specify star and line
wl_line = He2_4686
line = 'He2_4686'
star = 'xiPer'

# create list of all files including path
years = glob.glob('txt_files/' + star + '/*/')
for y in years:
  file_list = glob.glob(y + '/' + star + '_' + line + '*.txt')

# obtain the right continuum boundary conditions
names = ['Ha_6563', 'Hb_4861', 'Hg_4341', 'Hd_4102', 'He1_5876', 'He1_4713', 'He1_4471', 'He1_4026', 'He2_5412', 'He2_4686', 'He2_4542', 'He2_4200', 'O3_5592', 'C4_5801']
bound_ops = np.genfromtxt('Information/' + star + '_continuum_boundaries.txt', 
                          skip_header=2)
for i, name in enumerate(names):
  if name == line:
    inter_bounds = np.array(bound_ops[i][1:5])

###############################################################################
################################# Functions ###################################
###############################################################################

def TVS(file_list, con_bounds, xlim):
    ''' Overplot the different spectra of the line of the star and plot the 
    relative differences between the different spectra'''
    stds_con = []
    means_con = []
    stds_obs_vel = []
    vel_plot = []
    flux_plot = [] 
    julians = []
    
    count = 0

    for file in file_list:
      data = np.genfromtxt(file)
      vel = data[:,0]
      flux = data[:,1]
      vel_plot.append(list(vel))
      flux_plot.append(list(flux))

      if len(file) > 55:
        julians.append(float(file[len(y)+3+len(star)+len(line)+12:-4]))
      else:
        julians.append(float(file[len(y)+3+len(star)+len(line):-4]))
      
      c1a = np.where(vel >= con_bounds[0])[0][0]           # Boundaries for continuum from command line
      c1b = np.where(vel >= con_bounds[1])[0][0]
      c2a = np.where(vel >= con_bounds[2])[0][0]
      c2b = np.where(vel >= con_bounds[3])[0][0]    

      # calculate std and mean flux of the continuum
      flux_c = np.concatenate([flux[c1a:c1b], flux[c2a:c2b]])     # Flux in the selected continuum parts
      std_con = np.std(flux_c)
      stds_con.append(std_con)
      means_con.append(np.mean(flux_c))
      
      # create empty lists to compare fluxes at velocities of the diff spectra
      if count == 0 :
        for i in range(0, len(vel)):
          stds_obs_vel.append([])
      count += 1
      
      # append fluxes of all spectra for all velocities specific
      for i, f in enumerate(flux): 
          stds_obs_vel[i].append(f)
    
    # calculate std and mean flux per velocity 
    sigma_observed = []
    mean_flux = []
    for flux_per_vel in stds_obs_vel:
      sigma_observed.append(np.nanstd(flux_per_vel))
      mean_flux.append(np.nanmean(flux_per_vel))
    
    sigma_expected = np.nanmean(stds_con) * np.sqrt(mean_flux)

    # plotting
    fig = plt.figure()    
    ax1 = fig.add_axes([0.25, 1.25, 1.75, 1])
    plt.title('TVS - ' + star + ' - ' + line, fontsize=18)
    plt.grid(True)
    ax1.set_xticklabels([])
    ax1.set_xlim(-xlim, xlim)
    for i , flux in enumerate(flux_plot):
      ax1.plot(vel_plot[i], flux)
    ax1.set_ylabel('normalized flux (' + str(len(flux_plot)) + ' spectra)', fontsize=15)
    
    ax2 = fig.add_axes([0.25, 0.25, 1.75, 1])
    plt.grid(True)
    ax2.set_xlim(-xlim, xlim)
    ax2.set_ylabel('sigma-observed / sigma-expected', fontsize=15)
    ax2.set_xlabel('Velocity (km/s)', fontsize=15)
    ax2.plot(vel, np.array(sigma_observed)/np.array(sigma_expected))
    plt.axhline(y=1, color='red', linestyle='--')

    if save == True:
      plt.savefig('Plots/' + star + '/TVS_' + star + '_' + line)
      
    plt.show()
    
    return vel_plot, flux_plot, stds_con, means_con, julians


def interactive_boundary(question):
    "Function to get 2 values (i.e. wavelengths) from user input"
    correct_input = False
    while correct_input == False:
        print question
        bs = raw_input()
        bs = bs.split(',')
        if len(bs) == 2:
            if bs[0].strip('-').isdigit() and bs[1].strip('-').isdigit():
                bound1 = float(bs[0].strip( ))
                bound2 = float(bs[1].strip( ))
                correct_input = True
            else:
                print 'Please enter valid numbers (no text and spaces)'
        else:
            'Please enter the 2 numbers seperated by a comma'
    return bound1, bound2


def vtow2(vel, w0):
   "Convert velocity (km/s) to wavelength units (Angstrom)"
   wave = w0*(vel/clight)  # wave becomes array if vel is an array
   return wave

 
def my_model2(t, A, w, c):  
  """Sine fuction to fit""" 
  return A * np.sin(np.pi*w*t)+c


def ChiSq(parm, xval, yval, dy): 
    """the weighted least-squares"""
    ymod = my_model2(xval, *parm)
    chisq = sum(pow((yval-ymod)/dy,2))
    return chisq
 

def EW(vels, flux_plot, w0, left_bound, right_bound, stds_con, means_con, julians):
    """Calculating equivalent width including error and plot over time"""
    ews_sum = []
    errs_sum = []
    
    for i, flux in enumerate(flux_plot):
      vel = np.array(vels[i])
      flux = np.array(flux)
      std = stds_con[i]
      mean_fluxc = means_con[i]

      ew1 = np.where(vel >= left_bound)[0][0]
      ew2 = np.where(vel >= right_bound)[0][0]
  
      summed = 0
      for i in range(ew1, ew2):
          dl = abs(vel[i+1] - vel[i])
          summed += (1. - flux[i])* dl
  
      dlambda = abs(vel[ew1]) + abs(vel[ew2])
      error_s = np.sqrt(1 + (mean_fluxc/np.mean(flux[ew1:ew2])))*(dlambda - summed)/(1./std)

      summed_eq_width_angstrom = vtow2(summed, w0)
      error_s_angstrom = vtow2(error_s, w0)
      
      ews_sum.append(summed_eq_width_angstrom)
      errs_sum.append(error_s_angstrom)
    
    dates = np.array(julians)
    
#    guess = [-.05, .2, 0.5, 1]    
#    popt, pcov = scipy.optimize.curve_fit(sinfunc, dates, ews_sum, p0=guess)
#    A, w, c, p= popt
#    print popt
    flux2 = ews_sum
    error2 = errs_sum
    time = dates
    
    plt.figure(figsize=(16, 10))
    plt.title('EW over time for ' + line + ' in ' + star)
    plt.grid(True)
    
    if fit == True:
      p0 = [0.1, 5, 0.35] #, 500000, 0.35]
      popt, pcov = scipy.optimize.curve_fit(my_model2, time, flux2, p0, sigma=error2)
      print popt
      dof = len(flux2)-len(popt)
      print "Weighted least-squares fit results:"
      print "with chi-squared = " + str(round(ChiSq(popt, time, flux2, error2), 2)), "for " + str(dof) + " d.o.f.."
      print "The goodness of fit of the model is: " + str(scipy.stats.chi2.sf(ChiSq(popt, time, flux2, error2), df=dof))
      print "Minimum Chi-squared = " + str(ChiSq(popt, time, flux2, error2)) + " for " + str(len(time)-len([4., 0.1, 1., 16.])) + " d.o.f."
      print "The reduced chi-squared = ", round(ChiSq(popt, time, flux2, error2)/dof, 2)
      plt.plot(dates, my_model2(time, *popt), label='Fitted function')

    plt.errorbar(dates, ews_sum, yerr=errs_sum, marker='s', fmt='o')
    plt.xlabel('Julian date')
    plt.ylabel('Equivalent width in A')
    plt.legend()
    
    if save == True:
      plt.savefig('Plots/' + star + '/EW_over_time_' + star + '_' + line)
    plt.show()


def main():
  global save
  save = False
  
  global fit
  fit = True
  
  xlim = 700
  vel_plot, flux_plot, stds_con, means_con, julians = TVS(file_list, inter_bounds, xlim)
  
  print 'Calculate EW for this file? y/n'
  calculate_ew = raw_input()
  if calculate_ew.lower() == 'n':
    return    
  
  question = 'Please enter the left and right boundary for calculating the EW in km/s <b1,b2>'
  ew_bound_left, ew_bound_right = interactive_boundary(question)

  EW(vel_plot, flux_plot, wl_line, ew_bound_left, ew_bound_right, stds_con, means_con, julians)


if __name__ == "__main__":
    main()


"""
This script helps you in a normalising spectrum.
PS: if used the right way:)

Credits : Michael Stroet (cleaned up the base code and structered it clearly ) &
          Vysakh (added few new functionalities, UI/UX upgrades,and the documentation )

          ♫ solemn music ♫
          We dont need anything in return. We just ask for you to remember us when someone
          comes to you asking about how to normalise a spectrum...
          ♫              ♫

Last updated: 02-06-2024




>>>>>>>>>>>> DISCLAIMER <<<<<<<<<<<<<<

The previously existing one (made by Annelotte) was a really helpful version to perform spectral normalisation definitely. But first Michael, and then myself,
thought why not make it a little bit cleaner and with a few more functionality for ease of use. So we just sat down for around a week (with a 
gap of an year in between, different batches) to make this somewhat cleaner one.

Also, there is a chance this might crash if some mixed instruction are given. We were not able to test this extensively. So if that happens.. sorry.
Just restart it and it should work fine.

Any passive aggresiveness found in this code is completely accidental or you are just imagining it;)




>>>>>>>>>>> DOCUMENTATION <<<<<<<<<<<<

MAKE SURE YOU HAVE regex MODULE INSTALLED. REST OF THEM ARE PRETY MUCH BASIC ONES

*SUGGESTED TO RUN IT IN MAXIMISED SCREEN*

TOOLBAR:
    The toolbar above the plot is a default setting from matplotlib. Use that to zoom(in/out) and move around plot.
    For more info : https://matplotlib.org/3.2.2/users/navigation_toolbar.html
    (personally only the pan button and zoom to rectangle button is useful for us)

    For all the following tasks, MAKE SURE THAT NO OPTION IN THE TOOLBAR IS SELECTED.
    ALSO ALWAYS KEEP AN EYE ON THE TERMINAL WINDOW FROM WHICH THIS IS RUN. THERE ARE SOME PRINT STATEMENTS CONTAINING INFO ON WHAT IS HAPPENING

>>>> Inputs are ONLY possible on the upper plot <<<<

MOUSE INPUTS :
    Left click : selects points through which the continuum should fit the spline model
                    There 2 methods of selection : Median-approximated & non-assited

                    THESE METHODS ARE BETTER UNDERSTOOD IF YOU JUST PLAY AROUND THE PLOT RATHER THAN READING THIS.
                    BUT FOR THE NERDY PEOPLE....
                    
                    Median-approximated :
                        Clicking a point anywhere along the y axis, will automatically select the point at the median of 
                        the data in a 0.5 angstrom window of the selected x axis
                    non-assisted : 
                        Completely free selection of any point inside the plot without assistance from the existing data
    
    Right click : if you right click on the point you have already made, this deletes the point.
                    (it is kind of hard to do this, since the points are very small, so read the other method of deletion )

    Right click Rectangle : If you draw a rectangle by right clicking, this will select the points inside the drawn rectangle. 
                                Which can be deleted by pressing 'd'.

KEYS : 
    ENTER : Pressing ENTER after selecting atleast 3 points on the upper plot, fits a spline to the selected points and displays the 
            the normalised spectrum in the lower window.
            It also saves the selected points to the template folder created.

    d     : once the right-click-rectangle is drawn, pressing d will delete the points inside this. Once deleted, pressing ENTER will 
            fit the spline model to the remaining set of points.
    
    r     : Resets the plot, removing all existing points from the window (hopefully you dont have to use this. we haven't tested this
            one a lot, so if it runs into an error(fingers crossed), just let us know so that we can figure it out)

    w     : Writes the normalised model to the "normalised" folder. Also saves the plot in the image folder too.

    l     : Load the points from the previously saved template.

    m     : Toggle between median-approximated and non-assisted point selection methods.

    j     : Once the points are loaded from the template, this will use the x values of the template points to pull down the template y values
            to scale it to the current data (WOULD BE VERY USEFUL IF YOU ARE TRYING NORMALISE MULTIPLE SPECTRA OF THE SAME SOURCE MULTIPLE TIMES)
            More details on how it works follows.
    

So since that's done, let me give a quick outline on how to put this into action.


>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


HOW TO LOAD FROM PREVIOUS TEMPLATE:

!!!!!!!!!!!!!!!!       DEFINETLY SUGGEST YOU TRY TO UNDERSTAND THIS (IF MULTIPLE SPECTRA OF SAME SOURCE ARE INVOLVED), 
!!!!!!!!!!!!!!!!          YOU ONLY HAVE TO NORMALISE ONE SPECTRA, AND CAN REUSE THE TEMPLATE FOR ALL THE REST.
!!!!!!!!!!!!!!!!                                          SAVES A LOTTTT OF TIME!!!

So I think we can collectively agree that normalising spectra, after selecting the first 5 points, becomes the most boring thing ever. But what if you donot
need to do that anymore(As long as you are observing the same source).

Introducing the template-loader(too lazy to think of a cooler name, be my guest in naming it.... if you are as bored as me)



HOW TO:
1---> Normalise and save atleast one spectra to create the template file
2---> Open a new spectra and press 'l', this will load points from the template spectra
3---> Once points are loaded, press 'j', this will adjust the old template to the current one.


So getting serious, how does it work...
Every time you select points and press enter, the selected points are being saved as a txt file inside the normalised/template folder in your system. There already
existed a feature (pressing l) which loaded the previous template to the current window, but even though the source remains the same, the counts will change in different
exposures hence rendering this feature hard to use.

With this, once you load the previous datapoints by pressing l, and then if you press j, this will pull down the point by scaling it to the current data. 
Behind the scenes what happens is that, Once the points are loaded, the algorithm uses the x values of template to select x values of the current spectra. Once these are selected, it discards
the template y values, and replaces it with the median of 0.5 angstrom window around the corresponding x value, hence making it the new y value. 
This will easily help us reuse the selected points in a usefull manner, cutting down our work by a lot.

POINTS TO REMEMBER.
> Only works for repeated observations of the same source, since the lines could shift signfiicantly otherwise.
> You need to do the normalisation manually for atleast one source. Once you save the first one. you can start reusing the template for every other exposures.
> Try not to select points too close(inside the range of velocity shifts) to absorption or emission lines, as the old points might just fall into a line.
> ALWAYS DOUBLE CHECK THE NORMALISED SPECTRA. EVEN THOUGH THE ALGORITHM WILL HELP, IT IS ADVISED TO CHECK THE NORMALISED SPECTRA, IF IT HAPPEN TO ACCIDENTLY FALL
  ON A LINE.

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


STEPS TO NORMALISE SPECTRA:

-> First make a folder with the txt files containing wavelength and flux values of the spectrum. 
    Assign the path to the folder to the variable "spectrum_dir"
    In the code here, the folder is called "Normalisation", containing the txt files. 

-> Once this is done, run this python script using an editor or just using the command line. Whichever works for you.

            python <path-to-the-file>/normalise_spectrum.py

    btw, ALWAYS KEEP A LOOK AT THE COMMAND WINDOW FROM WHICH YOU RUN IT SINCE print COMMANDS return the values in the command line.
    PS : I used VScode( have an inbuild command window display).

-> Once the code is run, it opens the first file (alphabetically sorted) in 'spectrum_dir'. Also it creates a new folder named 'normalised' 
    with subfolders 'images' and 'templates' inside the "spectrum_dir" (to store stuff)

-> Once it is open, it is pretty direct. 
    Just select at least 3 points in the spectra, and then press ENTER to make it show the normalised spectra. 
    And as mentioned previosly, you can use both median-approximated or non-assited using "m" to change between them. There is a 
    warning in the plot itself to let you know which one is that you are using

    Let's say you made a mistake and you need to delete some points. Just draw a rectangle right clicking and once all
    the points are selected, press "d". It will make it all your problems go away. Now press ENTER and voila!!. You have a fit without those points.

-> Once you are happy with the continuum fit and the normalised spectra, you can press "w" to write the normalised file to "normalised"
    folder in the spectrum_dir. This also saves the plot as an image in the "images" folder. You can get a confirmation if it saved by looking
    at the terminal(There is a confirmation prompt after saving) or for those who dont trust this code (we dont either), go and have a look at the folder whether
    a new file have been created or not.

-> If you have multiple txt files inside the spectrum_dir, once you close the plot, it automatically opens the next one on the list.
    This can be bypassed using an if condition in the for loop in the main snippet, by prioviding the name of the file you need to open.
    I have provided the code for that (it is commented by default)

And TA-DA!! there you go!!. You have the normalised spectrum to work (cry over) with for the next few months.

If you have any doubts, the codes is pretty straigtforward, have a look, you can pretty much figure it out. And ofcourse, we are happy to help you with it too.

Happy normalising! :)

"""

import os, sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import FigureCanvasBase
from matplotlib.widgets import RectangleSelector
from matplotlib.patches import Rectangle
import matplotlib.transforms as transforms
plt.rcParams.update({'font.size': 14})
import re
import warnings
warnings.filterwarnings('ignore')
from pathlib import Path

from scipy.interpolate import splrep, splev

global pointCOUNTER # counter for points used for deleting function
pointCOUNTER = 0

def find_closest_index(arr, target):
    '''
    Just some details.
    '''
    closest_index = 0
    closest_difference = abs(arr[0] - target)

    for i in range(1, len(arr)):
        difference = abs(arr[i] - target)
        if difference < closest_difference:
            closest_index = i
            closest_difference = difference

    return closest_index

def loadTxtFiles(dir):
    """
    Find and open the .txt files to extract the spectra
    Returns a dictionary of the filenames and spectra
    """
    # Find all .txt files in the directory
    contents = os.listdir(dir)
    txt_files = [file for file in contents if file.split(".")[-1] == "txt"]

    txt_files.sort()

    if len(txt_files) == 0:
        print(f"\n WTH!! Where are the files in {dir}???\n")
        exit(1)

    # Extract the spectra
    file_contents = {}
    for file in txt_files:
        spectrum = np.genfromtxt(os.path.join(dir, file))
        file_contents[file] = spectrum
    
    return file_contents

def plot_vertical_line(ax, x_position, text, c='blue', ypos = 0.2, boxalpha = 1, textalpha=0.3):
        '''
        Function to plot vertical line with given text as part of it 
        '''
        ax.axvline(x=x_position, color=c, linestyle='--', alpha=0.3, zorder=1)
        
        trans = transforms.blended_transform_factory(ax.transData, ax.transAxes)
        
        ax.text(x_position, ypos, text, color=c, bbox = dict(facecolor = 'white',edgecolor = 'none', alpha =boxalpha),
                ha='center', va='center', transform=trans, rotation = 90, fontsize = 13 ,alpha=textalpha, zorder=2, weight='bold')


def refreshPlot(x, y, contin = [None], point_coords= [], label = "spectrum", flag='p'):

    """
    Refresh the spectrum plot with a bunch of other stuff.
    """
    
    ax[0].cla()
    ax[0].set_xlabel(r'$Wavelength\;[\AA]$')
    ax[0].set_ylabel(r'$Flux\;[arbitrary]$')
    ax[0].plot(x, y, "k-", label = 'spectrum')
    ax[0].set_ylim(min(y)-1000, max(y)+1000)
    ax[0].set_xlim(min(x)-100, max(x)+100)
    ax[0].grid(axis='x')
    plot_vertical_line(ax[0], 6562.81, r'$H\alpha$', ypos=0.7, c='blue')
    plot_vertical_line(ax[0], 4861.35, r'$H\beta$', ypos=0.7, c='blue')
    plot_vertical_line(ax[0], 4340.472, r'$H\gamma$', ypos=0.7, c='blue')
    ax[0].set_title('Orginial Spectum', fontsize=16, weight='bold')
        
    if len(point_coords)!=0:

        for k in range(len(point_coords)):        
            ax[0].plot(point_coords[k,0], point_coords[k,1], 'rs', label = 'point'+str(k))
            if (len(point_coords)>=3) & (contin[0]!=None):
                ax[0].plot(WAVE, contin, "r-", label="continuum")
        pointCOUNTER = len(point_coords)

    if flag=='n':
        ax[1].cla()
        ax[1].set_title('Normalised spectrum', fontsize=16, weight='bold')
        ax[1].set_xlabel(r'$Wavelength\;[\AA]$')
        ax[1].set_ylabel(r'$Flux\;[arbitrary]$')
        plot_vertical_line(ax[1], 6562.81, r'$H\alpha$', ypos=0.1, c='blue')
        plot_vertical_line(ax[1], 4861.35, r'$H\beta$', ypos=0.1, c='blue')
        plot_vertical_line(ax[1], 4340.472, r'$H\gamma$', ypos=0.1, c='blue')

        if len(point_coords)<3:
            ax[1].text(6400, 0.4,  "Don't be too lazy!!\nselect atleast 3 points and then press ENTER!!", fontsize=14, horizontalalignment='center')

        else:
            normalised = y/contin
            ax[1].axhline(1, ls='-.', color = 'b', lw = 3, label = r'$y = 1$')
            ax[1].plot(x, normalised, "k-", label="normalised")

            xleft = find_closest_index(x, point_coords[0,0])
            xright = find_closest_index(x, point_coords[-1,0])

            #ax[1].set_ylim(min(normalised[15000:55000])-0.5, max(normalised[15000:55000])+0.5)
            ax[1].grid(axis='x')
            ax[1].legend(loc = 'upper right')
    global medianAPPROX
    plt.suptitle(FILENAME + '\n' + medianApporx_str(medianAPPROX), horizontalalignment='center')




# -------------------------------------------------------------------------------------------------
# Normalisation code based on http://python4esac.github.io/plotting/specnorm.html
# -------------------------------------------------------------------------------------------------

def onClick(event):
    """
    When none of the toolbar buttons are activated and the user clicks in the
    plot somewhere, create a point at the clicked location.
    """
    global pointCOUNTER
    global medianAPPROX

    toolbar = plt.get_current_fig_manager().toolbar
    if event.button == 1 and toolbar.mode == "":

        if medianAPPROX:    # selects the point using median approximation of the data itself
            if event.xdata==None or event.ydata==None:
                print("That click was outside the plot")
            else:                
                window = ((event.xdata-.25)<=WAVE) & (WAVE<=(event.xdata+.25))
                y = np.median(FLUX[window])
                ax[0].plot(event.xdata,y,'rs',ms=6,picker=10,label='point'+str(pointCOUNTER))
                pointCOUNTER+=1
                plt.draw()
        else:               # completely used dependant selection of point selection. No inference from data
            x = event.xdata
            y = event.ydata
            if x == None or y == None:
                print("That click was outside the plot")
            else:
                ax[0].plot(x, y, "rs", ms=6, picker=10, label="point"+str(pointCOUNTER))
                pointCOUNTER +=1
                plt.draw()

def onPick(event):
    """
    When the user clicks right on a continuum point, remove it
    """
    if event.mouseevent.button==3:
        if hasattr(event.artist,"get_label") and bool((re.search('point',str(event.artist.get_label())))):
            event.artist.remove()
            plt.draw()


def is_point_inside_rectangle(x, y, rect_x, rect_y, rect_width, rect_height):
    '''
    Checks if a given point is inside a given rectangle for deletion
    '''
    if (rect_x <= x <= rect_x + rect_width and rect_y <= y <= rect_y + rect_height):
        return True
    else:
        return False
    

def remove_items_inside_rectangle(rectangle):
    '''
    Function to remove the items inside the rectangle
    '''
    artist_list = []
    for k,artist in enumerate(ax[0].get_children()):
        if hasattr(artist,"get_label") & bool((re.search('point',str(artist.get_label())))):
                    x, y = artist.get_data()                    
                    if is_point_inside_rectangle(x[0], y[0], rectangle.get_x(), rectangle.get_y(), rectangle.get_width(), rectangle.get_height()):
                        artist_list.append(artist)
                    
    for k,artist in enumerate(artist_list):
                artist.remove()

selected_rectangles = []
def on_select(eclick, erelease):
    """
    When a rectangle is drawn, store it in the list of selected rectangles
    """
    x0, y0 = eclick.xdata, eclick.ydata
    x1, y1 = erelease.xdata, erelease.ydata
    rect = Rectangle((min(x0, x1), min(y0, y1)), abs(x1 - x0), abs(y1 - y0), fill=False, edgecolor='red', label='rectangle')
    ax[0].add_patch(rect)
    selected_rectangles.append(rect)
    plt.draw()

def onType(event):
    """
    Is called when the user presses a key
        Enter: Fit a spline-continuum line through the points
        n    : Normalise the spectrum using the continuum fit
        w    : Write the normalised spectrum to a .txt file
        r    : Reset the plot to the original spectrum
        l    : Plot the last-used points from the template dictionary
        d    : Delete points inside the right-click-rectangle
        m    : toggles median-approximation on/off
        j    : to use the loaded point properly. Read the docstrings above on how to use it.
    Ignores all other key presses
    """
    global pointCOUNTER
    # When the user hits "enter"
    if event.key == "enter":
        """ Fit a spline-continuum line through the points """

        # Search for all points
        point_coords = []
        for artist in ax[0].get_children():
            if hasattr(artist,"get_label"):
                if bool(re.search('point',str(artist.get_label()))):
                    coords = artist.get_data()
                    if len(coords[0])!=0:
                        point_coords.append([coords[0][0], coords[1][0]])
                elif artist.get_label() == "continuum":
                    artist.remove()

        if len(point_coords) < 3:
            point_coords = np.array(point_coords)
            print(f"Not enough points were found. {len(point_coords)} < 3")
            refreshPlot(WAVE, FLUX, point_coords=point_coords, flag='n' )

        else:
            # Sort the point coordinates and remove NaNs
            point_coords = np.array(point_coords)
            point_coords = point_coords[np.argsort(point_coords[:,0])]
            point_coords = point_coords[~np.isnan(point_coords).any(axis=1), :]


            # Save the points template to a .txt file
            file = 'template.txt'
            file_path = os.path.join(TEMPLATE_DIR, file)
            np.savetxt(file_path, point_coords)

            # Fit the spline-continuum through the points
            spline = splrep(point_coords[:,0], point_coords[:,1], k=1)
            continuum = splev(WAVE,spline)

            # Add the fitted continuum to the plot
            refreshPlot(WAVE, FLUX, contin=continuum, point_coords=point_coords, label='',flag='n')


    # When the user hits "w"
    elif event.key == "w":
        """ Write the normalised spectrum to a .txt file """

        # Search for the normalised spectrum data and write to file if found
        for artist in ax[1].get_children():
            if hasattr(artist,"get_label") and bool(re.search('normalised',str(artist.get_label()))):
                file = f"{FILENAME.split('.')[0]}_norm.txt"
                file_path = os.path.join(OUTPUT_DIR, file)
                np.savetxt(file_path, np.array(artist.get_data()).T)
                print(f"Wrote to file {file}")

                # Also create an image of the plot
                image = f"{FILENAME.split('.')[0]}_norm.png"
                image_path = os.path.join(IMAGE_DIR, image)
                plt.savefig(image_path, bbox_inches='tight')
                break

    # When the user hits "r"
    elif event.key == "r":
        """ Reset the plot to the original spectrum """
        refreshPlot(WAVE, FLUX)


    # When the user hits "l", loads the last saved template into the current window.
    elif event.key == "l":
        """ Plot the last-used points from the template dictionary """

        # Load the template file, if it exists
        file = "template.txt"
        file_path = os.path.join(TEMPLATE_DIR, file)
        if os.path.exists(file_path):

            # Plot the points
            point_coords = np.genfromtxt(file_path)                
            refreshPlot(WAVE, FLUX, point_coords=point_coords)
        

    # When the user hits j, for calibrating loaded points with current spectra
    elif event.key == 'j':
        point_coords = []
        for artist in ax[0].get_children():
            if hasattr(artist,"get_label"):
                if bool(re.search('point',str(artist.get_label()))):
                    coords = artist.get_data()
                    if len(coords[0])!=0:
                        point_coords.append([coords[0][0], coords[1][0]])
                elif artist.get_label() == "continuum":
                    artist.remove()

        for artist in ax[0].get_children():
            if hasattr(artist,"get_label"):
                if bool(re.search('point',str(artist.get_label()))):
                    artist.remove()
                elif artist.get_label() == "continuum":
                    artist.remove()

        point_coords = np.array(point_coords)
        updated_points = []

        for inde,val in enumerate(point_coords[:,0]):
            window = ((val-.25)<=WAVE) & (WAVE<=(val+.25))
            y = np.median(FLUX[window])
            updated_points.append(y)
        
        point_coords[:,1] = np.array(updated_points)
        pointCOUNTER = 0
        for x, y in zip(point_coords[:,0], point_coords[:,1]):
                ax[0].plot(x, y, "rs", ms=6, picker=10, label = "point" + str(pointCOUNTER))
                pointCOUNTER+=1



    # when user hits "d". For deletion
    elif event.key == 'd':
        ''' 
        to remove elements in rectangle
        '''

        for rect in selected_rectangles:
            remove_items_inside_rectangle(rect)
            rect.set_visible(False)

        # Clear the list of selected rectangles
        for k,artist in enumerate(ax[0].get_children()):
            if hasattr(artist,"get_label") & bool((re.search('rectangle',str(artist.get_label())))):
                artist.remove()
        selected_rectangles.clear()

    # when user hits "m".
    elif event.key == 'm':
        '''
        For toggling between median approximation selection and non-assisted selection 
        '''
        global medianAPPROX
        if medianAPPROX:
            medianAPPROX = False
        else:
            medianAPPROX = True

        plt.suptitle(FILENAME + '\n' + medianApporx_str(medianAPPROX), horizontalalignment='center')
        
    # Apply any updates to the plot
    plt.draw()

# -------------------------------------------------------------------------------------------------
# Main function
# -------------------------------------------------------------------------------------------------

global WAVE             # Wavelengths of the spectrum
global FLUX             # Fluxes of the spectrum
global FILENAME         # Name of the .txt file containing spectra before normalisation
global OUTPUT_DIR       # directory for saving normalised spectra in
global IMAGE_DIR        # directory for saving IMAGES in
global TEMPLATE_DIR     # directory for saving point templates in
global pointCOORDS      # point coordinates of selected points

def medianApporx_str(bool_val):
    '''
    Just some details.
    '''
    if bool_val:
        return r'$\bf{press\;m\;to\;disable\;median\;approximation}$'
    else:
        return r'$\bf{press\;m\;to\;enable\;median\;approximation}$'
    
if __name__ == "__main__":

    global medianAPPROX      # median approximation for point selection
    
    pointCOUNTER = 0
    medianAPPROX =  False

    # Define the Folder which contains the txt file with the flux and wavelengths
    # spectrum_dir = '/Users/leayamashiro/AnA_MSc/Observations/LaPalma_analysis/data/our_data051026/full_median/'
    spectrum_dir = '/home/jade/lapalma_analysis/analysis_JM/data/our_data051026/full'  # combine_2 is the two spectra of day one combined together.
    
    # Get the path to the output directory and create it if it does not exist
    OUTPUT_DIR = os.path.join(spectrum_dir, "normalised")
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    # Get the path to the normalised images directory and create it if it does not exist
    IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")
    if not os.path.exists(IMAGE_DIR):
        os.mkdir(IMAGE_DIR)

    # Get the path to the templates directory and create it if it does not exist
    TEMPLATE_DIR = os.path.join(OUTPUT_DIR, "templates")
    if not os.path.exists(TEMPLATE_DIR):
        os.mkdir(TEMPLATE_DIR)

    # Load the spectra from the .txt files
    file_contents = loadTxtFiles(spectrum_dir)
    # mean_dir = '/home/jade/lapalma_analysis/analysis_JM/data/our_data051026/combine_2/mean_dir'
    # file_contents = loadTxtFiles(mean_dir)  # Load the mean spectrum file instead of the directory

    
    # Begin the normalisation of each spectrum
    for FILENAME in file_contents:
        
        #if FILENAME == '00980594_HRF_OBJ_data_wave.txt':           # Use this line if you dont want to iterate through every files, 
                                                                    # but only one of them in spectrum_dir
            

            # # Get the wavelength and flux data from the spectrum
            # WAVE = file_contents[FILENAME][:,0]
            # FLUX = file_contents[FILENAME][:,1]

            # --- addding for H-alpha stuff --- 

            WAVE_full = file_contents[FILENAME][:,0]
            FLUX_full = file_contents[FILENAME][:,1]
            # Keep only the region around H-alpha (6560) 5550 - 7550 is +/- 1000... 
            mask = (WAVE_full >= 6300) & (WAVE_full <= 6820)

            WAVE = WAVE_full[mask]
            FLUX = FLUX_full[mask]

            # Create the spectrum plot
            fig, ax = plt.subplots(2, 1, figsize = (8,8), sharex=True)

            refreshPlot(WAVE, FLUX)
            ax[0].set_title('Orginial Spectum', fontsize=16, weight='bold')
            ax[1].set_title('Normalised spectrum', fontsize=16, weight='bold')
            ax[1].text(6400, 0.4,  "Don't be too lazy!!\nselect atleast 3 points and then press ENTER!!", fontsize=14, horizontalalignment='center')
            ax[1].grid(axis='x')
            ax[1].set_xlabel(r'$Wavelength\;[\AA]$')
            ax[1].set_ylabel(r'$Flux\;[arbitrary]$')
            


            # Connect the different functions to the different events
            ax[0].figure.canvas.mpl_connect("button_press_event", onClick)
            ax[0].figure.canvas.mpl_connect("pick_event", onPick)
            ax[0].figure.canvas.mpl_connect("key_press_event", onType)
            rs = RectangleSelector(ax[0], on_select, useblit=True,button=[3], minspanx=5, minspany=5)

            plt.show()

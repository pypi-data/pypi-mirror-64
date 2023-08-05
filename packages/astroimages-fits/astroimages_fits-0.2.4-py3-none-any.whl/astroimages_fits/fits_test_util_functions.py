import tempfile
from astropy.io import fits
import numpy as np
import os


def create_empty_fits_files_on_temp_folder(number_of_files, dir=None):

    temp_folder = tempfile.TemporaryDirectory(dir=dir)
    files_list = []

    hdu = fits.PrimaryHDU()
    hdu.data = np.random.random((128, 128))
    hdu.header['TELESCOP'] = 'Unit Tests Telescope'

    for x in range(number_of_files):
        filename = "{}/{}_random_array.fits".format(temp_folder.name, x)
        hdu.writeto(name=filename, overwrite=True)
        files_list.append(filename)

    return temp_folder, files_list

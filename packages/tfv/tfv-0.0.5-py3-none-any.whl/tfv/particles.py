"""A module defining all Particle classes. Particles are the primary objects for ptm data extraction"""

import numpy as np
import datetime as dt
from abc import ABC, abstractmethod
from netCDF4 import Dataset
from tfv.misc import Expression, get_date_num


class Particles(ABC):

    def __init__(self, file):
        """Initializes Extractor object with a ptm results file i.e A TUFLOW FV netCDF4 results file."""

        # Store file path string as attribute
        self.file = file

        # Prepare static Extractor attributes
        self.__prep_file_handle__()
        self.__prep_time_vector__()
        self.__prep_2d_geometry__()
        self.__prep_3d_geometry__()

    @abstractmethod
    def get_raw_data(self, variable, ii):
        """
        Query to extract raw data at a time step (if time-varying).

        Parameters
        ----------
        variable : string
            Name of time varying data set to be extracted.
        ii : integer
            The time vector index at which to extract the data.

        Returns
        -------
        data : np.ndarray
            The raw data as 1D or 2D numpy array
        """
        pass

    @abstractmethod
    def get_mask_vector(self, ii):
        """
        Query to extract an array that defines invalid model data.

        Parameters
        ----------
        ii : integer
            Time index at which to extract the mask array.

        Returns
        -------
        mask : np.ndarray
            Logical index, True if model cells/nodes are invalid (i.e dry cells).

        """
        pass

    @abstractmethod
    def get_vertical_selection(self, ii, datum, limits):
        """
        Query to extract logical index of particles within a given vertical selection at given time step.

        Parameters
        ----------
        ii : integer
            Time index at which to extract the selection.
        datum : {'sigma', 'depth', 'height', 'elevation'}
            Vertical depth-averaging datum i.e sigma, depth, height, elevation, top, bottom.
        limits : tuple
            Vertical depth-averaging limits (z1, z2) relative to vertical datum.

        Returns
        -------
        lgi : np.ndarray
            A logical index for particles within specified limits. True if particle is in limits.
        """
        pass

    @abstractmethod
    def __prep_file_handle__(self):
        """Command which prepares the file handle for the extractor class"""

    @abstractmethod
    def __prep_time_vector__(self):
        """Command which prepares the result time stamp vector relative to python epoch"""

    @abstractmethod
    def __prep_2d_geometry__(self):
        """Command which prepares the result 2D mesh geometry"""

    @abstractmethod
    def __prep_3d_geometry__(self):
        """Command which prepares the result 2D mesh geometry"""


class FvParticles(Particles):
    """
        Class that extracts particle data from a TUFLOW FV PTM netCDF4 result file.

        Parameters
        ----------
        file : string
            Model result file path.

        Attributes
        ----------
        nc : netCDF4.Dataset
            Dataset object
        nt : int
            Number of time steps
        np : int
            Number of particles
        """

    def __init__(self, file):
        super(FvParticles, self).__init__(file)

    @Expression.decorator
    def get_raw_data(self, variable, ii):
        if self.nc[variable].ndim > 1:
            return self.nc[variable][ii, :].data
        else:
            return self.nc[variable][:].data

    def get_mask_vector(self, ii):
        return self.get_raw_data('stat', ii) < 0

    def get_vertical_selection(self, ii, datum, limits):
        # Get raw data
        pz = self.get_raw_data('z', ii)
        pd = self.get_raw_data('depth', ii)
        wd = self.get_raw_data('water_depth', ii)

        # Get the mask based on inactive particles
        mask = self.get_mask_vector(ii)

        # Get water level (wl) and bed level (bl) for each particle
        wl = np.ma.masked_array(pz + pd, mask=mask, fill_value=-999)
        bl = np.ma.masked_array(wl - wd, mask=mask, fill_value=-999)

        # Convert the limits into elevation
        if datum == 'sigma':
            z1 = limits[0] * (wl - bl) + bl
            z2 = limits[1] * (wl - bl) + bl
        elif datum == 'height':
            z1 = limits[0] + bl
            z2 = limits[1] + bl
        elif datum == 'depth':
            z1 = wl - limits[1]
            z2 = wl - limits[0]
        elif datum == 'elevation':
            z1 = limits[0]
            z2 = limits[1]
        else:
            return None

        # Return logical index of cells in limits
        return (z1.filled() <= pz) & (pz <= z2.filled())

    def __prep_file_handle__(self):
        # Store netCDF4 Dataset handle
        self.nc = Dataset(self.file, 'r')

    def __prep_time_vector__(self):
        # Define fv epoch relative to python epoch
        fv_epoch = dt.datetime(1990, 1, 1)
        fv_epoch = get_date_num(fv_epoch)

        # Prepare time vector relative to python epoch
        fv_time_vector = self.nc['Time'][:].data
        py_time_vector = fv_time_vector*3600 + fv_epoch

        # Store data as attributes
        self.time_vector = py_time_vector
        self.nt = self.time_vector.size

    def __prep_2d_geometry__(self):
        self.np = self.nc['groupID'].size

    def __prep_3d_geometry__(self):
        pass

    # Inherit doc strings (needs to be done a better way with decorator as per matplotlib)
    get_raw_data.__doc__ = Particles.get_raw_data.__doc__
    get_mask_vector.__doc__ = Particles.get_mask_vector.__doc__
    get_vertical_selection.__doc__ = Particles.get_vertical_selection.__doc__

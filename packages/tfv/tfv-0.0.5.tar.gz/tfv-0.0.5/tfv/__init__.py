import pkg_resources

__version__ = "0.0.5"
__author__ = "toby.devlin@bmtglobal.com, jonah.chorley@bmtglobal.com"
__aus_date__ = "%d/%m/%Y %H:%M:%S"

# List of dependencies copied from requirements.txt
dependencies = \
    [
        'matplotlib>=3.1.1',
        'netCDF4>=1.5.1.2',
        'numpy>=1.17.0',
        'PyQt5>=5.13.0',
    ]

# Throw exception if correct dependencies are not met
pkg_resources.require(dependencies)

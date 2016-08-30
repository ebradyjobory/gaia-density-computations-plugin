#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
#  Copyright Kitware Inc. and Epidemico Inc.
#
#  Licensed under the Apache License, Version 2.0 ( the "License" );
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
##############################################################################
import gaia.formats as formats
import gdal
import os
import osr
import ogr
import numpy as np
import itertools
import geopandas
import sys

from gaia.inputs import GaiaIO
from gaia.gaia_process import GaiaProcess
from gaia_densitycomputations import config
from gaia.geo.geo_inputs import RasterFileIO
from skimage.graph import route_through_array
from scipy import stats
import matplotlib.pyplot as plt
from math import sqrt, ceil


def toGeoTif(uri, array, ncols, nrows, originX, originY, csx, csy):
    # Convert the results to geoTif raster
    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(
        uri, ncols, nrows, 1, gdal.GDT_Byte
    )
    # Set layer geo transform
    outRaster.SetGeoTransform((originX, csx, 0, originY, 0, -csy))
    outband = outRaster.GetRasterBand(1)
    # Add colors to the raster image
    outband.SetRasterColorInterpretation(gdal.GCI_PaletteIndex)
    ct = gdal.ColorTable()
    ct.CreateColorRamp(0, (0, 0, 255), 14, (0, 255, 0))
    ct.CreateColorRamp(15, (0, 255, 0), 30, (127, 127, 0))
    ct.CreateColorRamp(30, (127, 127, 0), 50, (255, 0, 0))
    outband.SetColorTable(ct)
    outband.SetNoDataValue(0)
    outband.FlushCache()

    # Write the layer
    outband.WriteArray(array)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG(4326)
    # Set layer projection
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()
    outband = None

class DensityComputationsProcess(GaiaProcess):
    """
        Density Computations.
    """
    default_output = formats.RASTER

    def __init__(self, resolution, **kwargs):
        super(DensityComputationsProcess, self).__init__(**kwargs)

        self.resolution = resolution

        if not self.output:
            self.output = RasterFileIO(name='result', uri=self.get_outpath())
            self.uri = self.inputs[0]['uri']

    def calculateDensity(self):

        shpDriver = ogr.GetDriverByName('GeoJSON')

        dataSource = shpDriver.Open(self.uri, 0)

        # Open the source file, and exit if doesn't exist
        if dataSource is None:
            print 'Could not open file ' + self.uri
            sys.exit(1)

        if os.path.exists(self.output.uri):
            shpDriver.DeleteDataSource(self.output.uri)
        else:
            self.output.create_output_dir(self.output.uri)

        # Get the layer
        layer = dataSource.GetLayer()
        # Get the layer extent
        extent = layer.GetExtent()

        # Open the layer
        # Set the bounding box
        xmin = extent[0]
        ymin = extent[2]
        xmax = extent[1]
        ymax = extent[3]

        # Number of columns and rows
        nbrColumns = self.resolution['nCol']
        nbrRows = self.resolution['nRow']

        # Caculate the cell size in x and y direction
        csx = (xmax - xmin) / nbrColumns
        csy = (ymax - ymin) / nbrRows

        rows = []
        i = ymax
        while i > ymin:
            j = xmin
            cols = []
            while j < xmax:
                # Set a spatial filter
                layer.SetSpatialFilterRect(j, (i-csy), (j+csx), i)
                # And count the features
                cols.append(layer.GetFeatureCount())
                j += csx
            rows.append(cols)
            i -= csy

        array = np.array(rows)
        ncols = array.shape[1]
        nrows = array.shape[0]

        originX = extent[0]
        originY = extent[3]

        toGeoTif(self.output.uri, array, ncols, nrows, originX, originY, csx, csy)

    def compute(self):
        self.calculateDensity()



class kernelDensityEstimateProcess(GaiaProcess):
    """
       kernel Density Estimate
    """
    default_output = formats.RASTER

    def __init__(self, resolution, **kwargs):
        super(kernelDensityEstimateProcess, self).__init__(**kwargs)

        self.resolution = resolution

        if not self.output:
            self.output = RasterFileIO(name='result', uri=self.get_outpath())
            self.uri = self.inputs[0]['uri']

    def calculateKernelDensityEstimate(self):

        shpDriver = ogr.GetDriverByName('GeoJSON')

        dataSource = shpDriver.Open(self.uri, 0)

        # Open the source file, and exit if doesn't exist
        if dataSource is None:
            print 'Could not open file ' + self.uri
            sys.exit(1)

        if os.path.exists(self.output.uri):
            shpDriver.DeleteDataSource(self.output.uri)
        else:
            self.output.create_output_dir(self.output.uri)

        # Get the layer
        layer = dataSource.GetLayer()
        # Get the layer extent
        extent = layer.GetExtent()

        # Set the bounding box
        xmin = extent[0]
        ymin = extent[2]
        xmax = extent[1]
        ymax = extent[3]

        # Number of columns and rows
        nbrColumns = self.resolution['nCol']
        nbrRows = self.resolution['nRow']

        # Caculate the cell size in x and y direction
        csx = (xmax - xmin) / nbrColumns
        csy = (ymax - ymin) / nbrRows

        rows = []
        i = ymax
        while i > ymin:
            j = xmin
            cols = []
            while j < xmax:
                # Set a spatial filter
                layer.SetSpatialFilterRect(j, (i-csy), (j+csx), i)
                # And count the features
                cols.append(layer.GetFeatureCount())
                j += csx
            rows.append(cols)
            i -= csy

        array = np.array(rows)
        m1, m2 = array[0], array[1]

        X, Y = np.mgrid[xmin:xmax:500j, ymin:ymax:500j]
        positions = np.vstack([X.ravel(), Y.ravel()])
        values = np.vstack([m1, m2])
        kernel = stats.gaussian_kde(values)
        Z = np.reshape(kernel(positions).T, X.shape)

        ncols = Z.shape[1]
        nrows = Z.shape[0]

        originX = extent[0]
        originY = extent[3]

        toGeoTif(self.output.uri, array, ncols, nrows, originX, originY, csx, csy)

    def compute(self):
        self.calculateKernelDensityEstimate()


PLUGIN_CLASS_EXPORTS = [
    DensityComputationsProcess,
    kernelDensityEstimateProcess
]

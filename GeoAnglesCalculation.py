import numpy as np
from osgeo import gdal
import rasterio as rio
import tkinter
from tkinter.filedialog import askopenfilename

'''
Created on 23 December 2020 by Oanh Thi La
Purposes: 
1. Calculate cosine of Relative Azimuth Angle (RAA) for each pixel in the image scene from Sun-Azimuth Angle and Sensor Azimuth Angle
2. calculate cosine of Sun zenith angle (SZA) and Sensor zenith angle (VZA)
'''
'''1. COSINE OF RAA'''
# Read sun azimuth angle (SAA) and sensor azimuth angle (VAA)

Root = tkinter.Tk() # Create a Tkinter.Tk() instance
Root.withdraw() # Hide the Tkinter.Tk() instance
SAA_path = askopenfilename(title=u'Open SAA file', filetypes=[("TIF", ".tif")]) #choose your SAA angle
VAA_path = askopenfilename(title=u'Open VAA file', filetypes=[("TIF", ".tif")]) # choose your VAA angle
## read raster image as array
SAA = gdal.Open(SAA_path).ReadAsArray()
VAA = gdal.Open(VAA_path).ReadAsArray()
sun_azi_angle = SAA/100
sen_azi_angle = VAA/100

## CALCULATE RELATIVE AZIMUTH ANGLE FROM SUN AZIMUTH AND SENSOR AZIMUTH ANGLE
def relative_azimuth_angle(sun_azi_angle, sen_azi_angle):
    difference_value = abs(sun_azi_angle - sen_azi_angle) #abs(Sensor Azimuth - 180.0 - Solar azimuth)
    dif_row = difference_value.shape[0]
    dif_col = difference_value.shape[1]
    rel_azi_angle = np.zeros([dif_row, dif_col])
    for i in range(dif_row):
        for j in range(dif_col):
            if difference_value[i, j] > 180.0:
                rel_azi_angle[i, j] = 360.0 - difference_value[i, j]
            elif difference_value[i, j] == 0:
                rel_azi_angle[i, j] = 0.0
            else:
                rel_azi_angle[i, j] = 180.0 - difference_value[i, j]
    return rel_azi_angle, difference_value

[rel_azi_angle, difference_value] = relative_azimuth_angle(sun_azi_angle, sen_azi_angle)

#calculating cosine of RAA angle
rel_azi_angle[rel_azi_angle==0] = np.nan # convert 0 value to nan to avoid calculate cosine for pixel have 0 value
cos_RAA = np.cos(rel_azi_angle)
cos_RAA[np.isnan(cos_RAA)] = 0 # convert nan back to 0 value
cos_RAA = np.float32(cos_RAA) # convert float64 to float32
# save cos_RAA to TIF file
with rio.open(SAA_path) as src: # choose one image
    ras_data = src.read()
    ras_meta = src.profile

ras_meta['dtype'] = "float32"
ras_meta['No Data'] = 0.0

Fname1 = tkinter.filedialog.asksaveasfilename(title=u'Save RAA file', filetypes=[("TIF", ".tif")])
with rio.open(Fname1, 'w', **ras_meta) as dst: # write image with the same shape with the selected image aboved
    dst.write(cos_RAA, 1)




'''2. COSINE OF SZA and VZA'''

Root = tkinter.Tk() # Create a Tkinter.Tk() instance
Root.withdraw() # Hide the Tkinter.Tk() instance
SZA_path = askopenfilename(title=u'Open SZA file', filetypes=[("TIF", ".tif")]) #choose your SZA angle
VZA_path = askopenfilename(title=u'Open VZA file', filetypes=[("TIF", ".tif")]) # choose your VZA angle
## read raster image as array
SZA = gdal.Open(SZA_path).ReadAsArray()
VZA = gdal.Open(VZA_path).ReadAsArray()
sun_ze_angle = SZA/100
sen_ze_angle = VZA/100

sun_ze_angle[sun_ze_angle==0] = np.nan # convert 0 value to nan to avoid calculate cosine for pixel have 0 value
cos_SZA = np.cos(sun_ze_angle)
cos_SZA[np.isnan(cos_SZA)] = 0 # convert nan back to 0 value
cos_SZA = np.float32(cos_SZA) # convert float64 to float32

sen_ze_angle[sen_ze_angle==0] = np.nan # convert 0 value to nan to avoid calculate cosine for pixel have 0 value
cos_VZA = np.cos(sen_ze_angle)
cos_VZA[np.isnan(cos_VZA)] = 0 # convert nan back to 0 value
cos_VZA = np.float32(cos_VZA) # convert float64 to float32

# save cos_SZA to TIF file
with rio.open(SZA_path) as src: # choose one image
    ras_data = src.read()
    ras_meta = src.profile

ras_meta['dtype'] = "float32"
ras_meta['No Data'] = 0.0

Fname2 = tkinter.filedialog.asksaveasfilename(title=u'Save SZA file', filetypes=[("TIF", ".tif")])
with rio.open(Fname2, 'w', **ras_meta) as dst: # write image with the same shape with the selected image aboved
    dst.write(cos_SZA, 1)

# save cos_VZA to TIF file
with rio.open(VZA_path) as src:  # choose one image
    ras_data = src.read()
    ras_meta = src.profile

ras_meta['dtype'] = "float32"
ras_meta['No Data'] = 0.0

Fname3 = tkinter.filedialog.asksaveasfilename(title=u'Save VZA file', filetypes=[("TIF", ".tif")])
with rio.open(Fname3, 'w', **ras_meta) as dst:  # write image with the same shape with the selected image aboved
    dst.write(cos_VZA, 1)

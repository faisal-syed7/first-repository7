import arcpy

#assign bands
source = r"C:\first-repository7\Lab7"
band1 =arcpy.sa.Raster(source + r"\band1.tif.TIF")
band2 =arcpy.sa.Raster(source + r"\band2.tif.TIF")
band3 =arcpy.sa.Raster(source + r"\band3.tif.TIF")
band4 =arcpy.sa.Raster(source + r"\band4.tif.TIF")
combined = arcpy.CompositeBands_management([band1, band2, band3, band4], source + r"\combined_output.tif")

#hillshade
azimuth = 315
altitude = 45
shadows = 'NO_SHADOWS'
x_factor = 1 
arcpy.ddd.HillShade(source + r"\DEM.tif.tif", source + r"\hillshade_output.tif", azimuth, altitude, shadows, x_factor)

#slope
output_measurement = "DEGREE"
z_factor = 1 
arcpy.ddd.Slope(source + r"\DEM.tif.tif", source + r"\slope_output.tif", output_measurement, z_factor)
print ("success!")


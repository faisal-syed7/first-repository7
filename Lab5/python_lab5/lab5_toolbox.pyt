# -*- coding: utf-8 -*-

import arcpy

class Toolbox(object):
    def __init__(self):
        self.label = "Toolbox"
        self.alias = ""

        self.tools = [tool]

class tool(object):
    def __init__(self):
        self.label = "Building Proximity"
        self.description = "Determines which buildings on TAMU's campus are near a targeted building"
        self.canRuninBackground = False
        self.category = "Building Tools"

    def getParameterInfo(self):
        param0 = arcpy.Parameter(
            displayName= "GDB Folder",
            name="GDBFolder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )
        param1 = arcpy.Parameter(
            displayName ="GDB Name",
            name="GDBName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param2= arcpy.Parameter(
            displayName="Garage CSV File",
            name="GarageCSVFile",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
        param3 = arcpy.Parameter(
            displayName="Garage Layer Name",
            name="GarageLayerName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param4 = arcpy.Parameter(
            displayName="Campus GDB",
            name="Campus GDB",
            datatype="DEType",
            parameterType="Required",
            direction="Input"
        )
        param5 = arcpy.Parameter(
            displayName="Buffer Distance",
            name="BufferDistance",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input"
        )
        params = [param0, param1, param2, param3, param4, param5]
        return params
    
    def isLicensed(self):
        return True
    
    def updateParameters(self, parameters):
        return
    
    def updateMessages(self, parameters):
        return
    
    def execute(self, parameters, messages):
        folder_path = r'C:\first-repository7\Lab5'
        gdb_name = 'Test.gdb'
        gdb_path = folder_path + '\\' + gdb_name
        arcpy.CreateFileGDB_management(folder_path, gdb_name)

        csv_path = r'C:\first-repository7\Lab5\codes_env\garages.csv'
        garage_layer_name = 'Garage_Points'
        garages = arcpy.MakeXYEventLayer_management(csv_path, 'X', 'Y', garage_layer_name)

        input_layer = garages
        arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)
        garage_points = gdb_path + '\\' + garage_layer_name 

        campus = r'C:\first-repository7\Lab5\codes_env\Campus.gdb'
        buildings_campus = campus + '\Structures'
        buildings = gdb_path + '\\' + 'Buildings'

        arcpy.Copy_management(buildings_campus, buildings)

        spatial_ref = arcpy.Describe(buildings).spatialReference
        arcpy.Project_management(garage_points, gdb_path + '\Garage_Points_reprojected', spatial_ref)

        buffer_distance = int(parameters[5].value)
        garageBuffered = arcpy.Buffer_analysis(gdb_path + '\Garage_Points_reprojected', gdb_path + '\Garage_Points_buffered', 150)

        arcpy.Intersect_analysis([garageBuffered, buildings], gdb_path + '\Garage_Buildings_Intersection', 'ALL')

        arcpy.TableToTable_conversion(gdb_path + '\Garage_Buildings_Intersection.dbf', r'C:\first-repository7\Lab5', 'nearbyBuildings')

        return None 
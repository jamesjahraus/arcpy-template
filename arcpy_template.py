r"""ArcGIS Pro setup to automate the execution of geoprocessing tools.

Author: https://github.com/jamesjahraus

ArcGIS Pro Python reference:
https://pro.arcgis.com/en/pro-app/latest/arcpy/main/arcgis-pro-arcpy-reference.htm
"""

import os
import sys
import time
import arcpy


def pwd():
    r"""Prints the working directory.
    Used to determine the directory this module is in.

    Returns:
        The path of the directory this module is in.
    """
    wd = sys.path[0]
    arcpy.AddMessage('wd: {0}'.format(wd))
    return wd


def set_path(wd, data_path):
    r"""Joins a path to the working directory.

    Arguments:
        wd: The path of the directory this module is in.
        data_path: The suffix path to join to wd.
    Returns:
        The joined path.
    """
    path_name = os.path.join(wd, data_path)
    arcpy.AddMessage('path_name: {0}'.format(path_name))
    return path_name


def import_spatial_reference(dataset):
    r"""Extracts the spatial reference from input dataset.

    Arguments:
        dataset: Dataset with desired spatial reference.
    Returns:
        The spatial reference of any dataset input.
    """
    spatial_reference = arcpy.Describe(dataset).spatialReference
    arcpy.AddMessage('spatial_reference: {0}'.format(spatial_reference.name))
    return spatial_reference


def setup_env(workspace_path, spatial_ref_dataset):
    # Set workspace path.
    arcpy.env.workspace = workspace_path
    arcpy.AddMessage('workspace(s): {}'.format(arcpy.env.workspace))

    # Set output overwrite option.
    arcpy.env.overwriteOutput = True
    arcpy.AddMessage('overwriteOutput: {}'.format(arcpy.env.overwriteOutput))

    # Set the output spatial reference.
    arcpy.env.outputCoordinateSystem = import_spatial_reference(
        spatial_ref_dataset)
    arcpy.AddMessage('outputCoordinateSystem: {}'.format(
        arcpy.env.outputCoordinateSystem.name))


def check_status(result):
    r"""Logs the status of executing geoprocessing tools.

    Requires futher investigation to refactor this function:
        I can not find geoprocessing tool name in the result object.
        If the tool name can not be found may need to pass it in.
        Return result.getMessages() needs more thought on what it does.

    Understanding message types and severity:
    https://pro.arcgis.com/en/pro-app/arcpy/geoprocessing_and_python/message-types-and-severity.htm

    Arguments:
        result: An executing geoprocessing tool object.
    Returns:
        Requires futher investigation on what result.getMessages() means on return.
    """
    status_code = dict([(0, 'New'), (1, 'Submitted'), (2, 'Waiting'),
                        (3, 'Executing'), (4, 'Succeeded'), (5, 'Failed'),
                        (6, 'Timed Out'), (7, 'Canceling'), (8, 'Canceled'),
                        (9, 'Deleting'), (10, 'Deleted')])

    arcpy.AddMessage('current job status: {0}-{1}'.format(
        result.status, status_code[result.status]))
    # Wait until the tool completes
    while result.status < 4:
        arcpy.AddMessage('current job status (in while loop): {0}-{1}'.format(
            result.status, status_code[result.status]))
        time.sleep(0.2)
    messages = result.getMessages()
    arcpy.AddMessage('job messages: {0}'.format(messages))
    return messages


def function_template():
    r"""Function summary.
    Description sentence(s).
    Arguments:
        arg 1: Description sentence.
        arg 2: Description sentence.
    Returns:
        Description sentence.
    Raises:
        Description sentence.
    """
    pass


def main():
    r"""Example using data from Boulder County Geospatial Open Data.
    https://opendata-bouldercounty.hub.arcgis.com/datasets/boulder-area-trailheads?geometry=-136.557%2C6.748%2C30.699%2C35.099

    * In GitHub <Use this template>.
    * Clone as ArcGIS Pro project base folder.
    * Run ArcGIS Pro and create new project in base folder.
    * Copy data to project db.
    * Program and run arcpy module from this template.
    """
    # Setup Geoprocessing Environment
    spatial_ref_dataset = 'BoulderAreaTrailheads'
    wd = pwd()
    # Optional: use input_db and output_db.
    # input_db = set_path(wd, 'Project.gdb')
    # output_db = set_path(wd, 'Project_output.gdb')
    db = set_path(wd, 'arcpytemplate.gdb')
    setup_env(db, spatial_ref_dataset)

    # Geoprocessing Tools Example
    # https://pro.arcgis.com/en/pro-app/latest/tool-reference/analysis/buffer.htm
    buffer_trails = arcpy.Buffer_analysis('BoulderAreaTrailheads', 'Trailheads_Buff', '100 Meters', 'FULL', 'ROUND',
                                          'ALL')
    check_status(buffer_trails)


if __name__ == '__main__':
    main()

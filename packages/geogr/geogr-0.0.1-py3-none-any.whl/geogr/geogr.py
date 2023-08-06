import requests
import re
import pandas as pd
from urllib import parse
from shapely import geometry
import json
import topojson
import geopandas as gpd

def geocode(address):

    coords = {}

    address = [item.replace(', Grand Rapids, MI', '')
               .replace('/', '%26')
               for item in address]

    address = [re.sub(r'\(.*\)', '', item) for item in address]
    address = [re.sub(r'\s+', ' ', item) for item in address]

    geocode = address.unique()

    for item in address:
        print(address.index(item))
        latlon = requests.get(str(
            'https://maps.grcity.us/arcgis/rest/services/Geocode/Transport_StreetCenterlines/GeocodeServer/findAddressCandidates?Street=' + \
            parse.quote(item.upper()) + \
            '&outSR=4326&f=pjson'))
        latlon = latlon.json()
        if 'candidates' in latlon and len(latlon['candidates']) > 0:
            coords[item] = geometry.Point(latlon['candidates'][0]['location']['x'],
                                          latlon['candidates'][0]['location']['y'])

    return coords


def label_points_polygon(polygons, points, label):
    # Label 311 Data with ACS Boundary IDs
    labels = {}

    if isinstance(polygons, pd.core.series.Series) and isinstance(points, pd.core.series.Series) and isinstance(label, pd.core.series.Series):
        for index, point in points.iterrows():
            for number, polygon in polygons.iterrows():
                if pd.notna(polygon['geometry']) and pd.notna(point['geometry']):
                    if polygon['geometry'].contains(point['geometry']):
                        labels[index] = polygon[label]

    return labels

def get_precincts(file):

    precincts = gpd.read_file(file)

    return precincts


def combine_precincts(precincts, column, labels, path):

    # Read Precincts Dataframe
    combined = gpd.GeoDataFrame(precincts)

    # Re-label Combined Precincts
    combined[column] = combined[column].replace(labels)

    # Aggregate Polygons of Combined Precincts
    combined = precincts.dissolve(by=column)

    # Add Precincts Column back to Data
    combined[column] = combined.index

    if path is not None:
        with open(path, 'w') as file:
            file.write(topojson.Topology(combined, topology=True).to_json())
    else:
        return(combined)


def convert_shapefile(shapefile,label,path=None, export='topojson'):

    # READ SHAPEFILE
    shapefile = gpd.read_file(shapefile, driver='shapefile')

    # DROP ALL COLUMNS BUT LABEL AND GEOMETRY
    shapefile = shapefile[[label,
                           'geometry']]

    # PROJECT TO WGS84
    shapefile = shapefile.to_crs(epsg=4326)

    # SAVE JSON OR RETURN GEODATAFRAME
    if path is not None and export == 'topojson':
        with open(path, 'w') as file:
            file.write(topojson.Topology(shapefile, topology=True).to_json())
    elif path is not None and export == 'geojson':
        shapefile.to_file(path, driver='GeoJSON')
    else:
        return shapefile


def format_addresses(address):

    formatted = dict()

    if isinstance(address, list) and len(address) > 1:
        for item in address:
            if item is None:
                address.pop(address.index(item))

        for item in address:
            x = re.match('^\d*(\s*\w+){1,5}', item)
            if x is not None:
                formatted[item] = x.group()

    elif isinstance(address, pd.core.series.Series) and len(list(address)) > 1:
        address = list(address.unique())
        for item in address:
            if item is None:
                address.pop(address.index(item))

        for item in address:
            x = re.match('^\d*(\s*\w+){1,5}', item)
            if x is not None:
                formatted[item] = x.group()

    else:
        x = re.match('^\d*(\s*\w+){1,5}', address)
        formatted[address] = x.group()

        return formatted
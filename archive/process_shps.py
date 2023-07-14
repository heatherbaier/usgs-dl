import geopandas as gpd
import argparse
import pygee
import os

# from utils import *




if __name__ == "__main__":
    
        
    parser = argparse.ArgumentParser()
    parser.add_argument('shp_dir', type = str)
    parser.add_argument('ISO', type = str)
    args = parser.parse_args()
    
    shp_dir = args.shp_dir

    shp_path = os.path.join(shp_dir, args.ISO, [i for i in os.listdir(os.path.join(shp_dir, args.ISO)) if i.endswith(".shp")][0])
    
    print(shp_path)

    shp = gpd.read_file(shp_path)
    shp = shp.dropna(subset = ['geometry'])
    shp = shp.to_crs("EPSG:6362")
    shp = pygee.remove_islands(shp, "GEOLEVEL2")
    shp = shp.to_crs("EPSG:4326")
    gdf = pygee.convert_to_bbox(shp)
    gdf = gdf.rename(columns = {"GEOLEVEL2": "shapeID"})
    
    print(gdf.head())
    
    gdf.to_file(os.path.join(shp_dir, args.ISO, args.ISO + "_processed.shp"))




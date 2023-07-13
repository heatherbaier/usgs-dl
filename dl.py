from landsatxplore.earthexplorer import EarthExplorer
from shapely.geometry import Polygon
from landsatxplore.api import API
from rasterio.merge import merge
from rasterio.plot import show
import rioxarray as riox
from pathlib import Path
import geopandas as gpd
import rasterio as rio
import pandas as pd
import argparse
import tarfile
import shapely
# import pygee
import os

from utils import *



# import geopandas as gpd
import calendar
# import pygee
import os

# from utils import *


def chunker_list(seq, size):
    return (seq[i::size] for i in range(size))



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('ISO', type = str)
    parser.add_argument('year', type = int)
    args = parser.parse_args()
    
    for year in range(args.year - 5, args.year):
        
        for month in range(1, 13):
            
            all_dates = [str(year), str(month)]
            
            print(all_dates)
    
            base_dir = f"/rapids/notebooks/sciclone/geograd/Heather/clean_dl/imagery/{args.ISO}"

            dates = GetDays(all_dates[0], all_dates[1])

            download_dir = f"{base_dir}/{all_dates[0]}/{all_dates[1]}/zips"
            unzip_dir = f"{base_dir}/{all_dates[0]}/{all_dates[1]}/unzips"
            mosaic_dir = f"{base_dir}/{all_dates[0]}/{all_dates[1]}/mosaics"    
            year_dir = f"{base_dir}/{all_dates[0]}"  
            month_dir = f"{base_dir}/{all_dates[0]}/{all_dates[1]}"    

            print(all_dates, download_dir, unzip_dir, mosaic_dir, "\n")
            
            if not os.path.exists(year_dir):
                os.mkdir(year_dir)

            if not os.path.exists(month_dir):
                os.mkdir(month_dir)
            
            if not os.path.exists(download_dir):
                os.mkdir(download_dir)

            if not os.path.exists(unzip_dir):
                os.mkdir(unzip_dir)

            if not os.path.exists(mosaic_dir):
                os.mkdir(mosaic_dir)

            shp = gpd.read_file("/rapids/notebooks/sciclone/geograd/Heather/clean_dl/shps/NPL/geo2_np2001_2011.shp")
            shp["centroid"] = shp.geometry.centroid
            shp["bbox"] = shp["geometry"].apply(lambda x: calc_bbox(x))
            shp.head()

            # Your USGS  credentials
            username = "hmbaier"
            password = "930941741Hb."

            ee = EarthExplorer(username, password)

            # Initialize a new API instance
            api = API(username, password)

            # Perform a request
            response = api.request(endpoint="dataset-catalogs")
            print(response)

            scenes = search_for_imagery(api, shp, ["landsat_tm_c2_l1"], dates[0], dates[1])
            print(scenes.head())

            scenes.to_csv(f"{args.ISO}_{all_dates[0]}_{all_dates[1]}_scenes.csv", index = False)

            download_imagery(ee, scenes, download_dir)

            untar_imagery(download_dir, unzip_dir)

            mosaic_imagery(scenes, mosaic_dir, unzip_dir, shp, all_dates)         
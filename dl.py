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
import calendar
import tarfile
import shapely
import os

from utils import *


def chunker_list(seq, size):
    return (seq[i::size] for i in range(size))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('ISO', type = str)
    parser.add_argument('year', type = int)
    args = parser.parse_args()
    
    # Your USGS  credentials
    username = "hmbaier"
    password = "930941741Hb."

    ee = EarthExplorer(username, password)

    # Initialize a new API instance
    api = API(username, password)

    # Perform a request
    response = api.request(endpoint="dataset-catalogs")


    for year in range(args.year - 5, args.year):
        
        for month in range(1, 13):
            
            all_dates = [str(year), str(month)]
            
            print(all_dates)
    
            base_dir = f"/sciclone/geounder/hmbaier/usgs/imagery/{args.ISO}"

            dates = GetDays(all_dates[0], all_dates[1])

            download_dir = f"{base_dir}/{all_dates[0]}/{all_dates[1]}/zips"
            unzip_dir = f"{base_dir}/{all_dates[0]}/{all_dates[1]}/unzips"
            mosaic_dir = f"{base_dir}/{all_dates[0]}/{all_dates[1]}/mosaics"    
            year_dir = f"{base_dir}/{all_dates[0]}"  
            month_dir = f"{base_dir}/{all_dates[0]}/{all_dates[1]}"    

            print(all_dates, download_dir, unzip_dir, mosaic_dir, "\n")
            
            if not os.path.exists(base_dir):
                os.mkdir(base_dir)

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

            shp = gpd.read_file("/sciclone/geounder/hmbaier/usgs/shps/MWI/geo2_mw1998_2008.shp")
            shp["centroid"] = shp.geometry.centroid
            shp["bbox"] = shp["geometry"].apply(lambda x: calc_bbox(x))
            shp.head()

            log_path = f"logs/log_{args.ISO}_{all_dates[0]}_{all_dates[1]}.txt"

            with open(log_path, "a") as f:
                f.write(str(response) + "\n")

            # print(response)

            scenes = search_for_imagery(api, shp, ["landsat_tm_c2_l1"], dates[0], dates[1], log_path)
            # print(scenes.head())

            if scenes is None:

                with open(log_path, "a") as f:
                    f.write(f"NO IMAGERY FOR {all_dates[0]} {all_dates[1]} \n")

                continue

            with open(log_path, "a") as f:
                f.write(str(scenes.head()) + "\n")            

            scenes.to_csv(f"scenes/{args.ISO}_{all_dates[0]}_{all_dates[1]}_scenes.csv", index = False)

            download_imagery(ee, scenes, download_dir, log_path)

            untar_imagery(download_dir, unzip_dir, log_path)

            mosaic_imagery(scenes, mosaic_dir, unzip_dir, shp, all_dates)         
import geopandas as gpd
import pandas as pd
import argparse
import pygee
import ast
import os

# from utils import *


import ee

# ee.Authenticate()

ee.Initialize()


if __name__ == "__main__":
    
        
    parser = argparse.ArgumentParser()
    parser.add_argument('shp_dir', type = str)
    parser.add_argument('im_dir', type = str)
    parser.add_argument('ISO', type = str)
    parser.add_argument('year', type = int)
    args = parser.parse_args()
    
    landsat_info = pd.read_csv("./landsat_info.csv")
    shp = gpd.read_file(os.path.join(args.shp_dir, args.ISO, args.ISO + "_processed.shp"))
    print(landsat_info)
    
    start_year = args.year
    end_year = args.year - 5
    
    if start_year < 2013:
        landsat = 8
    else:
        landsat = 5
        
    ics = landsat_info[landsat_info["landsat"] == landsat]["ic"].to_list()
    rgb_bands = landsat_info[landsat_info["landsat"] == landsat]["rgb_bands"].to_list()
    ic_rgb = dict(zip(ics, rgb_bands))
    
    
    all_dates = [str(2001), str(1)]
    RANK_DIREC = os.path.join(args.im_dir, args.ISO, all_dates[0], all_dates[1])    
    
    iso_direc = os.path.join(args.im_dir, args.ISO)
    if not os.path.isdir(iso_direc):
        os.mkdir(iso_direc)      
        
    year_direc = os.path.join(args.im_dir, args.ISO, all_dates[0])
    if not os.path.isdir(year_direc):
        os.mkdir(year_direc)      
                
    month_direc = os.path.join(args.im_dir, args.ISO, all_dates[0], all_dates[1])
    if not os.path.isdir(month_direc):
        os.mkdir(month_direc)                
            
                
    for col, row in shp.iterrows():
        
        for IC, BANDS in ic_rgb.items():
            
            main_direc = os.path.join(RANK_DIREC, str(row.shapeID))
            
            print(main_direc)
            
            dates = pygee.GetDays(all_dates[0], all_dates[1])
            
            print(row.shapeID, IC, ast.literal_eval(BANDS), dates)
            

            
            pygee.download_imagery(geom = row.geometry,
                                shapeID = row.shapeID,
                                ic = IC, 
                                dates = dates, 
                                imagery_dir = RANK_DIREC, 
                                bands = BANDS)            
            
            
            
            # if an image has been downloaded, stop searching
            if len(os.listdir(main_direc)) == 1:
                
                print("Imagery downloaded so done!")
                
                break
                
                
                
                
            
#             print()
            
            
#             break
    
#         break
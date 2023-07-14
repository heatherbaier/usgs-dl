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
import calendar    
import tarfile
import shapely
import os


def calc_bbox(x):
    return shapely.geometry.box(*x.bounds, ccw=True)


def search_for_imagery(api, shp, ics, date1, date2, log_path):
    
    all_scenes = []

    for col, row in shp.iterrows():

        df_scenes = None

        try:

            for ic in ics:#, "landsat_tm_c2_l2"]:

                lng = row.centroid.x
                lat = row.centroid.y
                
#                 lng = row.geometry.centroid.x
#                 lat = row.geometry.centroid.y                

                scenes = api.search(
                    dataset = ic,
                    latitude = lat,
                    longitude = lng,
                    start_date = date1,
                    end_date = date2,
                    max_cloud_cover = 100
                )

                # Create a DataFrame from the scenes
                df_scenes = pd.DataFrame(scenes)
                df_scenes = df_scenes[['display_id','wrs_path', 'wrs_row','satellite','cloud_cover','acquisition_date']]
                df_scenes.sort_values('acquisition_date', ascending=False, inplace=True)
                df_scenes["shapeID"] = row.GEOLEVEL2
                df_scenes["ic"] = ic

                all_scenes.append(df_scenes)

        except:

            with open(log_path, "a") as f:
                f.write(row.GEOLEVEL2 + " has no imagery. \n")   

            # print(row.GEOLEVEL2, " has no imagery.")

    if len(all_scenes) != 0:
        all_scenes = pd.concat(all_scenes)
        return all_scenes

    else:
        return None


# scenes = search_for_imagery(api, shp, ["landsat_tm_c2_l1"])


def download_imagery(ee, all_scenes, output_dir, log_path):
    
    for display_id in all_scenes["display_id"].unique():

        try:

            ee.download(display_id, output_dir = output_dir)

            with open(log_path, "a") as f:
                f.write(str(display_id) + "\n")                  

            # print(display_id)

        except:

            pass
    
# download_imagery(scenes, "data2")


def untar_imagery(data_dir, output_dir, log_path):
    
    for file in os.listdir(data_dir):

        if ".ipynb" not in file:

            with open(log_path, "a") as f:
                f.write(str(file) + "\n")                  

            # print(file)
            
            try:

                tar = tarfile.open('{}/{}'.format(data_dir, file))
                tar.extractall('{}/{}'.format(output_dir, file.replace(".tar", "")))
                tar.close()
            
            except:
                
                pass
            
            
            
def mosaic_imagery(all_scenes, output_dir, unzip_dir, shp, all_dates, bands = ["B1", "B2", "B3"]):
    
    for shapeID in all_scenes["shapeID"].unique():
        
        try:

            cur = all_scenes[all_scenes["shapeID"] == shapeID]["display_id"].unique()
    #         print(cur)

            shapePath = os.path.join(output_dir, shapeID)

            raster_files = []

            if not os.path.exists(shapePath):
                os.mkdir(shapePath)

            for band in bands:

                raster_files = []

                for file in cur:

                    raster_files.append(f"{unzip_dir}/{file}/{file}_{band}.TIF")

    #             print(raster_files, "\n")

                raster_to_mosiac = []

                for p in raster_files:
                    raster = rio.open(p)
                    raster_to_mosiac.append(raster)    

                mosaic, output = merge(raster_to_mosiac)

                output_path = f"{shapePath}/{shapeID}_{band}.tiff"

                output_meta = raster.meta.copy()
                output_meta.update(
                    {"driver": "GTiff",
                        "height": mosaic.shape[1],
                        "width": mosaic.shape[2],
                        "transform": output,
                    }
                )

                with rio.open(output_path, "w", **output_meta) as m:
                    m.write(mosaic)

                # Read raster using rioxarray
                raster = riox.open_rasterio(output_path)
                raster = raster.rio.reproject(shp.crs)

                # Shapely Polygon  to clip raster
                geom = shp[shp["GEOLEVEL2"] == shapeID]["bbox"].squeeze()

                # Use shapely polygon in clip method of rioxarray object to clip raster
                clipped_raster = raster.rio.clip([geom])

                # Save clipped raster
                clipped_raster.rio.to_raster(f"{shapePath}/{shapeID}_{all_dates[0]}_{all_dates[1]}_{band}_clipped.tiff")   

                os.remove(output_path)
                
        except:
            
            pass
            

            
# mosaic_imagery(scenes, "saved2", "unzipped")         


def GetDays(year, month):
    
    if month != 'all':
        r = list(calendar.monthrange(int(year), int(month)))[1]
        sdate = "-".join([str(year), str(month), str(1)])
        edate = "-".join([str(year), str(month), str(r)])
        return [sdate, edate]
    else:
        sdate = str(year) + "-" + str(1) + "-" + str(1)
        edate = str(year) + "-" + str(12) + "-" + str(31)
        return [sdate, edate]
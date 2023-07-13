# USGS Landsat Imagery Download

## Instructions to set up code and data folders
### Getting the Code
1. Log into HPC using ```ssh <WM_USERNAME>@<CLUSTER>.sciclone.wm.edu``` replacing cluster within one of ```vortex``` or ```bora```
2. Once you log int, you'll be in ```/sciclone/home/<WM_USERNAME>/```. Make a new folder called ```usgs``` by running ```mkdir usgs``` and navigate into it using ```cd usgs```
3. Initialize git by running:
```
git init.
git remote add origin https://github.com/heatherbaier/usgs-dl.git
git pull origin master
```
4. You should now have the files from the master branch in your ```usgs``` folder.

### Setting up your shapefile folder
1. Now, navigate to the geounder folder by running ```cd /sciclone/geograd/geounder```
2. If you don't already have one, make a folder with your username by running ```mkdir <WM_USERNAME>```. This will be where you save all of the imagery and shapefiles to. 
3. Navigate into your folder by running ```cd <WM_USERNAME>```
4. Make a new folder called ```usgs``` for this project and navigate into it using ```cd usgs```
5. Set up your directory using the following commands:
```
mkdir shps
mkdir imagery
```
6. Navigate into shps using ```cd shps``` and make a folder for each of the countries you'll be working with by running:
```
mkdir BRA
mkdir ECU
mkdir MEX
mkdir MWI
mkdir PAN
mkdir SEN
mkdir SLV
```
7. In your browser, navigate to: https://international.ipums.org/international/gis_harmonized_2nd.shtml
8. For each country in *to_dl.csv*, download the shapefile in the 'GIS files' column by clicking on the link.
9. Open up a new terminal but **don't** login to the HPC. This terminal should just be setup to your local machine.
9. Using the new terminal **not** loged in to the HPC, upload each shapefile folder (with all of it's assocaited contents) into the correct country's *shp* folder. For example, for Malawi (MWI), this would look like:
```
scp -r /Users/heatherbaier/Downloads/geo2_mw1998_2008 hmbaier@vortex.sciclone.wm.edu:/sciclone/geounder/hmbaier/usgs/shps/MWI
```

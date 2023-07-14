# USGS Landsat Imagery Download

## Instructions to set up code and data folders
### Getting the Code
1. Log into HPC using ```ssh <WM_USERNAME>@<CLUSTER>.sciclone.wm.edu``` replacing <CLUSTER> within one of ```vortex``` or ```bora```
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

## Instructions to download imagery
1. The dl.py file is the main file used to control the imagery download. It takes two command line arguments:
    - ISO: the ISO3c for the country you are currelty working with (i.e. SLV for El Salvador)
    - The year the cesus was taken for that country. Get this from the to_dl.csv file. In this case of a country that appears twice like Ecuador, run the script first with ECU and 2001 as the arguments and then with ECU and 2010.
2. Replace the base_dir with the folder you set up on ```geounder```
3. Replace the shapefile path in the gpd.read_file() line
4. Replace the USGS username and password credentials wtih your own.
5. Replace the command liine arguments in the job script with the correct ISO and year and run using ```qsub job```
6. Check the status of your job using ```qsu```
7. The jobV file has the correct MPI path for Vortex and the jobB file has the correct MPI path for Bora.
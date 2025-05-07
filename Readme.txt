



1. We downloaded our catalog using obspy. Our catalog is organized using this format:
['YR','MO','DY','HR','MN', 'SC', 'N', 'Lat','Lon','Depth','Mag']

2. EqCat.py provides the function to load earthqauke catalog based on different formats e.g., Relocated, ANSS, USGS Hazard Model catalog etc. 

3. ETAS folder contains the code to create synthetic catalogs. I have automated the full process to create synthetic catalogs based on three different rate types. define_rates.py provide the definition of rates I used in the study. 

4. I have created synthetic catalog using code 1a/1b/1c and then prepared those synthetic as per NND format, as well as separated background events for further comparison in code 2a and 2b. 

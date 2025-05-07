We estimate background seismicity rate using Nearest Neighbor approach and compare the results with Reasenberg and Gamma Distribution Fit. We also create ETAS based stochatic catalogs to compare the rates against true values. 

We follow nearest neighbor approach by: Zaliapin, I., & Ben-Zion, Y. (2013). Earthquake clusters in southern california ii: Classification and relation to physical properties of the crust. Journal of Geophysical Research: Solid Earth, 118 , 2865-2877. doi: 10.1002/jgrb.50178. The nearest neighbor codes are available at: https://github.com/tgoebel/clustering-analysis. We modified the codes as per our dataset.

We follow the ETAS model developed by Mizrahi, L., Schmid, N., & Han, M. (2023). lmizrahi/etas: Etas with fit visualization (3.2). Zenodo. Retrieved from https://doi.org/10.5281/zenodo.7584575 doi:10.5281/zenodo.7584575. This code requires installation of etas as described in https://github.com/lmizrahi/etas. 

We fit Gamma distribution following: Hainzl, S., Scherbaum, F., & Beauval, C. (2006). Estimating background activity based on interevent-time distribution. Bulletin of the Seismological Society of America, 96 ,313-320. doi: 10.1785/0120050053

Folders:
1. code contains the code to run nearest neighbor analysis and then estimate the backgroud rate, finally compare rates with Gamma fit and reasenberg (if available).
2. ETAS contains the codes to create synthetic catalogs.
3. data contains the input catalogs files.
4. data_processed contains the processed files from NND and the declustered catalogs.
5. plots contains the figures. 

Basic procedure:

1. We downloaded our ANSS catalog using obspy. Our catalog is organized using this format:
['YR','MO','DY','HR','MN', 'SC', 'N', 'Lat','Lon','Depth','Mag']

2. EqCat.py provides the function to load earthqauke catalog based on different formats e.g., Relocated, ANSS, USGS Hazard Model catalog etc. 

3. ETAS folder contains the code to create synthetic catalogs. We have automated the full process to create synthetic catalogs based on three different rate types. define_rates.py provide the definition of rates we used in the study. 

4. We have created synthetic catalog using code 1a/1b/1c and then prepared those synthetic as per NND format, as well as separated background events for further comparison in code 2a and 2b. 

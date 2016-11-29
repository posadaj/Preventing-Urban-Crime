from data_cleaning import *
""" Clean the trees dataset. """

# Extract lon/lat
fname   = "PPR_StreetTrees.csv"
outname = "PPR_StreetTrees_ll.csv"
lon_idx, lat_idx = 0, 1
extract_lon_lat( fname, lat_idx, lon_idx, outname )
print("Completed extraction")


# Convert lon/lat to zip
fname  = "PPR_StreetTrees_ll.csv"
outname = "PPR_StreetTrees_zip.csv"
lon_lat_to_zip( fname, outname )
print("Completed conversion")

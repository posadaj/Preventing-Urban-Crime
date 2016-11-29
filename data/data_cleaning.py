"""" Script to clean locaitonal data. """

import sys, csv
import googlemaps

# Open endpoint
KEY = "AIzaSyDupWadt9tTVDrFp2nmtrmwBQ9cn7jMMwQ"
gmaps = googlemaps.Client(key=KEY)

# Philly zip codes from
# http://www.city-data.com/zipmaps/Philadelphia-Pennsylvania.html
"""
PHILLY_ZIP_CODES = [
  19102, 19103, 19104, 19106, 19107, 19109, 19111, 19112, 19114, 19115, 
  19116, 19118, 19119, 19120, 19121, 19122, 19123, 19124, 19125, 19126, 
  19127, 19128, 19129, 19130, 19131, 19132, 19133, 19134, 19135, 19136, 
  19137, 19138, 19139, 19140, 19141, 19142, 19143, 19144, 19145, 19146, 
  19147, 19148, 19149, 19150, 19151, 19152, 19153, 19154]
"""

def main( in_fname, lon_idx, lat_idx, lon_lat_fname, out_fname ):

    # Extract lon/lat
    extract_lon_lat( in_fname, lat_idx, lon_idx, lon_lat_fname )
    print("Completed extraction")


    # Convert lon/lat to zip
    lon_lat_to_zip( lon_lat_fname, out_fname )
    print("Completed conversion")


def extract_lon_lat( fname, lat_idx, lon_idx, outname ):
  """ Create CSV file with zip code. """ 

  # Extract lat/lon data
  fid_w = open(outname, 'w')

  with open(fname, 'r') as fid_r:

    row_number = 0

    # Skip header row
    header = fid_r.readline()

    # Iterate over rows
    for line in fid_r:

        # Extract lat/lon
        line = line.split(',')
        dec = 6     # Round to 6 decimals
        lon = round( float(line[lon_idx]), dec)
        lat = round( float(line[lat_idx]), dec)
        
        # Write to other file
        fid_w.write( str(lat) + ',' + str(lon) + ',' + '\n')


def parse_zip( api_resp ):
    """ Parse the zip code from the Geocode API response. """

    try:
        # Parser found by examining the response
        zc = api_resp[0]['address_components'][0]['long_name']
    except:
        zc = -1

    return zc


def lon_lat_to_zip( fname, outname ):
    """ Convert lon/lat data to zip codes in an efficient manner. """
    
    fid_read  = open(fname, 'r')        
    fid_write = open(outname, 'r+')  # Open a second file to write output

    # Iterate to perform API requests
    writing_new_data = False
    for i, line in enumerate(fid_read):

        # Report progress
        if ( i % 25 == 0 ):
            print("Progress: Index {}".format(i))
        
        # Extract lat/lon
        data = line.split(',')
        lat, lon = data[0], data[1]

        # Only make requests if zip code not already found
        if (writing_new_data == False):
            try:
                data_written = fid_write.next()
            except:
                writing_new_data = True

        # API request
        if (writing_new_data==False): continue
        response = gmaps.reverse_geocode((lat, lon), result_type="postal_code")

        # Parse zip code from API response
        zip_row = parse_zip( response )
        
        # Debugging output
        if ( zip_row == -1):
            print("Index {} failed for data {}, {}".format(i, lat, lon))
        
        # Write zip code data
        data.insert(2, str(zip_row))
        fid_write.write(','.join(data))


if __name__ == '__main__':
    """ Call by specifing name of dataset and indices of lon/lat coordinates.

    python data_cleaning <filename> <lon_idx> <lat_idx>
    """

    # python data_cleaning.py PPR_StreetTrees.csv 0 1
    # python data_cleaning.py theft.csv 11 12
    # python data_cleaning.py 2014crimetrainingdata.csv 12 13


    # Check that script called correctly
    if (len(sys.argv) != 4 ):
        print('Error')

    lon_idx = int( sys.argv[2] )
    lat_idx = int( sys.argv[3] )

    # Create intermediate filename
    in_fname = sys.argv[1]
    tmp = in_fname.split('.')
    tmp.insert(1, '_ll.')
    lon_lat_fname = ''.join(tmp)

    # Create output filename
    tmp = in_fname.split('.')
    tmp.insert(1, '_zip.')
    out_fname = ''.join(tmp)

    main(in_fname, lon_idx, lat_idx, lon_lat_fname, out_fname)
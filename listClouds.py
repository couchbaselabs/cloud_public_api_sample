
# -*- coding: utf-8 -*-

# Generic/Built-in

# Other Libs


import texttable as tt

# Owned
from cbcapi.cbc_api import cbc_api_get

__author__ = 'Jonathan Giffard'
__copyright__ = 'Copyright 2021, Couchbase'
__credits__ = ['Jonathan Giffard']
__license__ = 'GPL 2.0'
__version__ = '0.1.0'
__maintainer__ = 'Jonathan Giffard'
__email__ = 'jonathan.giffard@couchbase.com'
__status__ = 'Dev'


def _pretty_table(table_heading, table_rows):
    # This creates a formatted table using texttable

    pretty_table = ''

    tab_tt = tt.Texttable(900)

    # Characters used for horizontal & vertical lines
    # You can have different horizontal line for the header if wanted

    tab_tt.set_chars(['-', '|', '-', '-'])

    tab_tt.add_rows([table_heading] + table_rows)

    pretty_table = tab_tt.draw()

    return pretty_table


def get_api_status():

    returned_api_status = None

    status_api_response = cbc_api_get('/v2/status')

    if status_api_response is not None:
        # API got called , check if we got something back
        if status_api_response['responseStatus'] is not None:
            returned_api_status = status_api_response['responseHTTPInfo']['httpMessage']

    return returned_api_status

def get_clouds_from_api():

    clouds_api_response = cbc_api_get('/v2/clouds')

    cloud_list = []

    if clouds_api_response['responseStatus'] is not None:
        list_of_clouds = clouds_api_response['responseContent']

        # Did we get a list?
        if list_of_clouds is not None:
            for cloud in list_of_clouds['data']:
                # Builds up a row to display in a table
                # Table is generated by _pretty_table
                # by whomever called this function
                cloud_list.append([cloud['name'],cloud['provider'] , cloud['region'], cloud['id']])

    return(cloud_list)


def list_clouds():
    # Lists all clouds showing the name, provider, creation date and ID

    # Get a list of clouds
    # which will be used as rows in the output table

    cloud_table_rows = get_clouds_from_api()
    if len(cloud_table_rows) > 0:
        # We got data back
        # Table heading / rows for the output
        cloud_table_headings = ['Name','Provider','Region', 'ID']

        print('Cloud')
        print( _pretty_table(cloud_table_headings,cloud_table_rows))
    else:
        # We didn't get anything back
        print('Whoops something has gone wrong')
        print('Check environmental variables')


    return


def main():
    if get_api_status() == 'Success':
        list_clouds()
    else:
        print('Whoops something has gone wrong')

if __name__ == '__main__':
        main()


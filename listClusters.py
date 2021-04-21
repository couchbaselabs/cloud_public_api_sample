
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

def get_clusters_from_api():

    cluster_api_response = cbc_api_get('/v2/clusters')

    cluster_list = []

    if cluster_api_response['responseStatus'] is not None:
        list_of_clusters = cluster_api_response['responseContent']

        # Did we get a list?
        if list_of_clusters is not None:
            for cluster in list_of_clusters['data']:
                # Builds up a row to display in a table
                # Table is generated by _pretty_table
                # by whomever called this function
                cluster_list.append([cluster['name'], cluster['id'], cluster['nodes'], cluster['services']])

    return(cluster_list)


def list_clusters():
    # Lists all clouds showing the name, provider, creation date and ID

    # Get a list of clouds
    # which will be used as rows in the output table

    cluster_table_rows = get_clusters_from_api()

    print(cluster_table_rows)

    if len(cluster_table_rows) > 0:
        # We got data back
        # Table heading / rows for the output
        cluster_table_heading = ['Name','ID', 'Nodes', 'Services']

        print('Clusters')
        print(_pretty_table(cluster_table_heading,cluster_table_rows))
    else:
        # We didn't get anything back
        print('Whoops something has gone wrong')
        print('Check environmental variables')

    return


def main():
    if get_api_status() == 'Success':
        list_clusters()
    else:
        print('Whoops something has gone wrong')

if __name__ == '__main__':
        main()


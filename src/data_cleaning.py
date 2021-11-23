'''
Script to produce data files for analysis
'''
import os
import sys
import pandas as pd
import glob
from collections import defaultdict
from utils.helpers import (clean_artist_count, clean_sales_data,
                            group_sales_data, get_groupings, save_xlsx)
from utils.config import REMOVE_ARTIST_IDS, COLS

if __name__== "__main__":
    # Retrieve any arguments if available
    args = sys.argv # date
    # Retrieve times as strings
    time_start = pd.Timestamp(args[1]) if 1 < len(args) else pd.Timestamp(2019,1,1)
    time_end = pd.Timestamp(args[2]) if 2 < len(args) else pd.Timestamp(2020,1,1)

    print('Start Date (Inclusive): {}'.format(time_start))
    print('End Date (Exclusive): {}'.format(time_end))

    # File stored
    path = os.path.dirname(os.getcwd())+'/data/raw/'

    # Output file of cleaned data
    output_file = os.path.dirname(os.getcwd())+'/data/output/clean_data.xlsx'

    # Use Glob to retrieve all of the file names
    file_list = glob.glob(path+'*.xlsx')

    # Upload files
    d = defaultdict(lambda: defaultdict())
    for i,f in enumerate(file_list):
        d[file_list[i][len(path):-5]] = pd.read_excel(f)

    print('Retrieving Three Year Sales Data...')
    # Retrieve Three Year Sales Data
    three_year = d['three_year_sales'].copy()
    # Clean data
    three_year = clean_sales_data(three_year)
    # Group sales data
    three_yr_grp = group_sales_data(three_year)

    print('Retrieving Demographics Data...')
    # Retrieve demographic data
    demographic = d['demographics'].copy()
    # Remove Unamed column
    demographic = demographic.drop(labels=['Unnamed: 0'], axis=1)
    # Drop duplicates - Artist ID 133 is duplicated
    demographic = demographic.drop_duplicates(subset=['artist_id'], keep='last').reset_index(drop=True)

    print('Joining Sales and Demographics Data...')
    # Join Sales and Demographic data
    joined = three_yr_grp.merge(demographic, how='outer', left_on='Artist Payroll ID', right_on='artist_id')

    # Include only wanted Artist IDS - Remove Artist ID: 0
    inc_df = joined[~joined['Artist Payroll ID'].isin(REMOVE_ARTIST_IDS)]

    # Sales data with no demographic data
    null_demo = inc_df[pd.isnull(inc_df['artist_id'])].copy().reset_index(drop=True)

    # Sales data with demographic data
    demo = inc_df[~(pd.isnull(inc_df['artist_id'])) & ~(pd.isnull(inc_df['Artist Payroll ID']))].copy().reset_index(drop=True)

    print('Retrieving Artist Group Size Data...')
    # Retrieve artist group size data
    grp_size = d['artist_count'].copy()
    grp_size = clean_artist_count(grp_size)

    print('Filtering All Data by Dates, \n beg {} and \n end {}...'.format(time_start, time_end))
    # Filter data by date
    df = demo[(demo['Date']>=time_start) & (demo['Date']<time_end)].copy().reset_index(drop=True)

    print('Merging All Data...')
    # Merge demo and sales data with group size data
    df_merged = df.merge(grp_size, on='artist_id')

    # Retrieve only relevant columns
    df_merged = df_merged[COLS]

    print('Retrieving Grouped Data...')
    # Retrieve dictionary of dataframes of different groupings
    d = get_groupings(df_merged)

    # Merged data, non grouped
    d['merged_all'] = df_merged
    d['merged_demo'] = demo
    d['merged_no_demo'] = null_demo

    print('Outputting tabs into Excel: ')
    save_xlsx(d, output_file)
    print('Output data in Excel sheet in path {}'.format(output_file))
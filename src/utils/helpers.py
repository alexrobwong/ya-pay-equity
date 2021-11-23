'''
Helper functions for data cleaning
'''
import pandas as pd
from collections import defaultdict
from dotenv import load_dotenv
from pandas import ExcelWriter
#from .config import COMPONENTS, MULT_IDS, REMOVE_ARTIST_IDS, CMP_FILT
from config import COMPONENTS, MULT_IDS, REMOVE_ARTIST_IDS, CMP_FILT

def upload_dict(file_list, path):
    '''
    Upload data files into dictionary
    '''
    # Create a dictionary
    d = defaultdict()

    # Iterate through file list with name as key and data as DataFrame
    for i,f in enumerate(file_list):
        d[file_list[i][len(path):-5]] = pd.read_excel(f)

    return d

def clean_sales_data(df):
    '''
    Performs data cleaning to map some unmapped Payroll IDs to Artists
    Group some Literary Art to LIterary Arts
    Removes records with remaining NULL Artist Payroll IDS
    '''
    # Copy dataframe
    df = df.copy()

    # Strip and rename columns
    df.columns = [col.strip() for col in list(df.columns)]

    # Mapping for IDs
    id_map = defaultdict()
    for aid, an in zip(df['Artist Payroll ID'], df['Artist: Account Name']):
        if pd.isnull(aid)==False:
            id_map[an] = aid

    # Literary Art to Literary Arts
    df.loc[df[df['Art Form (General Discipline)']=='Literary Arts'].index, ['Art Form (General Discipline)']] = 'Literary Art'

    # Map missing names # Artist Payroll ID. Map some unmapped ones
    df['Artist Payroll ID'] = df.apply(lambda x: id_map.get(x['Artist: Account Name']) if pd.isnull(x['Artist Payroll ID']) else x, axis=1)['Artist Payroll ID']

    # Map Artists with same ID, but multiple groups:
    df['Artist Payroll ID'] = df.apply(lambda x: MULT_IDS.get(x['Artist: Account Name']) if MULT_IDS.get(x['Artist: Account Name']) is not None else x, axis=1)['Artist Payroll ID']

    # Removes unwanted rows that still have a NULL Artist Payroll ID
    print('Number of NULL Artist IDs removed: {}'.format(len(df[pd.isnull(df['Artist Payroll ID'])])))
    df = df[~df.index.isin(list(df[pd.isnull(df['Artist Payroll ID'])].index))].reset_index(drop=True)

    return df

def group_sales_data(df):
    '''
    Groups sales data together by contract number, date, artist ID
    This is because Workshops are broken out by assemblies
    E.g. 3 assemblies on the same day would be 3 different records, we want to group them together
    '''

    # Group by appropriate columns
    df_grp = df.groupby(['Artist Payroll ID', 'Artist: Account Name', 'Art Form (General Discipline)', 'Contract Classification', 'Date', 'Contract #', 'Client Zip Code', 'Client', 'Billing Code', 'Component Type', 'Artist Business name']).sum()['Artist Fee'].reset_index().reset_index(drop=True)

    # Retrieve only top components
    df_grp = df_grp[df_grp['Component Type'].isin(COMPONENTS)].copy()

    return df_grp

def clean_artist_count(df):
    '''
    Cleans artists per group spreadsheet
    Removes the artists with Remove in notes and also w/ artist ID designated in config Artist ID=0
    '''
    df = df.copy()
    # Capture only ones we want to keep (don't keep ones that say REMOVE)
    df = df[~(df['status'].str.contains('Remove')==True)].copy()
    df = df[~df['artist_id'].isin(REMOVE_ARTIST_IDS)]

    return df.reset_index(drop=True)

def get_groupings(df):
    # Dictionary of output
    d_cmp = defaultdict()

    # Iterate through the component types
    for c in CMP_FILT:
        df_tmp = df[df['Component Type'].str.contains(c)].copy().reset_index(drop=True)

        # Check if workshop otherwise filter by performance
        if c=='Workshop':
            d_cmp['{}_ind'.format(c)] = df_tmp[df_tmp['workshop']==1]
            d_cmp['{}_grp'.format(c)] = df_tmp[df_tmp['workshop']>1]
        else:
            d_cmp['{}_ind'.format(c)] = df_tmp[df_tmp['performance']==1]
            d_cmp['{}_grp'.format(c)] = df_tmp[df_tmp['performance']>1]

    return d_cmp

def save_xlsx(dict_df, path):
    """
    Save a dictionary of dataframes to an excel file, with each dataframe as a separate page
    """

    writer = ExcelWriter(path)
    for key in dict_df:
        print(key)
        dict_df[key].to_excel(writer, key, index=False)

    writer.save()
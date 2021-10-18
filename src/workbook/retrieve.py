#!/home/ubuntu/venv/bin/python
# Import Libraries
from urllib.parse import unquote
from urllib.parse import quote
from urllib.parse import urlencode
import urllib
import re
import requests
from collections import defaultdict
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from datetime import date, timedelta
from collections import defaultdict
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def get_request(url, params=None, headers=None):
    r = 'Error'
    try:
        r = requests.get(url=url,params=params,headers=headers,timeout=60*10)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("Oops: Something Else",err)
    return r

#####
def get_section(text, code):
    """
    Parse XML file to retrieve section by LOINC Code
    text: String of text
    code: String of LOINC Code to filter
    section_str --> returns String of filtered section based on LOINC
    """

    section_segment = re.compile(r'''
        code=\"{}\"
        ((.|\n)*?)
        <code\ code
        '''.format(code), re.VERBOSE)

    section_str = section_segment.findall(text)

    if section_str:
        return section_str[0][0] # Return string if found

    return print("Section not found")

def get_indications(section):
    """
    Retrieve indications from section
    section: String of filtered section
    Returns list of content
    """

    soup = BeautifulSoup(section, 'lxml')
    content = soup.find_all('content')
    #List of content in the content tag
    #Remove content that has <item> as parent tag because they indicate "Limitations of Use"
    return [c.string for c in content  if c.parent.name=='paragraph']

def get_dosages(section):
    """
    Retrieve indications mapped to dosages from section
    section: String of filtered section
    Returns dictionary of indications:dosages
    """
    bs = BeautifulSoup(section, 'lxml')
    dosage = bs.find_all('item') #Find all item tags
    id_dict = defaultdict() # Create default dictionary
    for d in dosage:
        s = d.contents[0] #Retrieve first value of each element in list
        s = s.split(':') #Split indication from dosage level
        #print('{}:{}'.format(s[0], s[1]))
        if id_dict.get(s[0]) is None:
            id_dict[s[0]] = s[1].strip('. (') # f it doesn't exist in dictionary then add
            #print("Entered: ", id_dict)
        else:
            id_dict[s[0]].append(s[1]) #If it exists in dicitonary, then append

    return id_dict

def get_match(indications, dosages):
    """
    indications: List of indications parsed from DailyMed XML Indication "34067-9" Section
    dosages: Dictionary of indication (abbreviated) and dosage instruction parsed from DailyMed XML Dosage "34068-7" Section
    df: Returns a dataframe w/ columns for indication, indication dosage, dosage, and fuzzy match score
    """
    df = pd.DataFrame(columns = ['indication', 'dosage_ind', 'dosage', 'score'])
    d_keys = list(dosages.keys()) #Retrieve indication names from dosage info

    #Iterate through indicationsa to see if there's a match with dosages
    for ind in indications:
        eo = process.extractOne(ind, d_keys, scorer=fuzz.partial_token_sort_ratio)
        dosage_ind = eo[0]
        score = eo[1]
        dosage = dosages[dosage_ind]
        if score<=50: #If low fuzzy match score then don't add
            dosage_ind, dosage, score = None, None, None
        df = df.append({'indication': ind, 'dosage_ind': dosage_ind, 'dosage': dosage, 'score': score}, ignore_index=True)

    return df

def return_mapping(set_id):
    """
    Return mapping for a specific drug with set_id to review mapping
    """

    #Request data via API
    url_dm = 'https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/{}.xml'.format(set_id)
    spls = get_request(url=url_dm)

    #Parse XML for indications and dosage sections
    indications_sec = get_section(spls.text, "34067-9")
    dosage_sec = get_section(spls.text, "34068-7")

    #List of indication names and dictionary of dosage indication names and dosages
    ind = get_indications(indications_sec)
    dos = get_dosages(dosage_sec)

    #Fuzzy match and return dataframe
    df = get_match(ind, dos)

    return df

def get_section_dm(set_id, sec):
    url_dm = 'https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/{}.xml'.format(set_id)
    spls = get_request(url=url_dm)
    section = get_section(spls.text, sec)

    return section

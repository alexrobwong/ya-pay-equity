# ya-pay-equity
This repo is for the Young Audiences - Artist Pay Equity project as supported by INFORMS Pro Bono Analytics. More information on this project can be found in our google drive folder: https://drive.google.com/drive/folders/1oYqk7QSaUyyeF2URFjdeLuZt0J9x8Vvj?usp=sharing (access request is required)

&nbsp;
## Goal
The purpose of this project is to ensure pay equality for all of YA's artists (where demographic information is not a factor in the final agreed upon prices for services).

&nbsp;
## Data
The data we use consists of three different files in the `data/raw/` folder:

1. **Three Year Sales Data**: `three_year_sales.xlsx`
   Salesforce data in spreadsheet format containing records of transactions for artists over the past three years from 7/2/18 to 6/19/21.

2. **Demographics Data**: `demographics.xlsx`
   Artist demographics data that combines the two demographics surveys sent out earlier this year to YA's artists.

3. **Artist Grouping**: `artist_count.xlsx`
   Data of artist group size count by component type (Performance, Workshop).

Data is joined on Artist ID

&nbsp;
## Data Cleaning Performed:
**All Files:**
* Artist IDs Mapped: Artist IDs 20, 95, 56 have multiple Artist Names due to the individuals performing as individuals and in groups. Excel data has been manually edited to include mappings for the same Artist IDs w/ different Artist Names: {95--> 95.1, 95.2, & 95.3}.

**Three Year Sales:**
  * Records Grouped: Different sessions under the same contract are listed separately in the Salesforce Sales Data and can be grouped together. E.g. one contract could be listed as three separate records because it consists of three assemblies on the same day, so we can group the records together by Contract #, Artist ID, and Date.
  * Existing Unmapped Artist IDs are mapped based on Artist Names
  * For some records: Art Form (General Discipline) for 'Literary Arts' --> 'Literary Art'
  * Artists with no Artist IDs were removed ~4 records.
  * Filtered by top components: Performance, Workshop, Learning, and Meeting
  * Removed Artist ID 0

**Demographics**
* Demographics survey was sent out in Parts 1 and 2. Manually cleaning has been performed that includes: binning ages, mapping artists to artist ids, converting free text responses to categorical values, etc. Parts 1 and 2 were joined to formed the shortened demographics data response.

**Artist Counts**
* Column added to separate the artist group size between performances and workshops.


---
&nbsp;
## How to Use the Script:

Navigate to the `src` folder and in terminal enter:
```zsh
python data_cleaning.py
```

Running this will default to 2019 data only. To add date filters:

```zsh
python data_cleaning.py '2019-01-01' '2021-01-01'
```
Start date is first (inclusive) and end date is second (exclusive)

&nbsp;
## Output File & Tabs:
Output will be saved in `data/output/clean_data.xlsx`

Tabs:
1. **Performance_ind**:
   * Component Type contains Performance; Individuals; Filtered by date
2. **Performance_grp**:
   * Component Type contains Performance; Groups; Filtered by date
3. **Workshop_ind**:
   * Component Type contains Workshop; Individuals; Filtered by date
4. **Workshop_grp**:
   * Component Type contains Workshop; Groups; Filtered by date
5. **Learning_ind**:
   * Component Type contains Learning; Individuals; Filtered by date
6. **Learning_grp**:
   * Component Type contains Learning; Groups; Filtered by date
7. **Meeting_ind**:
   * Component Type contains Meeting; Individuals; Filtered by date
8. **Meeting_grp**:
   * Component Type contains Meeting; Groups; Filtered by date
9.  **merged_all**:
    * Merged data (INNER JOIN) of sales, demographics, and artist grp size; Filtered by date
10. **merged_demo**
    * Merged data (INNER JOIN) of sales and demographics; Filtered by date
11. **merged_no_demo**
    * Sales data where Artist IDs did not have demographics data; Filtered by date

## Other Files
* `utils` folder contains:
  * `config.py` which sets some global variables and
  * `helpers.py` which contains helper functions for the `data_cleaning.py` script.
* `workbook` folder contains:
  * Jupyter Notebooks used to create the script and tests
  * Jupyter Notebook for attempted Regression modeling

## Authors
1. Alexander Wong (alexander.robert.wong@gmail.com)
2. JJ Gong (jjgong7@gmail.com)
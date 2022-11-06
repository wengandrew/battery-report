"""
11/05/2022

Post-process outputs from H1-B website to assign inflation-adjusted salaries,
job levels, job categories, and job relevance.

Original code from Linda Jing.
"""

import yaml
import pandas as pd

PATH_IN = "output/output_raw.csv"
PATH_OUT = "output/output_processed.csv"

PATH_CONFIG_TITLES = 'config/titles.yml'
PATH_CONFIG_LEVELS = 'config/levels.yml'
PATH_CONFIG_CPI    = 'config/cpi.yml'
PATH_CONFIG_RELEVANT_COMPANIES = 'config/company_list_relevant.csv'

def main():

    # Prepare and load dataframe
    df = pd.read_csv(PATH_IN)
    df['year'] = pd.DatetimeIndex(df['start date']).year
    df['salary'] = df["salary"].str.replace(",","").astype(float)
    df['salary_normalized'] = None
    df['level'] = None
    df['category'] = None
    df['relevance'] = None

    # Assign additional fields
    print('Normalizing salaries...')
    df = normalize_salary(df)

    print('Assigning relevance...')
    df = label_relevance(df)

    print('Assigning levels...')
    df = label_levels(df)

    print('Assigning titles')
    df = label_titles(df)


    df.to_csv(PATH_OUT)
    print('Done.')

def label_relevance(df):

    # convert company csv to list
    company_list_df = pd.read_csv(PATH_CONFIG_RELEVANT_COMPANIES)
    company_list = company_list_df['Company'].to_list()
    company_list = [x.upper() for x in company_list]

    # remove salary above 900k and below 30k
    df.loc[df['salary'] > 900000, 'category'] = 'Incorrect Values'
    df.loc[df['salary'] < 30000, 'category'] = 'Incorrect Values'

    for index, row in df.iterrows():

        # 0 is not relevant, 1 is relevant
        substrings = ['ACCOUNTANT',
                      'ART DIRECTOR',
                      'ACCOUNT',
                      'ASIC DESIGN',
                      'CELLULAR']

        if any([x in row['title'] for x in substrings]):

            if pd.isnull(df.at[index, 'category']):
                df.at[index,'category'] = 'Irrelevant'

            if pd.isnull(df.at[index, 'relevance']):
                df.at[index, 'relevance'] = 'Irrelevant'

        if any([x in row['title'] for x in ['BATTERY']]):

            if pd.isnull(df.at[index,'relevance']):
                df.at[index, 'relevance'] = 'Battery'

        if any([x in row['title'] for x in ['VEHICLE']]):

            if pd.isnull(df.at[index, 'relevance']):
                df.at[index, 'relevance'] = 'Vehicle'

        if any([x in row['company'] for x in company_list]):

            if pd.isnull(df.at[index, 'relevance']):
                df.at[index, 'relevance'] = 'Relevant'

        substrings = ['APPLE',
                      'OAK RIDGE',
                      'WAYMO',
                      'UT-BATTELLE',
                      'AC PROPULSION INC',
                      'ACRO SERVICE CORPORATION',
                      'AEROTEK INC',
                      'ALTAIR PRODUCTDESIGN INC',
                      'APTIV CORPORATION',
                      'BENDIX COMMERCIAL VEHICLE SYSTEMS LLC',
                      'CRUISE',
                      'NURO',
                      'SIRIUS XM CONNECTED VEHICLE SERVICES INC',
                      'TUSIMPLE',
                      'VISTEON CORPORATION',
                      'ZOOX',
                      'NATRON',
                      'BATTELLE MEMORIAL',
                      'YOTTA',
                      'ASCII GROUP',
                      'ALTAIR',
                      'AGGREKO LLC']

        if any([x in row['company'] for x in substrings]):
            if not any([x in row['title'] for x in ['BATTERY','CELL','VEHICLE']]):
                if pd.isnull(df.at[index, 'relevance']):
                   df.at[index,'relevance'] = 'Irrelevant'

    # fill the rest with not relevant
    df['relevance'] = df['relevance'].fillna(value=0)

    return df


def label_levels(df: pd.DataFrame) -> pd.DataFrame:

    with open(PATH_CONFIG_LEVELS, 'r') as file:
        levels = yaml.safe_load(file)

    for index, row in df.iterrows():

        # Start from the highest level and work down from there;
        # Assign all remaining roles as 'Junior' by default.
        for level in levels.keys():

            include_list = [x.upper() for x in levels[level]['incl']]
            exclude_list = [x.upper() for x in levels[level]['excl']]
            no_levels_to_exclude = (len(exclude_list) == 1) and (exclude_list[0] == '')

            if no_levels_to_exclude:
                if any( [x in row['title'] for x in include_list] ):
                    if pd.isnull(df.at[index, 'level']):
                        df.at[index, 'level'] = level
            else:
                if any( [x in row['title'] for x in include_list] ) \
                    and not any( [x in row['title'] for x in exclude_list] ):
                    if pd.isnull(df.at[index, 'level']):
                        df.at[index, 'level'] = level

        if pd.isnull(df.at[index, 'level']):
            df.at[index, 'level'] = 'Junior'

    return df


def label_titles(df: pd.DataFrame) -> pd.DataFrame:

    with open(PATH_CONFIG_TITLES, 'r') as file:
        titles = yaml.safe_load(file)

    for index, row in df.iterrows():

        for title in titles.keys():

            include_list = [x.upper() for x in titles[title]['incl']]
            exclude_list = [x.upper() for x in titles[title]['excl']]
            no_titles_to_exclude = (len(exclude_list) == 1) and (exclude_list[0] == '')

            if no_titles_to_exclude:
                if any( [x in row['title'] for x in include_list] ):
                    if pd.isnull(df.at[index, 'category']):
                        df.at[index, 'category'] = title
            else:
                if any( [x in row['title'] for x in include_list] ) \
                    and not any( [x in row['title'] for x in exclude_list] ):
                    if pd.isnull(df.at[index, 'category']):
                        df.at[index, 'category'] = title

        if any([x in row['level'] for x in ['Manager','Director','C-Suite']]):
            if pd.isnull(df.at[index, 'category']):
                df.at[index, 'category'] = 'General'

    return df


def normalize_salary(df: pd.DataFrame) -> pd.DataFrame:

    with open(PATH_CONFIG_CPI, 'r') as file:
        cpi = yaml.safe_load(file)

    cpi_pct = cpi['cpi_dict'].copy()

    for key, value in cpi_pct.items():

        cpi_pct[key] = cpi['current_cpi']/value

    df_cpi_pct = pd.DataFrame.from_dict(cpi_pct,
                                        orient='index',
                                        columns=['cpi_pct'])

    df_cpi_pct['year']=df_cpi_pct.index.astype(int)

    df = df.merge(df_cpi_pct, how='left', on='year')

    df['salary_normalized'] = round(df['salary'] * df['cpi_pct'], 0)

    return df


if __name__ == "__main__":
    main()

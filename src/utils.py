"""
Utility functions
"""

import pandas as pd
import numpy as np
import re

def calculate_fraction_of_jobs_with_battery_in_title():
    """
    Returns the fraction of job titles that have battery-related words in the
    title.

    Context: a lot of jobs are related to the battery industry. These jobs may
    not have battery-related key-words in the job title itself. Let's try to
    figure out what fraction of battery-related jobs have these specific
    keywords in the title.
    """

    # Fetch the processed list of jobs scraped from the H1B website.
    df = pd.read_csv('data/data_processed.csv')

    # Filter for only battery-related jobs
    df_filt = df[df['relevance'].isin(['Battery', 'Relevant', 'Vehicle'])]

    # Define criteria for a job title to explicitly contain battery-related
    # keywords
    match = lambda x: len(re.findall(r'battery|cell|bms|module', x)) >= 1

    # Count the number of jobs with battery-related keywords
    num_jobs_with_battery_terms = np.sum([match(x.lower()) for x in
                                               df.title.values])

    # Calculate the total
    num_jobs = len(df_filt)

    fraction = num_jobs_with_battery_terms / num_jobs

    return fraction

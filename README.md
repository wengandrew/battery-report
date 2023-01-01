# battery-report

Code and scripts used to generate data and analysis for 'Talent' section of The Battery Report 2022.

Contributors:
- Andrew Weng
- Linda Jing
- Gabe Hege

# Getting Started: H1B Data Survey

## To regenerate the dataset...

First run `src/scraper.py`, starting from the home directory. This will scrape the
web for H1-B data and export it into a file called
`data/data_h1binfo_export.csv`.

Then run `src/labeling.py`. This will return another file called
`data/data_processed.csv` which contains a cleaned up version of the data
including inflation-adjusted salaries and job category labels.

## To visualize the results...

Then visualize the data using `tableau/jobs.twb`. Tableau is required to view
the data.

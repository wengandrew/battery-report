# battery-report

Code and scripts used to generate data and analysis for 'Talent' section of The
Battery Report.

Outputs for each year of the report are organized under `/output'.

Contributors:
- Andrew Weng
- Linda Jing
- Gabe Hege

# Getting Started: H1B Data Survey

## To regenerate the dataset...

1. Configure and activate your virtual environment:

```
source venv/bin/activate
```

2. Install the packages from `requirements.txt`:

```
pip install -r requirements.txt
```

3. Run `src/scraper.py`. This will scrape the
web for H1-B data and export it into a file called
`data/data_h1binfo_export.csv`.

```
python src/scraper.py
```

4. Run `src/labeling.py`. This will return another file called
`data/data_processed.csv` which contains a cleaned up version of the data
including inflation-adjusted salaries and job category labels.

```
python src/labeling.py
```

## To visualize the results...

Then visualize the data using `tableau/jobs.twb`. Tableau is required to view
the data.

"""
11/05/2022

Crawl through H-1B website to export a list of job titles.

Code adapted from Gabe.
"""

from bs4 import BeautifulSoup
import requests
import csv
from os.path import exists
import time

COMPANIES_FILE = 'config/company_list_all.csv'
OUTPUT_FILE = 'output/output_raw.csv'

def search(company, job, city, year, t):

    year = 'all+years'

    url = f"https://h1bdata.info/index.php?em={company}&job={job}&city={city}&year={year}"

    print("Fetching Data from: " + url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    data = []

    for tr in soup.find_all("tr"):
        row = []
        for td in tr.find_all("td"):
            row.append(td.text)
        if "".join(row).strip():
            data.append(row)

    print(f'Writing {len(data)} entries out to {OUTPUT_FILE}')

    file_exists = exists(OUTPUT_FILE)

    with open(OUTPUT_FILE, "a+") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["company",
                             "title",
                             "salary",
                             "location",
                             "submit date",
                             "start date"])

        writer.writerows(data)

    print("Done.")

    return len(data)


if __name__ == "__main__":

    with open(COMPANIES_FILE) as csvfile:

        t = time.time()
        creader = csv.reader(csvfile)
        i = 0
        total = 0

        for row in creader:

            i += 1
            comp = row[0]

            total += search(comp, '', '', '', t)

        print('processed:' + str(i) + " companies.")
        print('found:' + str(total) + " job postings.")


#search('Tesla', '', '', 2021)
